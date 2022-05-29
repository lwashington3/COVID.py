from requests import get
from .county_tools import *


def scrape_overall_data(db, add_each_entry=False):
	response = get(get_overall_data_link()).content


def scrape_gender_data(db):
	pass


def scrape_age_race_data(db):
	pass


def scrape_illinois_vaccine_data(db):
	pass


def scrape_illinois_vaccine_administration(db):
	pass

