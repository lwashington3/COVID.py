from os import getenv
from dotenv import load_dotenv
import mysql.connector as sql


def create(db):
	cursor = db.cursor()
	cursor.execute("CREATE DATABASE covid")
	cursor.execute("CREATE DATABASE covid_gender")
	cursor.execute("CREATE DATABASE covid_age_race")
	cursor.execute("CREATE DATABASE covid_vaccine")

	cursor.execute("""CREATE TABLE covid.Overall(
		date DATE NOT NULL UNIQUE PRIMARY KEY,
		total_tested INT NOT NULL,
		confirmed_cases INT NOT NULL,
		deaths INT NOT NULL,
		change_in_total_tested INT NOT NULL,
		change_in_confirmed_cases INT NOT NULL,
		change_in_deaths INT NOT NULL,
		confirmed_7_day_rolling_average DECIMAL(10, 3) NOT NULL,
		deaths_7_day_rolling_average DECIMAL(7, 3) NOT NULL
	)""")

	for table_name in ("Confirmed_Cases", "Tested", "Deaths"):
		cursor.execute(f"""CREATE TABLE covid_gender.{table_name}(
			date DATE NOT NULL UNIQUE PRIMARY KEY,
			female INT NOT NULL,
			male INT NOT NULL,
			unknown INT NOT NULL,
			total INT NOT NULL 
		)""")

	# nh_pi is Native Hawaiian or Other Pacific Islander
	for table_name in ("Confirmed_Cases", "Tested", "Deaths"):
		cursor.execute(f"""CREATE TABLE covid_age_race.{table_name}(
			date DATE NOT NULL,
			age_group VARCHAR(7) NOT NULL
			american_indian INT NOT NULL,
			nh_pi INT NOT NULL,
			hispanic INT NOT NULL,
			asian INT NOT NULL,
			other INT NOT NULL,
			left_blank INT NOT NULL,
			black INT NOT NULL,
			white INT NOT NULL,
			total INT,
			PRIMARY KEY (date, age_group)
		)""")

	for county in ("Illinois", "Chicago"):
		cursor.execute(f"""CREATE TABLE covid_vaccine.{county}_administration(
			date DATE NOT NULL UNIQUE PRIMARY KEY,
			administered_vaccine_doses INT NOT NULL,
			count_7_day_rolling_average INT NOT NULL,
			population INT NOT NULL,
			population_one_dose INT NOT NULL,
			population_one_dose_percentage DECIMAL(4, 2) NOT NULL,
			population_fully_vaccinated INT NOT NULL,
			population_fully_vaccinated_percentage DECIMAL(4, 2) NOT NULL,
			booster_doses INT NOT NULL,
			allocated_doses INT NOT NULL,
			inventory_report_date DATE NOT NULL,
			lhd_reported_inventory INT NOT NULL,
			community_reported_inventory INT NOT NULL,
			total_reported_inventory INT NOT NULL
		)""")

	cursor.execute("""CREATE TABLE covid_vaccine.Illinois(
		date DATE NOT NULL UNIQUE PRIMARY KEY,
		total_doses INT NOT NULL,
		total_administered_doses INT NOT NULL,
		weekly_rolling_average INT NOT NULL,
		illinoisans_fully_vaccinated_5_up INT NOT NULL,
		illinoisans_fully_vaccinated_5_up_percentage DECIMAL(3, 1) NOT NULL,
		illinoisans_at_least_one_dose_5_up INT NOT NULL,
		illinoisans_at_least_one_dose_5_up DECIMAL(3, 1) NOT NULL,
		illinoisans_fully_vaccinated_12_up INT NOT NULL,
		illinoisans_fully_vaccinated_12_up_percentage DECIMAL(3, 1) NOT NULL,
		illinoisans_at_least_one_dose_12_up INT NOT NULL,
		illinoisans_at_least_one_does_12_up_percentage DECIMAL(3, 1) NOT NULL,
		illinoisans_fully_vaccinated_18_up INT NOT NULL,
		illinoisans_fully_vaccinated_18_up_percentage DECIMAL(3, 1) NOT NULL,
		illinoisans_at_least_one_dose_18_up INT NOT NULL,
		illinoisans_at_least_one_does_18_up_percentage DECIMAL(3, 1) NOT NULL,
		illinoisans_fully_vaccinated_65_up INT NOT NULL,
		illinoisans_fully_vaccinated_65_up_percentage DECIMAL(3, 1) NOT NULL,
		illinoisans_at_least_one_dose_65_up INT NOT NULL,
		illinoisans_at_least_one_does_65_up_percentage DECIMAL(3, 1) NOT NULL,
		illinois_fully_vaccinated_5_up INT NOT NULL,          
		illinois_fully_vaccinated_5_up_percentage DECIMAL(3, 1) NOT NULL,
		illinois_at_least_one_dose_5_up INT NOT NULL,          
		illinois_at_least_one_dose_5_up DECIMAL(3, 1) NOT NULL,
		illinois_fully_vaccinated_12_up INT NOT NULL,          
		illinois_fully_vaccinated_12_up_percentage DECIMAL(3, 1) NOT NULL,
		illinois_at_least_one_dose_12_up INT NOT NULL,          
		illinois_at_least_one_does_12_up_percentage DECIMAL(3, 1) NOT NULL,
		illinois_fully_vaccinated_18_up INT NOT NULL,          
		illinois_fully_vaccinated_18_up_percentage DECIMAL(3, 1) NOT NULL,
		illinois_at_least_one_dose_18_up INT NOT NULL,          
		illinois_at_least_one_does_18_up_percentage DECIMAL(3, 1) NOT NULL,
		illinois_fully_vaccinated_65_up INT NOT NULL,          
		illinois_fully_vaccinated_65_up_percentage DECIMAL(3, 1) NOT NULL,
		illinois_at_least_one_dose_65_up INT NOT NULL,          
		illinois_at_least_one_does_65_up_percentage DECIMAL(3, 1) NOT NULL,
	)""")

	db.commit()


if __name__ == "__main__":
	load_dotenv()
	db = sql.connect(host="localhost",
					 user="covidbot",
					 password=getenv("COVID_DB_PASSWORD"))
	create(db)
