import typer

from sys import path
import os
path.append(os.path.dirname(os.path.abspath(__file__)))

import commands.deploy as cmd_deploy
import commands.check as cmd_check
import commands.terminate as cmd_terminate


app = typer.Typer()


@app.command()
def deploy(service: str = '', provider: str = 's3', pbf: str = '', sp: str = '', ssp: str = ''):
    if service == 'osrm':
        public_ip, instance_id = cmd_deploy.Deploy(pbf, sp, ssp, provider).apply()
        print(f'Finished setup with public ip {public_ip} and instance id {instance_id}.')


@app.command()
def check(command_id: str):
    status = cmd_check.Check(command_id).apply()
    print(f'The current status of the command {command_id} is {status}.')


@app.command()
def terminate(id: str = ''):
    cmd_terminate.Terminate(id).apply()
    print(f'Finished deletion with instance id {id}.')


if __name__ == "__main__":
    app()
