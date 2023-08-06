import sys
import subprocess
import su
import pwd

username: str = sys.argv[1]
login: bool = sys.argv[2] == 'True'
cmd_list: list[str] = sys.argv[3].strip('[]').split(',')

p = pwd.getpwnam(username)
su.su(p.pw_uid, p.pw_gid)

if login:
    su.run(
        username,
        cmd_list,
        login=True
    )
else:
    subprocess.run(
        cmd_list
    )
