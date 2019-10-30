"""
"""

from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from os.path import expanduser
import sys

from . import cfg, github

__version__ = "0.0.1"

def main() -> int:
	parser = ArgumentParser(prog="jithub", formatter_class=ArgumentDefaultsHelpFormatter)
	parser.add_argument("-v", "--version", action="store_true")
	parser.add_argument("--config", type=str, default=expanduser(cfg._DEFAULT_CONFIG), help="Specify a relative or absolute path to a configuration file")
	parser.add_argument("--gh-user", type=str, help="Specify a GitHub user as whom to authenticate with GitHub")
	parser.add_argument("--gh-passwd", type=str, help="Specify a password to use when authenticating with GitHub")
	args = parser.parse_args()

	if args.version:
		print(__version__)
		sys.exit(0)

	try:
		config = cfg.loadConfig()
	except OSError as e:
		print("Failed to read configuration:", e, file=sys.stderr)
		sys.exit(e.errno)

	try:
		gh = github.createHandle(config, args.gh_user, args.gh_passwd)
	except OSError as e:
		print("Failed to authenticate with GitHub:", e, file=sys.stderr)
		sys.exit(e.errno)

	return 0


if __name__ == '__main__':
	sys.exit(main())
