from commons import common as common


class Terminate:
    def __init__(self, instance_id):
        self.instance_id = instance_id

    def apply(self):
        terminate_instance_cmd = f'aws ec2 terminate-instances --instance-ids {self.instance_id} --region ap-southeast-1'
        common.shell(terminate_instance_cmd, output=False)
