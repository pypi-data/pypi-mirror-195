import subprocess
import random
import string

PIPE = 'pipe'


def get_random_string(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for _ in range(length))
    return result_str


def shell(cmd, keyword='', ignore_error=False, output=True):
    cmd += ' --output yaml'
    if output is False:
        p = subprocess.Popen(cmd, stdout=subprocess.DEVNULL,
                             stderr=subprocess.STDOUT, cwd=None, shell=True)
    else:
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE, cwd=None, shell=True)
    res = ''
    if keyword != '':
        for line in p.stdout.readlines():
            if keyword in line.decode():
                res = line.decode()
                break
    else:
        for line in p.stdout.readlines():
            res = line.decode()
    p.stdout.close()
    error = ''
    for line in p.stderr.readlines():
        print(line.decode())
        error += line.decode()
    if len(error) > 0 and not ignore_error:
        raise Exception(f'shell return error {error[:-1]}')
    p.stderr.close()
    p.wait()
    return res


def get_file_size(file_path):
    get_size_cmd = f'aws s3 ls --summarize --human-readable {file_path}'
    info = shell(get_size_cmd, 'Total Size')
    size = 0
    if 'MiB' in info:
        size = int(float(info.split(':')[1].strip().split(' ')[0])) * 1024 
    if 'GiB' in info:
        size = int(float(info.split(':')[1].strip().split(' ')[0])) * 1024 * 1024
    if 'TiB' in info:
        size = int(float(info.split(':')[1].strip().split(' ')[0])) * 1024 * 1024 * 1024
    return size


def get_instance_type(pbf, sp, ssp):
    instance_type = 'r5.large'
    coefficient = 10

    size = get_file_size(pbf) + get_file_size(sp)
    if ssp != '':
        size += get_file_size(ssp)

    size = coefficient * size / 1024 / 1024  # in gb
    if size < 1:
        print(f'get_instance_type: {instance_type}')
        return instance_type
    if size <= 32:
        instance_type = 'c4.4xlarge'
    elif 32 < size <= 64:
        instance_type = 'c4.8xlarge'
    elif 64 < size <= 128:
        instance_type = 'm5.8xlarge'
    elif size > 128:
        instance_type = 'r5.8xlarge'

    print(f'get_instance_type: {instance_type}')
    return instance_type


def get_memory_size(instance_type):
    memory_size = 16
    if instance_type == 'c4.4xlarge':
        memory_size = 30
    elif instance_type == 'c4.8xlarge':
        memory_size = 60
    elif instance_type == 'm5.8xlarge':
        memory_size = 128
    elif instance_type == 'r5.8xlarge':
        memory_size = 256
    return memory_size


def get_volume_size(pbf, sp, ssp):
    size = get_file_size(pbf) + get_file_size(sp)
    if ssp != '':
        size += get_file_size(ssp)
    if 25 * (size / 1024 / 1024) < 8:
        return 8
    return 25 * (size / 1024 / 1024)
