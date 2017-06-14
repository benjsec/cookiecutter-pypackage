import sys

from subprocess import Popen, PIPE


dev_requirements = ['invoke', 'pytest', 'flake8']


def create_env(name):
    cmd_list = ['conda', 'create', '--yes', '--quiet', '--name', name]
    cmd_list.append('python={{ cookiecutter.py_version }}')
    cmd_list.extend(dev_requirements)

    try:
        p = Popen(cmd_list, stdout=PIPE, stderr=PIPE)
    except OSError:
        Exception("could not invoke %r\n" % args)
    out, err = p.communicate()
    if err.decode().strip():
        raise Exception('%s: %s' % (" ".join(cmd_list), err.decode()))
    return out.decode().strip()

    
try:
    out = create_env("{{ cookiecutter.repo_name }}")
except Exception as err:
    print(err)
    sys.exit(1)
else:
    print("Environment {{cookiecutter.repo_name}} created")
    sys.exit(0)
