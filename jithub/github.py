import ssl

from base64 import encodebytes
from datetime import datetime
from getpass import getpass
from json import loads
from sys import stdout
from urllib.request import Request, urlopen

class Issue():

	def __init__(self, raw: dict):
		self.ID = raw.get("id", -1)
		self.number = raw.get("number", -1)
		self.title = raw.get("title", "")
		self.commentsURL = raw.get("comments_url")
		self.state = raw.get("state")
		self.commentCount = raw.get("comments", -1)
		self.isPR = "pull_request" in raw
		self.updated = datetime.strptime(raw["updated_at"], "%Y-%m-%dT%H:%M:%SZ") if "updated_at" in raw else None

	def __repr__(self) -> str:
		return f"Issue('{{\"id\":{self.ID}, \"number\":{self.number}, \"title\":\"{self.title}\", \"comments_url\":\"{self.commentsURL}\", \"state\":\"{self.state}\"}}"

	def __str__(self) -> str:
		return f"#{self.number} {self.title} - {self.state} (last updated at {self.updated})"

class Handle():

	UAString = "Jithub/0.0.1"
	GH_API_MIME = "application/vnd.github.v3+json"

	def __init__(self, auth:str, insecure:bool, repo:str):
		self.auth = auth.replace("\n", "")
		self.insecure = insecure
		self.repository = repo

	def headers(self) -> dict:
		return {
			"Authorization": self.auth,
			"User-Agent": self.UAString,
			"Accept": self.GH_API_MIME
		}

	def get(self, path:str) -> bytes:
		ctx = ssl._create_unverified_context() if self.insecure else None
		linkURL = f"https://api.github.com/{path}"

		while linkURL:
			req = Request(linkURL, headers=self.headers())
			with urlopen(req, context=ctx) as url:
				inf = url.info()
				if "Link" in inf:
					for link in inf["Link"].split(","):
						l, *params = link.lstrip().rstrip().split(";")
						for p in params:
							k, v = p.split("=")
							if k.lstrip().rstrip() == "rel" and v.lstrip('" ').rstrip(' "') == "next":
								linkURL = l.lstrip("<").rstrip(">")
								break
						else:
							continue
						break
					else:
						linkURL = None
				else:
					linkURL = None

				yield url.read()

	def getIssues(self) -> list:
		for page in self.get(f"repos/{self.repository}/issues?state=all&sort=updated"):
			for i in loads(page, object_hook=Issue):
				if not i.isPR:
					yield i

class GHException(Exception):
	pass

def _createHandleFromUserAndPasswd(u:str, p:str, insecure:bool, repo:str) -> Handle:
	while not u:
		u = input("Please enter GitHub username:")
	while not p:
		p = getpass(prompt="Please enter GitHub password:", stream=stdout)

	try:
		return Handle("Basic " + encodebytes(f"{u}:{p}".encode()).decode(), insecure, repo)
	except ValueError as e:
		raise GHException from e


def createHandle(c:dict, user:str, passwd:str, insecure:bool) -> Handle:
	if "GitHub" not in c:
		return _createHandleFromUserAndPasswd(user, passwd, insecure, c.repository)

	gh = c["GitHub"]
	if "token" not in gh:
		return _createHandleFromUserAndPasswd(gh.get("user", ""), gh.get("password", ""), insecure, c.repository)

	return Handle(f"token {gh['token']}", insecure, c.repository)
