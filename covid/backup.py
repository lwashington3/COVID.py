def backup(db:CMySQLConnection, backup_dir:str=None):
	cursor = db.cursor(buffered=True)
	if backup_dir is None:
		from os.path import join, expanduser
		backup_dir = join(expanduser('~'), ".covid/backup")

	from os.path import isdir
	if not isdir(backup_dir):
		from os import mkdir
		mkdir(backup_dir)

	for database in ("covid", "covid_gender", "covid_age_race", "covid_vaccine"):
		cursor.execute(f"BACKUP DATABASE {database} TO DISK = '{backup_dir}\\{database}.bak' WITH DIFFERENTIAL")
