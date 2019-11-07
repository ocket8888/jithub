"""
This module deals with configuration management for JitHub.
"""

from configparser import ConfigParser
from os import mkdir, path

_DEFAULT_DIR = "~/.jithub"
_DEFAULT_PATH = f"{_DEFAULT_DIR}/jithub.config"

class Config(ConfigParser):
	"""
	Stores configuration information for JitHub.
	"""
	_repository: str

	def __init__(self, repo:str = None, directory:str = ""):
		self._repository = repo if repo else None
		self.directory = directory if directory else _DEFAULT_DIR
		super().__init__()

	@property
	def repository(self) -> str:
		if not self._repository:
			if "GitHub" in self and "repository" in self["GitHub"]:
				self._repository = self["GitHub"]["repository"]
			else:
				self._repository = "ocket8888/jithub"
		return self._repository


def mkConfig(repo:str) -> Config:
	c = Config(repo)
	c["GitHub"] = {
		"project": "https://github.com/ocket8888/jithub"
	}
	c["JIRA"] = {
		"url": "https://jira-instance.jira.com",
		"board": "myboard"
	}
	c["Other"] = {
		"database": path.join(_DEFAULT_DIR, "jithub.db")
	}

	try:
		mkdir(path.expanduser(_DEFAULT_DIR))
	except FileExistsError:
		pass

	with open(path.expanduser(_DEFAULT_PATH), 'w+') as f:
		f.write(c)

	return c

def loadConfig(p:str, repo:str) -> Config:
	if p is None:
		p = path.expanduser(_DEFAULT_PATH)
		if not path.exists(p):
			return mkConfig(repo)
		c = Config(repo)
		c.read(p)
		return c

	p = path.expanduser(p)
	c = Config(repo)
	c.read(p)

	return c
