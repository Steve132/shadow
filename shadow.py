
class Remote(object):	#represents a repository object that can be updated remotely
	pass

class LocalRemote(object):	#the current 'remote' backup inside the working copy
	pass

class Target(object):	#a file, folder, or regular expression target
	pass


def cmdfunction(funcobj): #make the funcobject visible as a command-line function...display helpstring and 
	funcobj.is_cmdfunction=True
	return funcobj 

@cmdfunction
def daemon():
	"""Run shadow as a server daemon listening for remote commits

	"""
	pass

@cmdfunction
def archive():
	"""Shadow working copy of target

	"""
	pass

@cmdfunction
def unarchive():
	"""Unshadow working copy of target

	"""
	pass

@cmdfunction
def update():
	"""Download revisions of target from the server if they exist

	"""
	pass

@cmdfunction
def commit(remote=LocalRemote()):
	"""Commit changes to the working copy to a backup

	"""
	pass

@cmdfunction
def revert(remote=LocalRemote()):
	"""Delete changes made to working copy, 

	"""
	pass

@cmdfunction
def ignore():
	"""Ignore a target

	"""
	pass #use tag system for this

@cmdfunction
def tag():
	"""Assign a tag to a target
	
	"""
	pass

@cmdfunction
def ls(remote=LocalRemote()):
	"""View remote ls

	"""
	pass

@cmdfunction
def delete():
	"""Delete target

	"""
	pass

@cmdfunction
def help(function=None):
	"""Get help about shadow's functionality

	"""
	global commands
	if(not function):
		function='help'

	if(function=='help'):
		keylen=max([len(v[0]) for v in commands])+2
		for f in sorted(commands):
			print '\t'+f[0]+':'+' '*(keylen-len(f[0]))+f[1].__doc__.splitlines()[0]
	elif(function in commands):
		f=commands[function][0]
		print f[0]
		print f[1].__doc__
	else:
		print "Function '"+function+"' not recognized as being a valid command"
	return -1


import sys

commands={(k,v) for k,v in globals().iteritems() if hasattr(v,'is_cmdfunction')}
	

if __name__=='__main__':
	if(len(sys.argv) > 1):
		fname=sys.argv[1]
	else:
		fname='help'
	if(fname not in globals()):
		fname='help'
	
	globals()[fname]() #todo, argument parsing
 
		
		
	




