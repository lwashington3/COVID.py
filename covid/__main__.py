from .scrape import scrape_overall_data, scrape_gender_data, scrape_age_race_data, scrape_illinois_vaccine_data, scrape_illinois_vaccine_administration
from argparse import ArgumentParser
import mysql.connector as sql
from os import getenv
from sys import argv
from threading import Thread


def scrape_overall(db):
	print("Scraping Overall Data")
	scrape_overall_data(db)
	print("Finished scraping Overall Data")


def scrape_gender(db):
	print("Scraping Gender Data")
	scrape_gender_data(db)
	print("Finished scraping Gender Data")


def age_race(db):
	print("Scraping Age/Race Data")
	scrape_age_race_data(db)
	print("Finished scraping Age/Race Data")


def illinois_vaccine(db):
	print("Scraping Statewide Vaccine Data")
	scrape_illinois_vaccine_data(db)
	print("Finished scraping Statewide Vaccine Data")


def illinois_administration(db):
	print("Scraping Vaccine Administration Data")
	scrape_illinois_vaccine_administration(db)
	print("Finished scraping Vaccine Administration Data")


def main_scrape(db):
	threads = [Thread(target=func, args=(db)) for func in [scrape_overall, scrape_gender, age_race, illinois_vaccine, illinois_administration]]
	for thread in threads:
		thread.start()
	for thread in threads:
		thread.join()


def _create_setup_parser(parser_factory):
	parser = parser_factory("setup", help="Create the databases to hold the COVID info.")
	_add_common_options(parser)


def _create_scrape_parser(parser_factory):
	parser = parser_factory("scrape", help="Daily scrape.")
	_add_common_options(parser)


def _add_common_options(parser):
	parser.add_argument("-u", "--username", help="The username for the database")
	parser.add_argument("-p", "--password", help="The password for the database")


def create_argument_parser():
	parser = ArgumentParser(prog="COVID.py")
	subparsers = parser.add_subparsers()
	subparsers.dest = 'command'
	subparsers.required = False
	_create_scrape_parser(subparsers.add_parser)
	_create_setup_parser(subparsers.add_parser)
	return parser


def main(args):
	parser = create_argument_parser()
	arguments = parser.parse_args(args)
	if arguments.command not in ("setup", "scrape"):
		print("You gave an unknown command, try again.")
		return

	username = arguments.username if arguments.username is not None else "covidbot"
	password = arguments.password if arguments.password is not None else getenv("COVID_DB_PASSWORD")
	db = sql.connect(host="localhost",
					 user=username,
					 password=password)

	if arguments.command == "setup":
		from .setup_db import create
		create(db)
	elif arguments.command == "scrape":
		main_scrape(db)


if __name__ == "__main__":
	db = sql.connect(hostname="localhost", user="covidbot", password=getenv("COVID_DB_PASSWORD"))
	main(db)
