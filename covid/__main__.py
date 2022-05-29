from .scrape import scrape_overall_data, scrape_gender_data, scrape_age_race_data, scrape_illinois_vaccine_data, scrape_illinois_vaccine_administration
import mysql.connector as sql
from os import getenv
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


def main(db):
	threads = [Thread(target=func, args=(db)) for func in [scrape_overall, scrape_gender, age_race, illinois_vaccine, illinois_administration]]
	for thread in threads:
		thread.start()
	for thread in threads:
		thread.join()


if __name__ == "__main__":
	db = sql.connect(hostname="localhost", user="covidbot", password=getenv("COVID_DB_PASSWORD"))
	main(db)
