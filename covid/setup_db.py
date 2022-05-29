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




if __name__ == "__main__":
	load_dotenv()
	db = sql.connect(host="localhost",
					 user="covidbot",
					 password=getenv("COVID_DB_PASSWORD"))
	create(db)
