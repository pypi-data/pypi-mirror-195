import os
import subprocess

src_dir = os.path.dirname(__file__)

def su(uid: int, gid: int):
    """
    Switches user in current process.
    """
    os.setgid(gid)
    os.setuid(uid)

def run(
    username: str,
    cmd_list: list[str],
    login=False,
    **kwargs
):
    """
    Switches user in the subprocess.run command line,
    and runs the cmd_list.
    """
    run_list: list[str] = ['su']

    if login:
        run_list.append('-')

    run_list += [username, '-c', ' '.join(cmd_list)]

    subprocess.run(run_list, **kwargs)

def start(
    username: str,
    cmd_list: list[str],
    login=False,
    **kwargs
):
    """
    Switches user in another python process 
    which runs the cmd_list.
    """
    run_list: list[str] = [
        f'{src_dir}/process.py',
        username,
        'True' if login else 'False',
        str(cmd_list)
    ]
    subprocess.run(
        run_list,
        **kwargs
    )
