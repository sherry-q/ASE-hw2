# reference tutorial: http://docs.fabfile.org/en/1.12/tutorial.html

from __future__ import with_statement
from fabric.api import *
from fabric.contrib.console import confirm
import os

#env.hosts = ['shopping_list_server']

# run unit tests
def test():
	with settings(warn_only=True):
		result = local('python test.py', capture=True)
	if result.failed and not confirm("Tests failed. Continue anyway?"):
		abort("Aborting at user request.")

def commit():
	local("git add -p && git commit")

def push():
	local("git push")

def prepare_deploy():
	test()
	commit()
	push()

# start server for web app
def deploy():
    with cd(os.getcwd()):
        local("git pull")
        local("python shopping_list.py")