from fabric.api import env, run, cd, sudo, settings
from fabric.contrib.files import upload_template


env.user = "ubuntu"
env.hosts = ['ec2-54-211-49-231.compute-1.amazonaws.com']
env.key_filename = ["demo.pem"]
env.repo_url = 'git@github.com:setaris/django-tesseract2.git'

env.root = "/home/ubuntu/webapps/djangotesseract2"
env.virtualenv = "/home/ubuntu/envs/djangotesseract2env"
env.project = "%s/djangotesseract2" % env.root
env.servicename = "djangotesseract2"


def deploy():
    "Full deploy: push, buildout, and reload."
    push()
    update_dependencies()
    syncdb()
    update_services()
    reload()


def push():
    "Push out new code to the server."
    with cd("%(project)s" % env):
        run("git pull origin master")


def update_services():
    upload_template('./nginx.conf',
        '/etc/nginx/sites-enabled/default', use_sudo=True)
    upload_template('./service.conf',
        '/etc/init/djangotesseract2.conf', use_sudo=True)

    with cd("/etc/nginx/sites-enabled"):
        sudo('rm *.bak')


def update_dependencies():
    run("%(virtualenv)s/bin/pip install -r %(root)s/requirements.txt" % env)


def createsuperuser():
    with cd("%(project)s" % env):
        run("%(virtualenv)s/bin/python manage.py createsuperuser --settings=djangotesseract2.settings.production" % env)


def syncdb():
    with cd("%(project)s" % env):
        run("%(virtualenv)s/bin/python manage.py syncdb --noinput --settings=djangotesseract2.settings.production" % env)


def reload():
    with settings(warn_only=True):
        sudo("sudo initctl stop djangotesseract2")
    sudo("sudo initctl start djangotesseract2")
    sudo('/etc/init.d/nginx reload')


def setup():
    run("mkdir -p %(root)s" % env)
    sudo("aptitude update")
    sudo("aptitude -y install git-core python-dev python-setuptools "
        "build-essential subversion mercurial nginx"
        "libjpeg62 libjpeg62-dev zlib1g-dev libfreetype6 libfreetype6-dev "
        "ghostscript imagemagick "
        "tesseract-ocr libtesseract-dev")

    sudo("easy_install virtualenv")
    run("virtualenv %(virtualenv)s" % env)
    run("%(virtualenv)s/bin/pip install -U pip" % env)

    with cd("~/webapps/"):
        run("git clone %(repo_url)s" % env)

    sudo("nginx")
    deploy()
