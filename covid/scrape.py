from ._classes import OverallData
from .county_tools import *
from datetime import date
from json import loads
from requests import get


def scrape_overall_data(db, add_each_entry=False):
	response = get(get_overall_data_link()).content
	data = OverallData.from_json(loads(response))
	cursor = db.cursor(buffered=True)  # TODO: Check if buffered is true or false
	sql_format = "INSERT INTO covid.OVERALL VALUES('%s',%d,%d,%d,%d,%d,%d,%f,%f,%f)"
	if add_each_entry:
		cursor.executemany(sql_format, [testing_result.value_tuple() for testing_result in data.state_testing_results])
	else:
		today = date.today()
		row = data.state_testing_results[today]
		if row is None:
			raise ValueError(f"Cannot find the state testing results for today, {today:%B %d, %Y}")
		cursor.execute(sql_format, row.value_tuple())
	db.commit()


def scrape_gender_data(db, county="Illinois"):
	response = get(get_age_race_link()).content
	data = Root.from_json(loads(response))
	county = data[county]
	cursor = db.cursor(buffered=True)
	today = date.today()

	for table_name in ("Confirmed_Cases", "Tested", "Deaths"):  # covid_gender
		cursor.execute(f"SELECT COUNT(*) FROM covid_gender.{table_name} WHERE date = ''")



def scrape_age_race_data(db):
	pass


def scrape_illinois_vaccine_data(db):
	pass


def scrape_illinois_vaccine_administration(db):
	pass

