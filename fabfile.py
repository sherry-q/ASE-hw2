from __future__ import with_statement
from fabric.api import *
from fabric.contrib.console import confirm

env.hosts = ['my_server']

def test():
	with settings(warn_only=True):
		result = local('python test.py', capture=True)
	if result.failed and not confirm("Tests failed. Continue anyway?"):
		abort("Aborting at user request.")

def commit():
	local("git add && git commit")

def push():
	local("git push")

def prepare_deploy():
	test()
	commit()
	push()