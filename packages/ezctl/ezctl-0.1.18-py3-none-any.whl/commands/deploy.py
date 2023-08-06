import time
import json
import math
from commons import common as common
from commands import check as cmd_check
import requests


class Deploy:
    def __init__(self, pbf, sp, ssp):
        self.pbf = pbf
        self.sp = sp
        self.ssp = ssp
        self.instanceid = ''
        self.public_ip = ''
        self.private_ip = ''

    def start_ec2_instance(self):
        instance_type = common.get_instance_type(self.pbf, self.sp, self.ssp)
        volume_size = math.ceil(common.get_volume_size(self.pbf, self.sp, self.ssp))
        mapping = [{"DeviceName": "/dev/xvda", "Ebs": {"VolumeSize": volume_size}}]
        create_ec2_instance_cmd = f'aws ec2 run-instances --image-id ami-0d06ca04c761f2766 --count 1 --instance-type {instance_type} --key-name ezctl --security-group-ids sg-0bfb8b5daee5dc0af  --iam-instance-profile Name=EnablesEC2SSMAndECRRole \
            --block-device-mappings \'{json.dumps(mapping)}\' --region ap-southeast-1'
        self.instanceid = common.shell(create_ec2_instance_cmd, 'InstanceId').strip().split(':')[1].strip()
        return instance_type

    def get_pulic_ip(self):
        get_public_ip_cmd = f'aws ec2 describe-instances --instance-ids {self.instanceid} --query \'Reservations[*].Instances[*].PublicIpAddress\' --region ap-southeast-1'
        self.public_ip = common.shell(get_public_ip_cmd).split('-')[2].strip().replace('\n', '')

    def get_private_ip(self):
        get_public_ip_cmd = f'aws ec2 describe-instances --instance-ids {self.instanceid} --query \'Reservations[*].Instances[*].PrivateIpAddress\' --region ap-southeast-1'
        self.private_ip = common.shell(get_public_ip_cmd).split('-')[2].strip().replace('\n', '')

    def generate_password(self):
        password = common.get_random_string(8)
        print(f'Password generated for ec2-user: {password}')
        data = {"Parameters": {"commands": ["sudo sed -i '/^[^#]*PasswordAuthentication[[:space:]]no/c\\PasswordAuthentication yes' /etc/ssh/sshd_config",
                "sudo service sshd restart", f"echo 'ec2-user:{password}' | sudo chpasswd"]}} 
        with open('installation.json', 'w+', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        change_password_cmd = f'aws ssm send-command --document-name "AWS-RunShellScript" --cli-input-json file://installation.json \
            --instance-ids {self.instanceid} --region ap-southeast-1'
        command_id = common.shell(change_password_cmd, 'CommandId').strip().split(':')[1].strip()
        checker = cmd_check.Check(command_id)
        res = checker.apply()
        while res != 'Success':
            if res == 'In Progress' or 'Pending':
                time.sleep(10)
                res = checker.apply()
            if res == 'Failed':
                return False
        return True

    def copy_files(self):
        if not self.pbf.startswith('s3://') or self.pbf.startswith('gs://'):
            print('Please indicate correct pbf path.')
            return False
        if not self.sp.startswith('s3://') or self.sp.startswith('gs://'):
            print('Please indicate correct sp path.')
            return False
        if self.ssp != '':
            if not self.sp.startswith('s3://') or self.sp.startswith('gs://'):
                print('Please indicate correct ssp path.')
                return False
        copy_pbf_cmd = f'aws s3 cp {self.pbf} /home/ec2-user/amylase/data/osrm/UNKNOWN/latest.osm.pbf'
        copy_sp_cmd = f'aws s3 cp {self.sp} /home/ec2-user/amylase/data/sp/output.lua'
        copy_files_cmd = f'aws ssm send-command --document-name "AWS-RunShellScript" --parameters \'commands=["{copy_pbf_cmd}","{copy_sp_cmd}"]\' --instance-ids {self.instanceid} --region ap-southeast-1'
        if self.ssp != '':
            copy_ssp_cmd = f'aws s3 cp {self.ssp} /home/ec2-user/amylase/data/ssp/ssp.csv'
            copy_files_cmd = f'aws ssm send-command --document-name "AWS-RunShellScript" --parameters \'commands=["{copy_pbf_cmd}","{copy_sp_cmd}","{copy_ssp_cmd}"]\' --instance-ids {self.instanceid} --region ap-southeast-1'
        command_id = common.shell(copy_files_cmd, 'CommandId').strip().split(':')[1].strip()
        checker = cmd_check.Check(command_id)
        res = checker.apply()
        while res != 'Success':
            if res == 'In Progress' or 'Pending':
                time.sleep(10)
                res = checker.apply()
            if res == 'Failed':
                return False
        return True

    def preprocessing(self, instance_type):
        memory_size = common.get_memory_size(instance_type)
        start_docker_cmd = f'aws ssm send-command --document-name "AWS-RunShellScript" --parameters \'commands=["sudo service docker start","cd /home/ec2-user/amylase","yarn","nohup bash run {self.private_ip} {memory_size}g {memory_size}g > /home/ec2-user/amylase/out.log 2>&1 &"]\' \
            --output-s3-bucket-name "nextbillion-data" --output-s3-key-prefix "enzyme-stg/ezctl" --timeout-seconds 21600 --instance-ids {self.instanceid} --region ap-southeast-1'
        command_id = common.shell(start_docker_cmd, 'CommandId').strip().split(':')[1].strip()
        print(f'command {command_id} is sent to start docker.')
        url = f'http://{self.public_ip}:80/health'
        while True:
            try:
                requests.get(url=url, timeout=10)
            except Exception:
                print('.', end='', flush=True)
                time.sleep(60)
                continue
            break

    def start_osrm(self):
        start_osrm_cmd = f'aws ssm send-command --document-name "AWS-RunShellScript" --parameters \'commands=["nohup docker run -p {self.private_ip}:5000:5000 -v /home/ec2-user/amylase/data/osrm/UNKNOWN:/data nextbillionai/libosrm:v5.25.0-p3 osrm-routed --algorithm mld /data/latest.osrm >> /home/ec2-user/amylase/osrm.log 2>&1 &"]\' \
            --output-s3-bucket-name "nextbillion-data" --output-s3-key-prefix "enzyme-stg/ezctl" --timeout-seconds 21600 --instance-ids {self.instanceid} --region ap-southeast-1'
        command_id = common.shell(start_osrm_cmd, 'CommandId').strip().split(':')[1].strip()
        print(f'\ncommand {command_id} is sent to start osrm.')

    def apply(self):
        instance_type = self.start_ec2_instance()
        time.sleep(120)
        self.get_pulic_ip()
        self.get_private_ip()
        res = self.generate_password()
        if res is False:
            raise Exception('Password set up failed.')
        res = self.copy_files()
        if res is False:
            raise Exception('Files copy failed.')
        self.preprocessing(instance_type)
        self.start_osrm()
        time.sleep(10)
        return self.public_ip, self.instanceid
