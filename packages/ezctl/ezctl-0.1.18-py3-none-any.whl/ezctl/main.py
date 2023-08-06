import typer
from commands import deploy as cmd_deploy
from commands import check as cmd_check
from commands import terminate as cmd_terminate


app = typer.Typer()


@app.command()
def deploy(service: str = '', pbf: str = '', sp: str = '', ssp: str = ''):
    if service == 'osrm':
        public_ip, instance_id = cmd_deploy.Deploy(pbf, sp, ssp).apply()
        print(f'\nFinished setup with public ip {public_ip} and instance id {instance_id}.')


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
