from getpass import getpass

class Handle():
	pass

class GHException(Exception):
	pass

def _createHandleFromUserAndPasswd(u:str, p:str) -> Handle:
	while not u:
		u = input("Please enter GitHub username:")
	while not p:
		p = getpass(prompt="Please enter GitHub password:")


def createHandle(c:dict, user:str, passwd:str) -> Handle:
	if "GitHub" not in c:
		return _createHandleFromUserAndPasswd(user, passwd)
