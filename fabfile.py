from fabric.api import run, local, env
from fabric.context_managers import cd, prefix


def prod():
    env.hosts = ['greg@vps2.gregbrown.co.nz']
    env.project = "/var/django/notepad"
    env.virtualenv = 'notepad'
    env.restartcommand = 'sudo restart flask_notepad'


def update():
    local('git pull')
    local('git push')
    if env.get('project', False):
        with cd(env.project):
            run('git pull')


def deploy():
    update()
    restart()


def deps():
    update()
    with cd(env.project), prefix('workon %s' % env.virtualenv):
        run('pip install -r requirements.txt')


def restart():
    run(env.restartcommand)
