"""
"""
import sys

from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from json import dumps
from urllib.error import HTTPError

from . import cfg, github, database

__version__ = "0.0.1"

def _main() -> int:
	parser = ArgumentParser(prog="jithub", formatter_class=ArgumentDefaultsHelpFormatter, epilog="The first time jithub is run, the -i/--init option should be used to perform initial setup operations. After that, subsequent runs (without -i/--init) will act as a webhook listener to continually update as GitHub events occur.")
	parser.add_argument("-v", "--version", action="version", version=f"%(prog)s {__version__}")
	parser.add_argument("-k", "--insecure", action="store_true", help="When passed, causes jithub to not verify the certificate chain of SSL certificates given by GitHub AND JIRA.")
	parser.add_argument("--config", type=str, default=None, help="Specify a relative or absolute path to a configuration file")
	parser.add_argument("--gh-user", type=str, help="Specify a GitHub user as whom to authenticate with GitHub")
	parser.add_argument("--gh-passwd", type=str, help="Specify a password to use when authenticating with GitHub")
	parser.add_argument("--repository", type=str, help="Specify a GitHub repository to sync")
	parser.add_argument("--database", type=str, help="Give a relative or absolute path to a sqlite database to use")
	parser.add_argument("-i", "--init", action="store_true", help="Initialize the GitHub/JIRA linking rather than pick up where a previous link left off.")
	args = parser.parse_args()

	if args.version:
		print(__version__)
		return 0

	try:
		config = cfg.loadConfig(args.config, args.repository)
	except OSError as e:
		print("Failed to read configuration:", e, file=sys.stderr)
		return e.errno

	try:
		gh = github.createHandle(config, args.gh_user, args.gh_passwd, args.insecure)
	except OSError as e:
		print("Failed to create GitHub Handle:", e, file=sys.stderr)
		return e.errno

	db = database.getDB(args.database, config)

	try:
		for issue in gh.getIssues():
			print(issue)
			db.insertIssue(issue)
	except ValueError as e:
		print("GitHub returned bad JSON payload: e", file=sys.stderr)
		return 1
	except ConnectionError as e:
		print("Connection Error:", e, file=sys.stderr)
		return e.errno
	except HTTPError as e:
		print("HTTPError:", e)
		return 1

	db.close()

	return 0

def main() -> int:
	try:
		return _main()
	except KeyboardInterrupt:
		return 2


if __name__ == '__main__':
	sys.exit(main())
