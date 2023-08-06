import click
import requests
import tabulate

class Struct:
    def __init__(self, **entries):
        self.__dict__.update(entries)


@click.group()
def hpc():
    """Group for hpc commands."""
    pass

@hpc.command()
@click.pass_context
def list(ctx):
    """List HPC clusters"""
    config = ctx.obj
    url = config.get("default","url")
    cookie = config.get("default","cookie")
    r = requests.get(url + "/api/hpc/clusters/", cookies={"_oauth2_proxy": cookie}, verify=False)
    if r.status_code != 200:
        print(r.text)
        raise click.Abort()

    data = r.json()
    username = config.get("default","username")
    workspaces = [["id", "name", "status", "image", "memory(GB)", "cores", "gpu", "created"]]
    for workspace in data:
        w = Struct(**workspace)
        if w.owner != username:
            continue
        workspaces.append([w.id, w.name, w.status, w.image, w.memory, w.cpu_count, w.gpu_count, w.created_at])
    print(tabulate(workspaces, headers="firstrow", tablefmt="presto"))
