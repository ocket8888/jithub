"""
This module deals with configuration management for JitHub.
"""

from configparser import ConfigParser
from os.path import exists, expanduser

class Config(ConfigParser):
	"""
	Stores configuration information for JitHub.
	"""
	pass

_DEFAULT_PATH = "~/.jithub/jithub.config"

def mkConfig() -> Config:
	c = Config()
	c["GitHub"] = {
		"project": "https://github.com/ocket8888/jithub"
	}
	c["JIRA"] = {
		"url": "https://jira-instance.jira.com",
		"board": "myboard"
	}

	with open(expanduser(_DEFAULT_PATH), 'w') as f:
		f.write(c)

	return c

def loadCfg(path:str) -> Config:
	if path is None:
		path = expanduser(_DEFAULT_PATH)
		if exists(path):
			return mkConfig()

	path = expanduser(path)
	with open(path) as f:
		pass

	return Config()
