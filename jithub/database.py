import sqlite3

from os import path

_CREATE_TABLES_QUERY = '''
CREATE TABLE issues (
	gh_id INTEGER PRIMARY KEY,
	jira_id INTEGER NOT NULL,
	updated TEXT,
	comment_count INTEGER,
	state TEXT,
	gh_number INTEGER,
	title TEXT
)
'''

_INSERT_ISSUE_QUERY = '''
INSERT INTO issues VALUES (
	?,
	1,
	?,
	?,
	?,
	?,
	?
)
'''

class Cursor():
	"""
	A wrapper around sqlite3.Cursor that provides context management.
	"""

	cursor: sqlite3.Cursor

	def __init__(self, cur:sqlite3.Cursor):
		self.cursor = cur

	def __enter__(self):
		return self

	def __exit__(self, exc_type, exc_value, traceback):
		self.close()

	def close(self):
		return self.cursor.close()

	def execute(self, *args, **kwargs) -> object:
		return self.cursor.execute(*args, **kwargs)

	def fetchall(self) -> list:
		return self.cursor.fetchall()

	def fetchone(self) -> sqlite3.Row:
		return self.cursor.fetchone()

	def fetchmany(self, *args, **kwargs) -> list:
		return self.cursor.fetchmany(*args, **kwargs)

	@property
	def rowcount(self) -> int:
		return self.cursor.rowcount

	@property
	def arraysize(self) -> int:
		return self.cursor.arraysize

	@arraysize.setter
	def arraysize(self, val: int):
		self.cursor.arraysize = val

	@property
	def connection(self) -> sqlite3.Connection:
		return self.cursor.connection


class DB():

	db: sqlite3.Connection

	def __init__(self, dbPath:str):
		self.db = sqlite3.connect(dbPath)

	def execute(self, *args, **kwargs) -> object:
		return self.db.execute(*args, **kwargs)

	def commit(self):
		return self.db.commit()

	def cursor(self):
		return Cursor(self.db.cursor())

	def close(self):
		return self.db.close()

	def insertIssue(self, issue:object):
		args = (issue.ID, issue.updated, issue.commentCount, issue.state, issue.number, issue.title)
		with self.cursor() as cur:
			cur.execute(_INSERT_ISSUE_QUERY, args)
		self.commit()

def getDB(dbPath: str, c: dict) -> DB:
	if dbPath:
		return sqlite3.connect(dbPath)
	if "Other" in c and "database" in c["Other"]:
		return DB(c["Other"]["database"])

	dbPath = path.join(path.expanduser(c.directory), "jithub.db")
	if path.exists(dbPath):
		return DB(dbPath)
	db = DB(dbPath)
	seed(db)
	return db

def seed(db:DB):
	cur = db.cursor()

	cur.execute(_CREATE_TABLES_QUERY)

	cur.close()
	db.commit()
