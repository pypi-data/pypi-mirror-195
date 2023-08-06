from sys import path
import os
path.append(os.path.dirname(os.path.abspath(__file__)))

import commons.common as common


class Check:
    def __init__(self, command_id):
        self.command_id = command_id

    def apply(self):
        check_cmd = f'aws ssm list-commands --command-id {self.command_id} --region ap-southeast-1'
        return common.shell(cmd=check_cmd, keyword='Status', s3=True).strip().split(':')[1].strip()
