from ._classes import *
from .county_tools import *
from datetime import date, timedelta as td
from json import loads
from requests import get
from mysql.connector.connection_cext import CMySQLConnection


def get_dates(day=None) -> tuple[date, str]:
	if day is None:
		day = date.today()
	return day, date_to_sql(day)


def scrape_overall_data(db:CMySQLConnection, add_each_entry=False):
	response = get(get_overall_data_link()).content
	data = OverallData.from_json(loads(response))
	cursor = db.cursor(buffered=True)
	sql_format = "INSERT INTO covid.Overall VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
	today, sql_today = get_dates()

	if add_each_entry:
		cursor.executemany(sql_format, [testing_result.value_tuple() for testing_result in data.state_testing_results])
	else:
		cursor.execute(f"SELECT COUNT(*) FROM covid.Overall WHERE date = '{sql_today}'")
		if cursor.fetchone()[0]:
			return

		row = data[today]
		if row is None:
			return
		cursor.execute(sql_format, row.value_tuple())
	db.commit()


def scrape_gender_data(db:CMySQLConnection, county=County.Illinois):
	if not isinstance(county, County):
		raise ValueError(f"The given county when scraping the gender_data needs to be from the County Enum, not {county.__class__.__name__}")
	response = get(get_age_race_link()).content
	data = Root.from_json(loads(response))
	county_data = data[county.value]
	cursor = db.cursor(buffered=True)
	today, sql_today = get_dates()
	genders = county_data.demographics.genders

	for table_name in ("Confirmed_Cases", "Tested", "Deaths"):
		sql_format = f"INSERT INTO covid_gender.{table_name} VALUES(%s,%s,%s,%s,%s)"
		cursor.execute(f"SELECT COUNT(*) FROM covid_gender.{table_name} WHERE date = '{sql_today}'")
		if cursor.fetchone()[0]:
			continue

		dct = {gender.description: getattr(gender, table_name.lower()) for gender in genders}
		female = dct["Female"]
		male = dct["Male"]
		unknown = dct["Unknown/Left Blank"]
		total = female + male + unknown
		lst = [sql_today, female, male, unknown, total]
		cursor.execute(sql_format, lst)
	db.commit()


def scrape_age_race_data(db:CMySQLConnection, county=County.Illinois):
	if not isinstance(county, County):
		raise ValueError(f"The given county when scraping the age_race_data needs to be from the County Enum, not {county.__class__.__name__}")
	response = get(get_age_race_link()).content
	data = Root.from_json(loads(response))
	county_data = data[county.value]
	cursor = db.cursor(buffered=True)
	today, sql_today = get_dates()

	for table_name in ("Confirmed_Cases", "Tested", "Deaths"):
		sql_format = f"INSERT INTO covid_age_race.{table_name} VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
		cursor.execute(f"SELECT COUNT(*) FROM covid_age_race.{table_name} WHERE date = '{sql_today}'")
		if cursor.fetchone()[0]:
			continue

		lst = []
		for age_group in county_data.demographics.ages:
			full = [sql_today]
			full.extend(age_group.value_tuple(table_name.lower()))
			lst.append(full)

		# region Create total row
		totals = [sql_today, "Total"]
		i = 0
		for total_age_group in zip(*lst):
			while i < 2:  # Ignores the date and age_group
				i += 1
				continue

			totals.append(sum(total_age_group))
		lst.append(totals)
		# endregion

		cursor.executemany(sql_format, lst)
	db.commit()


def scrape_illinois_vaccine_data(db:CMySQLConnection):
	cursor = db.cursor(buffered=True)
	response = get(get_vaccine_details_link()).content
	data = StateWideVaccine.from_json(loads(response))

	cursor.execute(f"SELECT date FROM covid_vaccine.Illinois ORDER BY date DESC")
	last_upload = cursor.fetchone()
	if last_upload is not None and not len(last_upload):
		return

	last_upload = last_upload[0] if last_upload is not None else None
	if last_upload != data.report_date:
		illinoise = ("%s,"*32).strip(",")
		sql_format = f"INSERT INTO covid_vaccine.Illinois VALUES(%s,%s,%s,%s,{illinoise})"
		lst = [date_to_sql(data.report_date)]
		lst.extend(data.value_tuple())
		cursor.execute(sql_format, lst)

	db.commit()


def scrape_illinois_vaccine_administration(db:CMySQLConnection, counties=(County.Illinois, County.Chicago)):
	cursor = db.cursor(buffered=True)
	for county in counties:
		response = get(county_to_link(get_vaccine_administration_link(), county)).content
		administrations = Administration.from_json(loads(response))
		today, sql_today = get_dates()
		yesterday = today - td(days=1)

		if administrations.current_vaccine_administration is not None and administrations.current_vaccine_administration.report_date == yesterday:
			administration = administrations.current_vaccine_administration
		else:
			administration = administrations[-1]

		cursor.execute(f"SELECT date FROM covid_vaccine.{county.value}_administration ORDER BY date DESC")
		lst = cursor.fetchone()
		up_to_date = True
		if lst is None:
			up_to_date = False
		elif not len(lst):
			up_to_date = False
		elif lst[0] != administration.report_date:
			up_to_date = False
		if up_to_date:
			continue

		sql_format = f"INSERT INTO covid_vaccine.{county.value}_administration VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
		lst = [date_to_sql(administration.report_date)]
		lst.extend(administration.value_tuple())
		cursor.execute(sql_format, lst)
	db.commit()
