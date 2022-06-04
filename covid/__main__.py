from .scrape import scrape_overall_data, scrape_gender_data, scrape_age_race_data, scrape_illinois_vaccine_data, scrape_illinois_vaccine_administration
from argparse import ArgumentParser
import mysql.connector as sql
from mysql.connector.connection_cext import CMySQLConnection
from os import getenv
from sys import argv
from threading import Thread


def scrape_overall(db:CMySQLConnection):
	print("Scraping Overall Data")
	scrape_overall_data(db)
	print("Finished scraping Overall Data")


def scrape_gender(db:CMySQLConnection):
	print("Scraping Gender Data")
	scrape_gender_data(db)
	print("Finished scraping Gender Data")


def age_race(db:CMySQLConnection):
	print("Scraping Age/Race Data")
	scrape_age_race_data(db)
	print("Finished scraping Age/Race Data")


def illinois_vaccine(db:CMySQLConnection):
	print("Scraping Statewide Vaccine Data")
	scrape_illinois_vaccine_data(db)
	print("Finished scraping Statewide Vaccine Data")


def illinois_administration(db:CMySQLConnection):
	print("Scraping Vaccine Administration Data")
	scrape_illinois_vaccine_administration(db)
	print("Finished scraping Vaccine Administration Data")


def main_scrape(db:CMySQLConnection):
	threads = [Thread(target=func, args=[db]) for func in [scrape_overall]] #, scrape_gender, age_race, illinois_vaccine, illinois_administration]]
	for thread in threads:
		thread.start()
	for thread in threads:
		thread.join()


def _add_common_options(parser):
	parser.add_argument("-u", "--username", help="The username for the database", required=False)
	parser.add_argument("-p", "--password", help="The password for the database", required=False)


def _create_setup_parser(parser_factory):
	parser = parser_factory("setup", help="Create the databases to hold the COVID info.")
	_add_common_options(parser)


def _create_scrape_parser(parser_factory):
	parser = parser_factory("scrape", help="Daily scrape.")
	_add_common_options(parser)


def _create_backup_parser(parser_factory):
	parser = parser_factory("backup", help="Backup the database to a file.")
	_add_common_options(parser)
	parser.add_argument("-d", "--directory", help="The directory to save the backup.")


def create_argument_parser():
	parser = ArgumentParser(prog="COVID.py")
	subparsers = parser.add_subparsers()
	subparsers.dest = 'command'
	subparsers.required = False
	_create_scrape_parser(subparsers.add_parser)
	_create_setup_parser(subparsers.add_parser)
	_create_backup_parser(subparsers.add_parser)
	return parser


def main(args):
	parser = create_argument_parser()
	arguments = parser.parse_args(args)
	possible_commands = ("setup", "scrape", "backup")
	if arguments.command not in possible_commands:
		print(f"You gave an unknown command, try again. The command must be one of the following: {possible_commands}")
		return

	username = arguments.username if arguments.username is not None else "covidbot"
	password = arguments.password if arguments.password is not None else getenv("COVID_DB_PASSWORD")
	db = sql.connect(host="localhost",
					 user=username,
					 password=password)

	if arguments.command == "setup":
		from .setup_db import create
		create(db, "covidbot")
	elif arguments.command == "scrape":
		main_scrape(db)
	elif arguments.command == "backup":
		from .backup import backup
		backup(db, backup_dir=arguments.directory)


if __name__ == "__main__":
	main(argv[1:])
