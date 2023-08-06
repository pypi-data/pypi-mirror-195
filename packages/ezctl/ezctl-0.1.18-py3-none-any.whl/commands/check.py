from commons import common as common


class Check:
    def __init__(self, command_id):
        self.command_id = command_id

    def apply(self):
        check_cmd = f'aws ssm list-commands --command-id {self.command_id} --region ap-southeast-1'
        return common.shell(check_cmd, 'Status').strip().split(':')[1].strip()
