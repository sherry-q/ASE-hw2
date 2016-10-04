# reference tutorial: http://docs.fabfile.org/en/1.12/tutorial.html

from __future__ import with_statement
from fabric.api import *
from fabric.contrib.console import confirm
import os

# run unit tests
def test():
	with settings(warn_only=True):
		result = local('python test.py', capture=True)
	if result.failed and not confirm("Tests failed. Continue anyway?"):
		abort("Aborting at user request.")

def static_analysis():
	# ignore error from static analysis so files can be pushed to git
	try:
		local("pylint shopping_list.py >> shopping_list_static_analysis.txt")
	except:
		pass

def commit():
	local("git add -u && git commit")
	local("git add shopping_list_static_analysis.txt")

def push():
	local("git push")

def prepare_deploy():
	test()
	static_analysis()
	commit()
	push()

# start server for web app
def deploy():
    with cd(os.getcwd()):
        local("git pull")
        local("python shopping_list.py")