from datetime import date, datetime as dt


def iter_check(obj, type_name, name=None):
	if not hasattr(obj, "__iter__"):
		raise ValueError(f"{name} needs to be an iterable object, not: {obj.__class__.__name__}")
	for inner in obj:
		if not isinstance(inner, type_name):
			raise ValueError(f"Every object in the races iterable must be a {type_name.__class__.__name__} object, not: {inner.__class__.__name__}")
	return obj if isinstance(obj, list) else list(obj)


def json_to_date(json:dict|str) -> date:
	if isinstance(json, dict):
		test_date = f"{json['year']}-{json['month']}-{json['day']}"
		return dt.strptime(test_date, "%Y-%m-%d").date()
	else:
		return dt.strptime(json, "%Y-%m-%dT00:00:00").date()


def date_to_sql(day:date) -> str:
	return day.strftime("%Y-%m-%d")


class IllinoisTestingResults:
	def __init__(self, test_date, total_tested, confirmed_cases, deaths, tested_change,
				 cases_change, deaths_change, tested_7_day_rolling_avg, cases_7_day_rolling_avg, deaths_7_day_rolling_avg):
		self.test_date = test_date
		self.total_tested = total_tested
		self.confirmed_cases = confirmed_cases
		self.deaths = deaths
		self.tested_change = tested_change
		self.cases_change = cases_change
		self.deaths_change = deaths_change
		self.tested_7_day_rolling_avg = tested_7_day_rolling_avg
		self.cases_7_day_rolling_avg = cases_7_day_rolling_avg
		self.deaths_7_day_rolling_avg = deaths_7_day_rolling_avg

	@property
	def test_date(self) -> date:
		return self._test_date

	@test_date.setter
	def test_date(self, test_date:date):
		if not isinstance(test_date, date):
			raise ValueError(f"The test date must be a datetime.date object, not: {last_updated_date.__class__.__name__}")
		self._test_date = test_date

	@property
	def total_tested(self) -> int:
		return self._total_tested

	@total_tested.setter
	def total_tested(self, total_tested:int):
		if not isinstance(total_tested, int):
			total_tested = int(total_tested)
		self._total_tested = total_tested

	@property
	def confirmed_cases(self) -> int:
		return self._confirmed_cases

	@confirmed_cases.setter
	def confirmed_cases(self, confirmed_cases: int):
		if not isinstance(confirmed_cases, int):
			confirmed_cases = int(confirmed_cases)
		self._confirmed_cases = confirmed_cases

	@property
	def deaths(self) -> int:
		return self._deaths

	@deaths.setter
	def deaths(self, deaths: int):
		if not isinstance(deaths, int):
			deaths = int(deaths)
		self._deaths = deaths

	@property
	def tested_change(self) -> int:
		return self._tested_change

	@tested_change.setter
	def tested_change(self, tested_change: int):
		if not isinstance(tested_change, int):
			tested_change = int(tested_change)
		self._tested_change = tested_change

	@property
	def cases_change(self) -> int:
		return self._cases_change

	@cases_change.setter
	def cases_change(self, cases_change: int):
		if not isinstance(cases_change, int):
			cases_change = int(cases_change)
		self._cases_change = cases_change

	@property
	def deaths_change(self) -> int:
		return self._deaths_change

	@deaths_change.setter
	def deaths_change(self, deaths_change: int):
		if not isinstance(deaths_change, int):
			deaths_change = int(deaths_change)
		self._deaths_change = deaths_change

	@property
	def tested_7_day_rolling_avg(self) -> float:
		return self._tested_7_day_rolling_avg

	@tested_7_day_rolling_avg.setter
	def tested_7_day_rolling_avg(self, tested_7_day_rolling_avg: float):
		if not isinstance(tested_7_day_rolling_avg, float):
			tested_7_day_rolling_avg = float(tested_7_day_rolling_avg)
		self._tested_7_day_rolling_avg = tested_7_day_rolling_avg

	@property
	def cases_7_day_rolling_avg(self) -> float:
		return self._cases_7_day_rolling_avg

	@cases_7_day_rolling_avg.setter
	def cases_7_day_rolling_avg(self, cases_7_day_rolling_avg: float):
		if not isinstance(cases_7_day_rolling_avg, float):
			cases_7_day_rolling_avg = float(cases_7_day_rolling_avg)
		self._cases_7_day_rolling_avg = cases_7_day_rolling_avg

	@property
	def deaths_7_day_rolling_avg(self) -> float:
		return self._deaths_7_day_rolling_avg

	@deaths_7_day_rolling_avg.setter
	def deaths_7_day_rolling_avg(self, deaths_7_day_rolling_avg: float):
		if not isinstance(deaths_7_day_rolling_avg, float):
			deaths_7_day_rolling_avg = float(deaths_7_day_rolling_avg)
		self._deaths_7_day_rolling_avg = deaths_7_day_rolling_avg

	def value_tuple(self) -> tuple:
		return (self.test_date.strftime("%Y-%m-%d"), self.total_tested, self.confirmed_cases, self.deaths, self.tested_change,
				self.cases_change, self.deaths_change, self.tested_7_day_rolling_avg, self.cases_7_day_rolling_avg, self.deaths_7_day_rolling_avg)

	@classmethod
	def from_json(cls, json: dict):
		test_date = json_to_date(json["testDate"])
		total_tested = int(json["total_tested"])
		confirmed_cases = int(json["confirmed_cases"])
		deaths = int(json["deaths"])
		tested_change = int(json["tested_change"])
		cases_change = int(json["cases_change"])
		deaths_change = int(json["deaths_change"])
		tested_7_day_rolling_avg = float(json["tested_7_day_rolling_avg"])
		cases_7_day_rolling_avg = float(json["cases_7_day_rolling_avg"])
		deaths_7_day_rolling_avg = float(json["deaths_7_day_rolling_avg"])
		return cls(test_date, total_tested, confirmed_cases, deaths, tested_change, cases_change, deaths_change,
				   tested_7_day_rolling_avg, cases_7_day_rolling_avg, deaths_7_day_rolling_avg)


class OverallData:
	def __init__(self, last_updated_date:date, state_testing_results:list[IllinoisTestingResults]):
		self.last_updated_date = last_updated_date
		self.state_testing_results = state_testing_results

	def __iter__(self):
		for testing_result in self.state_testing_results:
			yield testing_result

	def __getitem__(self, item):
		if isinstance(item, int):
			return self.state_testing_results[item]
		elif isinstance(item, date):
			for testing_result in self:
				if date == testing_result.test_date:
					return testing_result
		return None

	@property
	def last_updated_date(self) -> date:
		return self._last_updated_date

	@last_updated_date.setter
	def last_updated_date(self, last_updated_date: date):
		if not isinstance(last_updated_date, date):
			raise ValueError(f"The last updated date must be a datetime.date object, not: {last_updated_date.__class__.__name__}")
		self._last_updated_date = last_updated_date

	@property
	def state_testing_results(self) -> list[IllinoisTestingResults]:
		return self._state_testing_results

	@state_testing_results.setter
	def state_testing_results(self, state_testing_results:list[IllinoisTestingResults]):
		self._state_testing_results = iter_check(state_testing_results, IllinoisTestingResults, "State testing results")

	@classmethod
	def from_json(cls, json:dict):
		last_updated_date = json_to_date(json["lastUpdatedDate"])
		state_testing_results = [IllinoisTestingResults.from_json(testing_result) for testing_result in json["state_testing_results"]]
		return cls(last_updated_date, state_testing_results)


class VaccineAdministration:
	def __init__(self, county_name, administered_count, administered_count_change, administered_count_rolling_average,
				 allocated_doses, persons_fully_vaccinated, persons_fully_vaccinated_change, persons_vaccinated_one_dose,
				 persons_vaccinated_one_dose_change, booster_dose_administered, booster_dose_administered_change,
				 report_date:date, population:int, percent_vaccinated_population, percent_vaccinated_one_dose_population,
				 longitude:float, latitude:float, lhd_reported_inventory, community_reported_inventory,
				 total_reported_inventory, inventory_report_date:date):
		self.county_name = county_name
		self.administered_count = administered_count
		self.administered_count_change = administered_count_change
		self.administered_count_rolling_average = administered_count_rolling_average
		self.allocated_doses = allocated_doses
		self.persons_fully_vaccinated = persons_fully_vaccinated
		self.persons_fully_vaccinated_change = persons_fully_vaccinated_change
		self.persons_vaccinated_one_dose = persons_vaccinated_one_dose
		self.persons_vaccinated_one_dose_change = persons_vaccinated_one_dose_change
		self.booster_dose_administered = booster_dose_administered
		self.booster_dose_administered_change = booster_dose_administered_change
		self.report_date = report_date
		self.population = population
		self.percent_vaccinated_population = percent_vaccinated_population
		self.percent_vaccinated_one_dose_population = percent_vaccinated_one_dose_population
		self.longitude = longitude
		self.latitude = latitude
		self.lhd_reported_inventory = lhd_reported_inventory
		self.community_reported_inventory = community_reported_inventory
		self.total_reported_inventory = total_reported_inventory
		self.inventory_report_date = inventory_report_date

	@property
	def report_date(self) -> date:
		return self._report_date

	@report_date.setter
	def report_date(self, report_date:date):
		if not isinstance(report_date, date):
			raise ValueError(f"The report date must be a datetime.date object, not: {report_date.__class__.__name__}")
		self._report_date = report_date

	@property
	def county_name(self) -> str:
		return self._county_name

	@county_name.setter
	def county_name(self, county_name: str):
		if not isinstance(county_name, str):
			county_name = str(county_name)
		self._county_name = county_name

	@property
	def population(self) -> int:
		return self._population

	@population.setter
	def population(self, population:int):
		if not isinstance(population, int):
			population = int(population)
		self._population = population

	@property
	def longitude(self) -> float:
		return self._longitude

	@longitude.setter
	def longitude(self, longitude:float):
		if not isinstance(longitude, float):
			longitude = float(longitude)
		self._longitude = longitude

	@property
	def latitude(self) -> float:
		return self._latitude

	@latitude.setter
	def latitude(self, latitude: float):
		if not isinstance(latitude, float):
			latitude = float(latitude)
		self._latitude = latitude

	@property
	def administered_count(self) -> int:
		return self._administered_count

	@administered_count.setter
	def administered_count(self, administered_count:int):
		if not isinstance(administered_count, int):
			administered_count = int(administered_count)
		self._administered_count = administered_count

	@property
	def administered_count_change(self) -> int:
		return self._administered_count_change

	@administered_count_change.setter
	def administered_count_change(self, administered_count_change: int):
		if not isinstance(administered_count_change, int):
			administered_count_change = int(administered_count_change)
		self._administered_count_change = administered_count_change

	@property
	def administered_count_rolling_average(self) -> int:
		return self._administered_count_rolling_average

	@administered_count_rolling_average.setter
	def administered_count_rolling_average(self, administered_count_rolling_average:int):
		if not isinstance(administered_count_rolling_average, int):
			administered_count_rolling_average = int(administered_count_rolling_average)
		self._administered_count_rolling_average = administered_count_rolling_average

	@property
	def allocated_doses(self) -> int:
		return self._allocated_doses

	@allocated_doses.setter
	def allocated_doses(self, allocated_doses:int):
		if not isinstance(allocated_doses, int):
			allocated_doses = int(allocated_doses)
		self._allocated_doses = allocated_doses

	@property
	def persons_fully_vaccinated(self) -> int:
		return self._persons_fully_vaccinated

	@persons_fully_vaccinated.setter
	def persons_fully_vaccinated(self, persons_fully_vaccinated:int):
		if not isinstance(persons_fully_vaccinated, int):
			persons_fully_vaccinated = int(persons_fully_vaccinated)
		self._persons_fully_vaccinated = persons_fully_vaccinated

	@property
	def persons_fully_vaccinated_change(self) -> int:
		return self._persons_fully_vaccinated_change

	@persons_fully_vaccinated_change.setter
	def persons_fully_vaccinated_change(self, persons_fully_vaccinated_change: int):
		if not isinstance(persons_fully_vaccinated_change, int):
			persons_fully_vaccinated_change = int(persons_fully_vaccinated_change)
		self._persons_fully_vaccinated_change = persons_fully_vaccinated_change

	@property
	def persons_vaccinated_one_dose(self) -> int:
		return self._persons_vaccinated_one_dose

	@persons_vaccinated_one_dose.setter
	def persons_vaccinated_one_dose(self, persons_vaccinated_one_dose:int):
		if not isinstance(persons_vaccinated_one_dose, int):
			persons_vaccinated_one_dose = int(persons_vaccinated_one_dose)
		self._persons_vaccinated_one_dose = persons_vaccinated_one_dose

	@property
	def persons_vaccinated_one_dose_change(self) -> int:
		return self._persons_vaccinated_one_dose_change

	@persons_vaccinated_one_dose_change.setter
	def persons_vaccinated_one_dose_change(self, persons_vaccinated_one_dose_change: int):
		if not isinstance(persons_vaccinated_one_dose_change, int):
			persons_vaccinated_one_dose_change = int(persons_vaccinated_one_dose_change)
		self._persons_vaccinated_one_dose_change = persons_vaccinated_one_dose_change

	@property
	def booster_dose_administered(self) -> int:
		return self._booster_dose_administered

	@booster_dose_administered.setter
	def booster_dose_administered(self, booster_dose_administered:int):
		if not isinstance(booster_dose_administered, int):
			booster_dose_administered = int(booster_dose_administered)
		self._booster_dose_administered = booster_dose_administered

	@property
	def booster_dose_administered_change(self) -> int:
		return self._booster_dose_administered_change

	@booster_dose_administered_change.setter
	def booster_dose_administered_change(self, booster_dose_administered_change: int):
		if not isinstance(booster_dose_administered_change, int):
			booster_dose_administered_change = int(booster_dose_administered_change)
		self._booster_dose_administered_change = booster_dose_administered_change

	@property
	def percent_vaccinated_population(self) -> float:
		return self._ercent_vaccinated_population

	@percent_vaccinated_population.setter
	def percent_vaccinated_population(self, percent_vaccinated_population:float):
		if not isinstance(percent_vaccinated_population, int):
			percent_vaccinated_population = float(percent_vaccinated_population)
		self._percent_vaccinated_population = percent_vaccinated_population

	@property
	def percent_vaccinated_one_dose_population(self) -> float:
		return self._ercent_vaccinated_one_dose_population

	@percent_vaccinated_one_dose_population.setter
	def percent_vaccinated_one_dose_population(self, percent_vaccinated_one_dose_population: float):
		if not isinstance(percent_vaccinated_one_dose_population, int):
			percent_vaccinated_one_dose_population = float(percent_vaccinated_one_dose_population)
		self._percent_vaccinated_one_dose_population = percent_vaccinated_one_dose_population

	@property
	def lhd_reported_inventory(self) -> int:
		return self._lhd_reported_inventory

	@lhd_reported_inventory.setter
	def lhd_reported_inventory(self, lhd_reported_inventory:int):
		if not isinstance(lhd_reported_inventory, int):
			lhd_reported_inventory = int(lhd_reported_inventory)
		self._lhd_reported_inventory = lhd_reported_inventory

	@property
	def community_reported_inventory(self) -> int:
		return self._community_reported_inventory

	@community_reported_inventory.setter
	def community_reported_inventory(self, community_reported_inventory:int):
		if not isinstance(community_reported_inventory, int):
			community_reported_inventory = int(community_reported_inventory)
		self._community_reported_inventory = community_reported_inventory

	@property
	def total_reported_inventory(self) -> int:
		return self._total_reported_inventory

	@total_reported_inventory.setter
	def total_reported_inventory(self, total_reported_inventory: int):
		if not isinstance(total_reported_inventory, int):
			total_reported_inventory = int(total_reported_inventory)
		self._total_reported_inventory = total_reported_inventory

	@property
	def inventory_report_date(self) -> date:
		return self._inventory_report_date

	@inventory_report_date.setter
	def inventory_report_date(self, inventory_report_date: date):
		if not isinstance(inventory_report_date, date):
			raise ValueError(f"The inventory report date must be a datetime.date object, not: {inventory_report_date.__class__.__name__}")
		self._inventory_report_date = inventory_report_date

	def value_tuple(self) -> tuple:
		return (self.administered_count, self.administered_count_rolling_average, self.population,
				self.persons_vaccinated_one_dose, self.percent_vaccinated_one_dose_population,
				self.persons_fully_vaccinated, self.percent_vaccinated_population, self.booster_dose_administered,
				self.allocated_doses, date_to_sql(self.inventory_report_date), self.lhd_reported_inventory,
				self.community_reported_inventory, self.total_reported_inventory)

	@classmethod
	def from_json(cls, json:dict):
		return cls(county_name=json["CountyName"], administered_count=json["AdministeredCount"],
				   administered_count_change=json["AdministeredCountChange"],
				   administered_count_rolling_average=json["AdministeredCountRollAvg"],
				   allocated_doses=json["AllocatedDoses"], persons_fully_vaccinated=json["PersonsFullyVaccinated"],
				   persons_fully_vaccinated_change=json["PersonsFullyVaccinatedChange"],
				   persons_vaccinated_one_dose=json["PersonsVaccinatedOneDose"],
				   persons_vaccinated_one_dose_change=json["PersonsVaccinatedOneDoseChange"],
				   booster_dose_administered=json["BoosterDoseAdministered"],
				   booster_dose_administered_change=json["BoosterDoseAdministeredChange"],
				   report_date=json["Report_Date"], population=json["Population"],
				   percent_vaccinated_population=json["PctVaccinatedPopulation"],
				   percent_vaccinated_one_dose_population=["PctVaccinatedOneDosePopulation"],
				   longitude=json["Longitude"], latitude=json["Latitude"],
				   lhd_reported_inventory=json["LHDReportedInventory"],
				   community_reported_inventory=json["CommunityReportedInventory"],
				   total_reported_inventory=json["TotalReportedInventory"], inventory_report_date=json["InventoryReportDate"])


class Administration:
	def __init__(self, last_updated_date, vaccine_administrations, current_vaccine_administration):
		self.last_updated_date = last_updated_date
		self.vaccine_administrations = vaccine_administrations
		self.current_vaccine_administration = current_vaccine_administration

	def __iter__(self):
		for vaccine_admin in self.vaccine_administrations:
			yield vaccine_admin

	def __getitem__(self, item) -> VaccineAdministration | None:
		if isinstance(item, int):
			return self.vaccine_administrations[item]
		elif isinstance(item, date):
			for vaccine_admin in self:
				if item == vaccine_admin.report_date:
					return vaccine_admin
		return None

	@property
	def last_updated_date(self) -> date:
		return self._last_updated_date

	@last_updated_date.setter
	def last_updated_date(self, last_updated_date: date):
		if not isinstance(last_updated_date, date):
			raise ValueError(f"The last updated date must be a datetime.date object: not {last_updated_date}")
		self._last_updated_date = last_updated_date

	@property
	def vaccine_administrations(self) -> list[VaccineAdministration]:
		return self._vaccine_administrations

	@vaccine_administrations.setter
	def vaccine_administrations(self, vaccine_administrations):
		self._vaccine_administrations = iter_check(vaccine_administrations, VaccineAdministration, "vaccine administrations")

	@property
	def current_vaccine_administration(self) -> VaccineAdministration:
		return self._current_vaccine_administration

	@current_vaccine_administration.setter
	def current_vaccine_administration(self, current_vaccine_administration:VaccineAdministration):
		if not isinstance(current_vaccine_administration, VaccineAdministration):
			raise ValueError(f"The current_vaccine_administration must be a VaccineAdministration object, not: {vaccine_admin.__class__.__name__}")
		self._current_vaccine_administration = current_vaccine_administration

	@classmethod
	def from_json(cls, json:dict):
		last_updated_date = json_to_date(json["lastUpdatedDate"])
		vaccine_administrations = [VaccineAdministration.from_json(administration) for administration in json["CurrentVaccineAdministration"]]
		current_vaccine_administration = VaccineAdministration.from_json(json["VaccineAdministration"])
		return cls(last_updated_date, vaccine_administrations, current_vaccine_administration)


class Race:
	def __init__(self, description:str, confirmed_cases:int, tested:int, deaths:int, color:str):
		self.description = description
		self.confirmed_cases = confirmed_cases
		self.tested = tested
		self.deaths = deaths
		self.color = color

	@property
	def description(self) -> str:
		return self._description

	@description.setter
	def description(self, description:str):
		if not isinstance(description, str):
			description = str(description)
		self._description = description

	@property
	def confirmed_cases(self) -> int:
		return self._confirmed_cases

	@confirmed_cases.setter
	def confirmed_cases(self, confirmed_cases:int):
		if not isinstance(confirmed_cases, int):
			confirmed_cases = int(confirmed_cases)
		self._confirmed_cases = confirmed_cases

	@property
	def tested(self) -> int:
		return self._tested

	@tested.setter
	def tested(self, tested: int):
		if not isinstance(tested, int):
			tested = int(tested)
		self._tested = tested

	@property
	def deaths(self) -> int:
		return self._deaths

	@deaths.setter
	def deaths(self, deaths: int):
		if not isinstance(deaths, int):
			deaths = int(deaths)
		self._deaths = deaths

	@property
	def color(self) -> str:
		return self._color

	@color.setter
	def color(self, color: str):
		if not isinstance(color, str):
			color = str(color)
		self._color = color

	@classmethod
	def from_json(cls, json:dict):
		description = json["description"]
		confirmed_cases = int(json["count"])
		tested = int(json["tested"])
		deaths = int(json["deaths"])
		color = json["color"]
		return cls(description, confirmed_cases, tested, deaths, color)


class Age:
	def __init__(self, races, age_group, confirmed_cases, tested, deaths):
		self.races = races
		self.age_group = age_group
		self.confirmed_cases = confirmed_cases
		self.tested = tested
		self.deaths = deaths

	@property
	def races(self) -> list[Race]:
		return self._races

	@races.setter
	def races(self, races:list[Race]):
		self._races = iter_check(races, Race, name="races")

	@property
	def age_group(self) -> str:
		return self._age_group

	@age_group.setter
	def age_group(self, age_group:str):
		if not isinstance(age_group, str):
			age_group = str(age_group)
		self._age_group = age_group.strip()

	@property
	def confirmed_cases(self) -> int:
		return self._confirmed_cases

	@confirmed_cases.setter
	def confirmed_cases(self, confirmed_cases:int):
		if not isinstance(confirmed_cases, int):
			confirmed_cases = int(confirmed_cases)
		self._confirmed_cases = confirmed_cases

	@property
	def tested(self) -> int:
		return self._tested

	@tested.setter
	def tested(self, tested: int):
		if not isinstance(tested, int):
			tested = int(tested)
		self._tested = tested

	@property
	def deaths(self) -> int:
		return self._deaths

	@deaths.setter
	def deaths(self, deaths: int):
		if not isinstance(deaths, int):
			deaths = int(deaths)
		self._deaths = deaths

	def value_tuple(self, property_name:str):
		dct = {race.description: getattr(race, property_name) for race in self.races}
		american_indian = dct["AI/AN**"]
		hawaiian = dct["NH/PI*"]
		hispanic = dct["Hispanic"]
		asian = dct["Asian"]
		other = dct["Other"]
		left_blank = dct["Left Blank"]
		black = dct["Black"]
		white = dct["White"]
		total = american_indian + hawaiian + hispanic + asian + other + left_blank + black + white
		return (self.age_group, american_indian, hawaiian, hispanic, asian, other, left_blank, black, white, total)

	@classmethod
	def from_json(cls, json:dict):
		race_list = [Race.from_json(race) for race in json["race"]]
		age_group = json["age_group"]
		confirmed_cases = int(json["count"])
		tested = int(json["tested"])
		deaths = int(json["deaths"])
		return cls(race_list, age_group, confirmed_cases, tested, deaths)


class Gender:
	def __init__(self, description, confirmed_cases, tested, deaths, color):
		self.description = description
		self.confirmed_cases = confirmed_cases
		self.tested = tested
		self.deaths = deaths
		self.color = color

	@property
	def description(self) -> str:
		"""The given gender: 'Female', 'Male', 'Unknown/Left Blank'"""
		return self._description

	@description.setter
	def description(self, description: str):
		if not isinstance(description, str):
			description = str(description)
		self._description = description

	@property
	def confirmed_cases(self) -> int:
		return self._confirmed_cases

	@confirmed_cases.setter
	def confirmed_cases(self, confirmed_cases:int):
		if not isinstance(confirmed_cases, int):
			confirmed_cases = int(confirmed_cases)
		self._confirmed_cases = confirmed_cases

	@property
	def tested(self) -> int:
		return self._tested

	@tested.setter
	def tested(self, tested: int):
		if not isinstance(tested, int):
			tested = int(tested)
		self._tested = tested

	@property
	def deaths(self) -> int:
		return self._deaths

	@deaths.setter
	def deaths(self, deaths: int):
		if not isinstance(deaths, int):
			deaths = int(deaths)
		self._deaths = deaths

	@property
	def color(self) -> str:
		return self._color

	@color.setter
	def color(self, color: str):
		if not isinstance(color, str):
			color = str(color)
		self._color = color

	@classmethod
	def from_json(cls, json:dict):
		description = json["description"]
		confirmed_cases = int(json["count"])
		tested = int(json["tested"])
		deaths = int(json["deaths"])
		color = json["color"]
		return cls(description, confirmed_cases, tested, deaths, color)


class Demographics:
	def __init__(self, ages, races, genders):
		self.ages = ages
		self.races = races
		self.genders = genders

	@property
	def ages(self) -> list[Age]:
		return self._ages

	@ages.setter
	def ages(self, ages:list[Age]):
		self._ages = iter_check(ages, Age, "ages")

	@property
	def races(self) -> list[Race]:
		return self._races

	@races.setter
	def races(self, races:list[Race]):
		self._races = iter_check(races, Race, "races")

	@property
	def genders(self) -> list[Gender]:
		return self._genders

	@genders.setter
	def genders(self, genders:list[Gender]):
		self._genders = iter_check(genders, Gender, "genders")

	@classmethod
	def from_json(cls, json:dict):
		age = [Age.from_json(age) for age in json["age"]]
		races = [Race.from_json(race) for race in json["race"]]
		gender = [Gender.from_json(gender) for gender in json["gender"]]
		return cls(age, races, gender)


class CountyDemographic:
	def __init__(self, county:str, confirmed_cases:int, tested:int, demographics:Demographics):
		self.county = county
		self.confirmed_cases = confirmed_cases
		self.tested = tested
		self.demographics = demographics

	@property
	def county(self) -> str:
		return self._county

	@county.setter
	def county(self, county:str):
		if not isinstance(county, str):
			county = str(county)
		self._county = county

	@property
	def confirmed_cases(self) -> int:
		return self._confirmed_cases

	@confirmed_cases.setter
	def confirmed_cases(self, confirmed_cases: int):
		if not isinstance(confirmed_cases, int):
			confirmed_cases = int(confirmed_cases)
		self._confirmed_cases = confirmed_cases

	@property
	def tested(self) -> int:
		return self._tested

	@tested.setter
	def tested(self, tested: int):
		if not isinstance(tested, int):
			tested = int(tested)
		self._tested = tested

	@property
	def demographics(self) -> Demographics:
		return self._demographics

	@demographics.setter
	def demographics(self, demographics:Demographics):
		if not isinstance(demographics, Demographics):
			raise ValueError(f"The demographics object must be a Demographics object, not: {demographics.__class__.__name__}")
		self._demographics = demographics

	@classmethod
	def from_json(cls, json:dict):
		county = json["County"]
		confirmed_cases = int(json["confirmed_cases"])
		tested = int(json["total_tested"])
		demographics = Demographics.from_json(json["demographics"])
		return CountyDemographic(county, confirmed_cases, tested, demographics)


class Root:
	def __init__(self, last_updated_date:date, county_demographics:list[CountyDemographic]):
		self.last_updated_date = last_updated_date
		self.county_demographics = county_demographics

	def __iter__(self):
		for demographic in self.county_demographics:
			yield demographic

	def __getitem__(self, item) -> CountyDemographic | None:
		if isinstance(item, int):
			return self.county_demographics[item]
		elif isinstance(item, str):
			lower = item.lower()
			for demographic in self:
				if lower == demographic.county.lower():
					return demographic
		return None

	@property
	def last_updated_date(self) -> date:
		return self._last_updated_date

	@last_updated_date.setter
	def last_updated_date(self, last_updated_date:date):
		if not isinstance(last_updated_date, date):
			raise ValueError(f"The last updated date must be a datetime.date object, not: {last_updated_date.__class__.__name__}")
		self._last_updated_date = last_updated_date

	@property
	def county_demographics(self) -> list[CountyDemographic]:
		return self._county_demographics

	@county_demographics.setter
	def county_demographics(self, county_demographics:list[CountyDemographic]):
		if not hasattr(county_demographics, "__iter__"):
			raise ValueError(f"The county demographics need to be an iterable object, not: {county_demographics.__class__.__name__}")
		for demographic in county_demographics:
			if not isinstance(demographic, CountyDemographic):
				raise ValueError(f"Every object in the county_demographic iterable must be a CountyDemographics object, not: {demographic.__class__.__name__}")
		if isinstance(county_demographics, list):
			self._county_demographics = county_demographics
		else:
			self._county_demographics = list(county_demographics)

	@classmethod
	def from_json(cls, json:dict):
		last_updated_date = json_to_date(json["lastUpdatedDate"])
		county_demographics = [CountyDemographic.from_json(demographic) for demographic in json["county_demographics"]]
		return cls(last_updated_date, county_demographics)


class StateWideVaccine:
	def __init__(self, report_date:date, total_doses:int, total_administered:int, persons_fully_vaccinated:int,
				 administered_rolling_average:float, administered_to_illinois_fully_vaccinated_5_plus,
				 administered_to_illinois_fully_vaccinated_5_plus_percent, administered_to_illinois_fully_vaccinated_12_plus,
				 administered_to_illinois_fully_vaccinated_12_plus_percent, administered_to_illinois_fully_vaccinated_18_plus,
				 administered_to_illinois_fully_vaccinated_18_plus_percent, administered_to_illinois_fully_vaccinated_65_plus,
				 administered_to_illinois_fully_vaccinated_65_plus_percent, administered_to_illinoisans_fully_vaccinated_5_plus,
				 administered_to_illinoisans_fully_vaccinated_5_plus_percent, administered_to_illinoisans_fully_vaccinated_12_plus,
				 administered_to_illinoisans_fully_vaccinated_12_plus_percent, administered_to_illinoisans_fully_vaccinated_18_plus,
				 administered_to_illinoisans_fully_vaccinated_18_plus_percent, administered_to_illinoisans_fully_vaccinated_65_plus,
				 administered_to_illinoisans_fully_vaccinated_65_plus_percent, administered_to_illinoisans_one_dose_5_plus,
				 administered_to_illinois_one_dose_5_plus_percent, administered_to_illinois_one_dose_12_plus,
				 administered_to_illinois_one_dose_12_plus_percent, administered_to_illinois_one_dose_18_plus,
				 administered_to_illinois_one_dose_18_plus_percent, administered_to_illinois_one_dose_65_plus,
				 administered_to_illinois_one_dose_65_plus_percent, administered_to_illinois_one_dose_5_plus,
				 administered_to_illinoisans_one_dose_5_plus_percent, administered_to_illinoisans_one_dose_12_plus,
				 administered_to_illinoisans_one_dose_12_plus_percent, administered_to_illinoisans_one_dose_18_plus,
				 administered_to_illinoisans_one_dose_18_plus_percent, administered_to_illinoisans_one_dose_65_plus,
				 administered_to_illinoisans_one_dose_65_plus_percent):
		self.report_date = report_date
		self.total_doses = total_doses
		self.total_administered = total_administered
		self.persons_fully_vaccinated = persons_fully_vaccinated
		self.administered_rolling_average = administered_rolling_average
		self.administered_to_illinois_fully_vaccinated_5_plus = administered_to_illinois_fully_vaccinated_5_plus
		self.administered_to_illinois_fully_vaccinated_5_plus_percent = administered_to_illinois_fully_vaccinated_5_plus_percent
		self.administered_to_illinois_fully_vaccinated_12_plus = administered_to_illinois_fully_vaccinated_12_plus
		self.administered_to_illinois_fully_vaccinated_12_plus_percent = administered_to_illinois_fully_vaccinated_12_plus_percent
		self.administered_to_illinois_fully_vaccinated_18_plus = administered_to_illinois_fully_vaccinated_18_plus
		self.administered_to_illinois_fully_vaccinated_18_plus_percent = administered_to_illinois_fully_vaccinated_18_plus_percent
		self.administered_to_illinois_fully_vaccinated_65_plus = administered_to_illinois_fully_vaccinated_65_plus
		self.administered_to_illinois_fully_vaccinated_65_plus_percent = administered_to_illinois_fully_vaccinated_65_plus_percent
		self.administered_to_illinoisans_fully_vaccinated_5_plus = administered_to_illinoisans_fully_vaccinated_5_plus
		self.administered_to_illinoisans_fully_vaccinated_5_plus_percent = administered_to_illinoisans_fully_vaccinated_5_plus_percent
		self.administered_to_illinoisans_fully_vaccinated_12_plus = administered_to_illinoisans_fully_vaccinated_12_plus
		self.administered_to_illinoisans_fully_vaccinated_12_plus_percent = administered_to_illinoisans_fully_vaccinated_12_plus_percent
		self.administered_to_illinoisans_fully_vaccinated_18_plus = administered_to_illinoisans_fully_vaccinated_18_plus
		self.administered_to_illinoisans_fully_vaccinated_18_plus_percent = administered_to_illinoisans_fully_vaccinated_18_plus_percent
		self.administered_to_illinoisans_fully_vaccinated_65_plus = administered_to_illinoisans_fully_vaccinated_65_plus
		self.administered_to_illinoisans_fully_vaccinated_65_plus_percent = administered_to_illinoisans_fully_vaccinated_65_plus_percent
		self.administered_to_illinoisans_one_dose_5_plus = administered_to_illinoisans_one_dose_5_plus
		self.administered_to_illinois_one_dose_5_plus_percent = administered_to_illinois_one_dose_5_plus_percent
		self.administered_to_illinois_one_dose_12_plus = administered_to_illinois_one_dose_12_plus
		self.administered_to_illinois_one_dose_12_plus_percent = administered_to_illinois_one_dose_12_plus_percent
		self.administered_to_illinois_one_dose_18_plus = administered_to_illinois_one_dose_18_plus
		self.administered_to_illinois_one_dose_18_plus_percent = administered_to_illinois_one_dose_18_plus_percent
		self.administered_to_illinois_one_dose_65_plus = administered_to_illinois_one_dose_65_plus
		self.administered_to_illinois_one_dose_65_plus_percent = administered_to_illinois_one_dose_65_plus_percent
		self.administered_to_illinois_one_dose_5_plus = administered_to_illinois_one_dose_5_plus
		self.administered_to_illinoisans_one_dose_5_plus_percent = administered_to_illinoisans_one_dose_5_plus_percent
		self.administered_to_illinoisans_one_dose_12_plus = administered_to_illinoisans_one_dose_12_plus
		self.administered_to_illinoisans_one_dose_12_plus_percent = administered_to_illinoisans_one_dose_12_plus_percent
		self.administered_to_illinoisans_one_dose_18_plus = administered_to_illinoisans_one_dose_18_plus
		self.administered_to_illinoisans_one_dose_18_plus_percent = administered_to_illinoisans_one_dose_18_plus_percent
		self.administered_to_illinoisans_one_dose_65_plus = administered_to_illinoisans_one_dose_65_plus
		self.administered_to_illinoisans_one_dose_65_plus_percent = administered_to_illinoisans_one_dose_65_plus_percent

	@property
	def report_date(self) -> date:
		return self._report_date

	@report_date.setter
	def report_date(self, report_date: date):
		if not isinstance(report_date, date):
			raise ValueError(f"The report date must be a datetime.date object, not: {report_date.__class__.__name__}")
		self._report_date = report_date

	@property
	def total_doses(self) -> int:
		return self._total_doses

	@total_doses.setter
	def total_doses(self, total_doses:int):
		if not isinstance(total_doses, int):
			total_doses = int(total_doses)
		self._total_doses = total_doses

	@property
	def total_administered(self) -> int:
		return self._total_administered

	@total_administered.setter
	def total_administered(self, total_administered:int):
		if not isinstance(total_administered, int):
			total_administered = int(total_administered)
		self._total_administered = total_administered

	@property
	def persons_fully_vaccinated(self) -> int:
		return self._persons_fully_vaccinated

	@persons_fully_vaccinated.setter
	def persons_fully_vaccinated(self, persons_fully_vaccinated:int):
		if not isinstance(persons_fully_vaccinated, int):
			persons_fully_vaccinated = int(persons_fully_vaccinated)
		self._persons_fully_vaccinated = persons_fully_vaccinated

	@property
	def administered_rolling_average(self) -> float:
		return self._administered_rolling_average

	@administered_rolling_average.setter
	def administered_rolling_average(self, administered_rolling_average:float):
		if not isinstance(administered_rolling_average, float):
			administered_rolling_average = float(administered_rolling_average)
		self._administered_rolling_average = administered_rolling_average

	# region Fully Vaccinated Administered to Illinois
	@property
	def administered_to_illinois_fully_vaccinated_5_plus(self) -> int:
		return self._administered_to_illinois_fully_vaccinated_5_plus

	@administered_to_illinois_fully_vaccinated_5_plus.setter
	def administered_to_illinois_fully_vaccinated_5_plus(self, administered_to_illinois_fully_vaccinated_5_plus:int):
		if not isinstance(administered_to_illinois_fully_vaccinated_5_plus, int):
			administered_to_illinois_fully_vaccinated_5_plus = int(administered_to_illinois_fully_vaccinated_5_plus)
		self._administered_to_illinois_fully_vaccinated_5_plus = administered_to_illinois_fully_vaccinated_5_plus

	@property
	def administered_to_illinois_fully_vaccinated_5_plus_percent(self) -> float:
		return self._administered_to_illinois_fully_vaccinated_5_plus_percent

	@administered_to_illinois_fully_vaccinated_5_plus_percent.setter
	def administered_to_illinois_fully_vaccinated_5_plus_percent(self, administered_to_illinois_fully_vaccinated_5_plus_percent: float):
		if not isinstance(administered_to_illinois_fully_vaccinated_5_plus_percent, float):
			administered_to_illinois_fully_vaccinated_5_plus_percent = float(administered_to_illinois_fully_vaccinated_5_plus_percent)
		self._administered_to_illinois_fully_vaccinated_5_plus_percent = administered_to_illinois_fully_vaccinated_5_plus_percent

	@property
	def administered_to_illinois_fully_vaccinated_12_plus(self) -> int:
		return self._administered_to_illinois_fully_vaccinated_12_plus

	@administered_to_illinois_fully_vaccinated_12_plus.setter
	def administered_to_illinois_fully_vaccinated_12_plus(self, administered_to_illinois_fully_vaccinated_12_plus:int):
		if not isinstance(administered_to_illinois_fully_vaccinated_12_plus, int):
			administered_to_illinois_fully_vaccinated_12_plus = int(administered_to_illinois_fully_vaccinated_12_plus)
		self._administered_to_illinois_fully_vaccinated_12_plus = administered_to_illinois_fully_vaccinated_12_plus

	@property
	def administered_to_illinois_fully_vaccinated_12_plus_percent(self) -> float:
		return self._administered_to_illinois_fully_vaccinated_12_plus_percent

	@administered_to_illinois_fully_vaccinated_12_plus_percent.setter
	def administered_to_illinois_fully_vaccinated_12_plus_percent(self, administered_to_illinois_fully_vaccinated_12_plus_percent: float):
		if not isinstance(administered_to_illinois_fully_vaccinated_12_plus_percent, float):
			administered_to_illinois_fully_vaccinated_12_plus_percent = float(administered_to_illinois_fully_vaccinated_12_plus_percent)
		self._administered_to_illinois_fully_vaccinated_12_plus_percent = administered_to_illinois_fully_vaccinated_12_plus_percent

	@property
	def administered_to_illinois_fully_vaccinated_18_plus(self) -> int:
		return self._administered_to_illinois_fully_vaccinated_18_plus

	@administered_to_illinois_fully_vaccinated_18_plus.setter
	def administered_to_illinois_fully_vaccinated_18_plus(self, administered_to_illinois_fully_vaccinated_18_plus:int):
		if not isinstance(administered_to_illinois_fully_vaccinated_18_plus, int):
			administered_to_illinois_fully_vaccinated_18_plus = int(administered_to_illinois_fully_vaccinated_18_plus)
		self._administered_to_illinois_fully_vaccinated_18_plus = administered_to_illinois_fully_vaccinated_18_plus

	@property
	def administered_to_illinois_fully_vaccinated_18_plus_percent(self) -> float:
		return self._administered_to_illinois_fully_vaccinated_18_plus_percent

	@administered_to_illinois_fully_vaccinated_18_plus_percent.setter
	def administered_to_illinois_fully_vaccinated_18_plus_percent(self, administered_to_illinois_fully_vaccinated_18_plus_percent: float):
		if not isinstance(administered_to_illinois_fully_vaccinated_18_plus_percent, float):
			administered_to_illinois_fully_vaccinated_18_plus_percent = float(administered_to_illinois_fully_vaccinated_18_plus_percent)
		self._administered_to_illinois_fully_vaccinated_18_plus_percent = administered_to_illinois_fully_vaccinated_18_plus_percent

	@property
	def administered_to_illinois_fully_vaccinated_65_plus(self) -> int:
		return self._administered_to_illinois_fully_vaccinated_65_plus

	@administered_to_illinois_fully_vaccinated_65_plus.setter
	def administered_to_illinois_fully_vaccinated_65_plus(self, administered_to_illinois_fully_vaccinated_65_plus:int):
		if not isinstance(administered_to_illinois_fully_vaccinated_65_plus, int):
			administered_to_illinois_fully_vaccinated_65_plus = int(administered_to_illinois_fully_vaccinated_65_plus)
		self._administered_to_illinois_fully_vaccinated_65_plus = administered_to_illinois_fully_vaccinated_65_plus

	@property
	def administered_to_illinois_fully_vaccinated_65_plus_percent(self) -> float:
		return self._administered_to_illinois_fully_vaccinated_65_plus_percent

	@administered_to_illinois_fully_vaccinated_65_plus_percent.setter
	def administered_to_illinois_fully_vaccinated_65_plus_percent(self, administered_to_illinois_fully_vaccinated_65_plus_percent: float):
		if not isinstance(administered_to_illinois_fully_vaccinated_65_plus_percent, float):
			administered_to_illinois_fully_vaccinated_65_plus_percent = float(administered_to_illinois_fully_vaccinated_65_plus_percent)
		self._administered_to_illinois_fully_vaccinated_65_plus_percent = administered_to_illinois_fully_vaccinated_65_plus_percent
	# endregion

	# region Fully Vaccinated Administered to Illinoisans
	@property
	def administered_to_illinoisans_fully_vaccinated_5_plus(self) -> int:
		return self._administered_to_illinoisans_fully_vaccinated_5_plus

	@administered_to_illinoisans_fully_vaccinated_5_plus.setter
	def administered_to_illinoisans_fully_vaccinated_5_plus(self, administered_to_illinoisans_fully_vaccinated_5_plus: int):
		if not isinstance(administered_to_illinoisans_fully_vaccinated_5_plus, int):
			administered_to_illinoisans_fully_vaccinated_5_plus = int(administered_to_illinoisans_fully_vaccinated_5_plus)
		self._administered_to_illinoisans_fully_vaccinated_5_plus = administered_to_illinoisans_fully_vaccinated_5_plus

	@property
	def administered_to_illinoisans_fully_vaccinated_5_plus_percent(self) -> float:
		return self._administered_to_illinoisans_fully_vaccinated_5_plus_percent

	@administered_to_illinoisans_fully_vaccinated_5_plus_percent.setter
	def administered_to_illinoisans_fully_vaccinated_5_plus_percent(self, administered_to_illinoisans_fully_vaccinated_5_plus_percent: float):
		if not isinstance(administered_to_illinoisans_fully_vaccinated_5_plus_percent, float):
			administered_to_illinoisans_fully_vaccinated_5_plus_percent = float(administered_to_illinoisans_fully_vaccinated_5_plus_percent)
		self._administered_to_illinoisans_fully_vaccinated_5_plus_percent = administered_to_illinoisans_fully_vaccinated_5_plus_percent

	@property
	def administered_to_illinoisans_fully_vaccinated_12_plus(self) -> int:
		return self._administered_to_illinoisans_fully_vaccinated_12_plus

	@administered_to_illinoisans_fully_vaccinated_12_plus.setter
	def administered_to_illinoisans_fully_vaccinated_12_plus(self, administered_to_illinoisans_fully_vaccinated_12_plus: int):
		if not isinstance(administered_to_illinoisans_fully_vaccinated_12_plus, int):
			administered_to_illinoisans_fully_vaccinated_12_plus = int(administered_to_illinoisans_fully_vaccinated_12_plus)
		self._administered_to_illinoisans_fully_vaccinated_12_plus = administered_to_illinoisans_fully_vaccinated_12_plus

	@property
	def administered_to_illinoisans_fully_vaccinated_12_plus_percent(self) -> float:
		return self._administered_to_illinoisans_fully_vaccinated_12_plus_percent

	@administered_to_illinoisans_fully_vaccinated_12_plus_percent.setter
	def administered_to_illinoisans_fully_vaccinated_12_plus_percent(self, administered_to_illinoisans_fully_vaccinated_12_plus_percent: float):
		if not isinstance(administered_to_illinoisans_fully_vaccinated_12_plus_percent, float):
			administered_to_illinoisans_fully_vaccinated_12_plus_percent = float(administered_to_illinoisans_fully_vaccinated_12_plus_percent)
		self._administered_to_illinoisans_fully_vaccinated_12_plus_percent = administered_to_illinoisans_fully_vaccinated_12_plus_percent

	@property
	def administered_to_illinoisans_fully_vaccinated_18_plus(self) -> int:
		return self._administered_to_illinoisans_fully_vaccinated_18_plus

	@administered_to_illinoisans_fully_vaccinated_18_plus.setter
	def administered_to_illinoisans_fully_vaccinated_18_plus(self, administered_to_illinoisans_fully_vaccinated_18_plus: int):
		if not isinstance(administered_to_illinoisans_fully_vaccinated_18_plus, int):
			administered_to_illinoisans_fully_vaccinated_18_plus = int(administered_to_illinoisans_fully_vaccinated_18_plus)
		self._administered_to_illinoisans_fully_vaccinated_18_plus = administered_to_illinoisans_fully_vaccinated_18_plus

	@property
	def administered_to_illinoisans_fully_vaccinated_18_plus_percent(self) -> float:
		return self._administered_to_illinoisans_fully_vaccinated_18_plus_percent

	@administered_to_illinoisans_fully_vaccinated_18_plus_percent.setter
	def administered_to_illinoisans_fully_vaccinated_18_plus_percent(self, administered_to_illinoisans_fully_vaccinated_18_plus_percent: float):
		if not isinstance(administered_to_illinoisans_fully_vaccinated_18_plus_percent, float):
			administered_to_illinoisans_fully_vaccinated_18_plus_percent = float(administered_to_illinoisans_fully_vaccinated_18_plus_percent)
		self._administered_to_illinoisans_fully_vaccinated_18_plus_percent = administered_to_illinoisans_fully_vaccinated_18_plus_percent

	@property
	def administered_to_illinoisans_fully_vaccinated_65_plus(self) -> int:
		return self._administered_to_illinoisans_fully_vaccinated_65_plus

	@administered_to_illinoisans_fully_vaccinated_65_plus.setter
	def administered_to_illinoisans_fully_vaccinated_65_plus(self, administered_to_illinoisans_fully_vaccinated_65_plus: int):
		if not isinstance(administered_to_illinoisans_fully_vaccinated_65_plus, int):
			administered_to_illinoisans_fully_vaccinated_65_plus = int(administered_to_illinoisans_fully_vaccinated_65_plus)
		self._administered_to_illinoisans_fully_vaccinated_65_plus = administered_to_illinoisans_fully_vaccinated_65_plus

	@property
	def administered_to_illinoisans_fully_vaccinated_65_plus_percent(self) -> float:
		return self._administered_to_illinoisans_fully_vaccinated_65_plus_percent

	@administered_to_illinoisans_fully_vaccinated_65_plus_percent.setter
	def administered_to_illinoisans_fully_vaccinated_65_plus_percent(self, administered_to_illinoisans_fully_vaccinated_65_plus_percent: float):
		if not isinstance(administered_to_illinoisans_fully_vaccinated_65_plus_percent, float):
			administered_to_illinoisans_fully_vaccinated_65_plus_percent = float(administered_to_illinoisans_fully_vaccinated_65_plus_percent)
		self._administered_to_illinoisans_fully_vaccinated_65_plus_percent = administered_to_illinoisans_fully_vaccinated_65_plus_percent
	# endregion

	# region One Dose Administered to Illinois
	@property
	def administered_to_illinois_one_dose_5_plus(self) -> int:
		return self._administered_to_illinois_one_dose_5_plus

	@administered_to_illinois_one_dose_5_plus.setter
	def administered_to_illinois_one_dose_5_plus(self, administered_to_illinois_one_dose_5_plus: int):
		if not isinstance(administered_to_illinois_one_dose_5_plus, int):
			administered_to_illinois_one_dose_5_plus = int(administered_to_illinois_one_dose_5_plus)
		self._administered_to_illinois_one_dose_5_plus = administered_to_illinois_one_dose_5_plus

	@property
	def administered_to_illinois_one_dose_5_plus_percent(self) -> float:
		return self._administered_to_illinois_one_dose_5_plus_percent

	@administered_to_illinois_one_dose_5_plus_percent.setter
	def administered_to_illinois_one_dose_5_plus_percent(self, administered_to_illinois_one_dose_5_plus_percent: float):
		if not isinstance(administered_to_illinois_one_dose_5_plus_percent, float):
			administered_to_illinois_one_dose_5_plus_percent = float(administered_to_illinois_one_dose_5_plus_percent)
		self._administered_to_illinois_one_dose_5_plus_percent = administered_to_illinois_one_dose_5_plus_percent

	@property
	def administered_to_illinois_one_dose_12_plus(self) -> int:
		return self._administered_to_illinois_one_dose_12_plus

	@administered_to_illinois_one_dose_12_plus.setter
	def administered_to_illinois_one_dose_12_plus(self, administered_to_illinois_one_dose_12_plus: int):
		if not isinstance(administered_to_illinois_one_dose_12_plus, int):
			administered_to_illinois_one_dose_12_plus = int(administered_to_illinois_one_dose_12_plus)
		self._administered_to_illinois_one_dose_12_plus = administered_to_illinois_one_dose_12_plus

	@property
	def administered_to_illinois_one_dose_12_plus_percent(self) -> float:
		return self._administered_to_illinois_one_dose_12_plus_percent

	@administered_to_illinois_one_dose_12_plus_percent.setter
	def administered_to_illinois_one_dose_12_plus_percent(self, administered_to_illinois_one_dose_12_plus_percent: float):
		if not isinstance(administered_to_illinois_one_dose_12_plus_percent, float):
			administered_to_illinois_one_dose_12_plus_percent = float(administered_to_illinois_one_dose_12_plus_percent)
		self._administered_to_illinois_one_dose_12_plus_percent = administered_to_illinois_one_dose_12_plus_percent

	@property
	def administered_to_illinois_one_dose_18_plus(self) -> int:
		return self._administered_to_illinois_one_dose_18_plus

	@administered_to_illinois_one_dose_18_plus.setter
	def administered_to_illinois_one_dose_18_plus(self, administered_to_illinois_one_dose_18_plus: int):
		if not isinstance(administered_to_illinois_one_dose_18_plus, int):
			administered_to_illinois_one_dose_18_plus = int(administered_to_illinois_one_dose_18_plus)
		self._administered_to_illinois_one_dose_18_plus = administered_to_illinois_one_dose_18_plus

	@property
	def administered_to_illinois_one_dose_18_plus_percent(self) -> float:
		return self._administered_to_illinois_one_dose_18_plus_percent

	@administered_to_illinois_one_dose_18_plus_percent.setter
	def administered_to_illinois_one_dose_18_plus_percent(self, administered_to_illinois_one_dose_18_plus_percent: float):
		if not isinstance(administered_to_illinois_one_dose_18_plus_percent, float):
			administered_to_illinois_one_dose_18_plus_percent = float(administered_to_illinois_one_dose_18_plus_percent)
		self._administered_to_illinois_one_dose_18_plus_percent = administered_to_illinois_one_dose_18_plus_percent

	@property
	def administered_to_illinois_one_dose_65_plus(self) -> int:
		return self._administered_to_illinois_one_dose_65_plus

	@administered_to_illinois_one_dose_65_plus.setter
	def administered_to_illinois_one_dose_65_plus(self, administered_to_illinois_one_dose_65_plus: int):
		if not isinstance(administered_to_illinois_one_dose_65_plus, int):
			administered_to_illinois_one_dose_65_plus = int(administered_to_illinois_one_dose_65_plus)
		self._administered_to_illinois_one_dose_65_plus = administered_to_illinois_one_dose_65_plus

	@property
	def administered_to_illinois_one_dose_65_plus_percent(self) -> float:
		return self._administered_to_illinois_one_dose_65_plus_percent

	@administered_to_illinois_one_dose_65_plus_percent.setter
	def administered_to_illinois_one_dose_65_plus_percent(self, administered_to_illinois_one_dose_65_plus_percent: float):
		if not isinstance(administered_to_illinois_one_dose_65_plus_percent, float):
			administered_to_illinois_one_dose_65_plus_percent = float(administered_to_illinois_one_dose_65_plus_percent)
		self._administered_to_illinois_one_dose_65_plus_percent = administered_to_illinois_one_dose_65_plus_percent
	# endregion

	# region One Dose Administered to Illinoisans
	@property
	def administered_to_illinoisans_one_dose_5_plus(self) -> int:
		return self._administered_to_illinoisans_one_dose_5_plus

	@administered_to_illinoisans_one_dose_5_plus.setter
	def administered_to_illinoisans_one_dose_5_plus(self, administered_to_illinoisans_one_dose_5_plus: int):
		if not isinstance(administered_to_illinoisans_one_dose_5_plus, int):
			administered_to_illinoisans_one_dose_5_plus = int(administered_to_illinoisans_one_dose_5_plus)
		self._administered_to_illinoisans_one_dose_5_plus = administered_to_illinoisans_one_dose_5_plus

	@property
	def administered_to_illinoisans_one_dose_5_plus_percent(self) -> float:
		return self._administered_to_illinoisans_one_dose_5_plus_percent

	@administered_to_illinoisans_one_dose_5_plus_percent.setter
	def administered_to_illinoisans_one_dose_5_plus_percent(self, administered_to_illinoisans_one_dose_5_plus_percent: float):
		if not isinstance(administered_to_illinoisans_one_dose_5_plus_percent, float):
			administered_to_illinoisans_one_dose_5_plus_percent = float(administered_to_illinoisans_one_dose_5_plus_percent)
		self._administered_to_illinoisans_one_dose_5_plus_percent = administered_to_illinoisans_one_dose_5_plus_percent

	@property
	def administered_to_illinoisans_one_dose_12_plus(self) -> int:
		return self._administered_to_illinoisans_one_dose_12_plus

	@administered_to_illinoisans_one_dose_12_plus.setter
	def administered_to_illinoisans_one_dose_12_plus(self, administered_to_illinoisans_one_dose_12_plus: int):
		if not isinstance(administered_to_illinoisans_one_dose_12_plus, int):
			administered_to_illinoisans_one_dose_12_plus = int(administered_to_illinoisans_one_dose_12_plus)
		self._administered_to_illinoisans_one_dose_12_plus = administered_to_illinoisans_one_dose_12_plus

	@property
	def administered_to_illinoisans_one_dose_12_plus_percent(self) -> float:
		return self._administered_to_illinoisans_one_dose_12_plus_percent

	@administered_to_illinoisans_one_dose_12_plus_percent.setter
	def administered_to_illinoisans_one_dose_12_plus_percent(self, administered_to_illinoisans_one_dose_12_plus_percent: float):
		if not isinstance(administered_to_illinoisans_one_dose_12_plus_percent, float):
			administered_to_illinoisans_one_dose_12_plus_percent = float(administered_to_illinoisans_one_dose_12_plus_percent)
		self._administered_to_illinoisans_one_dose_12_plus_percent = administered_to_illinoisans_one_dose_12_plus_percent

	@property
	def administered_to_illinoisans_one_dose_18_plus(self) -> int:
		return self._administered_to_illinoisans_one_dose_18_plus

	@administered_to_illinoisans_one_dose_18_plus.setter
	def administered_to_illinoisans_one_dose_18_plus(self, administered_to_illinoisans_one_dose_18_plus: int):
		if not isinstance(administered_to_illinoisans_one_dose_18_plus, int):
			administered_to_illinoisans_one_dose_18_plus = int(administered_to_illinoisans_one_dose_18_plus)
		self._administered_to_illinoisans_one_dose_18_plus = administered_to_illinoisans_one_dose_18_plus

	@property
	def administered_to_illinoisans_one_dose_18_plus_percent(self) -> float:
		return self._administered_to_illinoisans_one_dose_18_plus_percent

	@administered_to_illinoisans_one_dose_18_plus_percent.setter
	def administered_to_illinoisans_one_dose_18_plus_percent(self, administered_to_illinoisans_one_dose_18_plus_percent: float):
		if not isinstance(administered_to_illinoisans_one_dose_18_plus_percent, float):
			administered_to_illinoisans_one_dose_18_plus_percent = float(administered_to_illinoisans_one_dose_18_plus_percent)
		self._administered_to_illinoisans_one_dose_18_plus_percent = administered_to_illinoisans_one_dose_18_plus_percent

	@property
	def administered_to_illinoisans_one_dose_65_plus(self) -> int:
		return self._administered_to_illinoisans_one_dose_65_plus

	@administered_to_illinoisans_one_dose_65_plus.setter
	def administered_to_illinoisans_one_dose_65_plus(self, administered_to_illinoisans_one_dose_65_plus: int):
		if not isinstance(administered_to_illinoisans_one_dose_65_plus, int):
			administered_to_illinoisans_one_dose_65_plus = int(administered_to_illinoisans_one_dose_65_plus)
		self._administered_to_illinoisans_one_dose_65_plus = administered_to_illinoisans_one_dose_65_plus

	@property
	def administered_to_illinoisans_one_dose_65_plus_percent(self) -> float:
		return self._administered_to_illinoisans_one_dose_65_plus_percent

	@administered_to_illinoisans_one_dose_65_plus_percent.setter
	def administered_to_illinoisans_one_dose_65_plus_percent(self, administered_to_illinoisans_one_dose_65_plus_percent: float):
		if not isinstance(administered_to_illinoisans_one_dose_65_plus_percent, float):
			administered_to_illinoisans_one_dose_65_plus_percent = float(administered_to_illinoisans_one_dose_65_plus_percent)
		self._administered_to_illinoisans_one_dose_65_plus_percent = administered_to_illinoisans_one_dose_65_plus_percent
	# endregion

	def value_tuple(self):
		return (self.total_doses, self.total_administered, self.administered_rolling_average,
				self.administered_to_illinoisans_fully_vaccinated_5_plus,
				self.administered_to_illinoisans_fully_vaccinated_5_plus_percent,
				self.administered_to_illinoisans_one_dose_5_plus,
				self.administered_to_illinoisans_one_dose_5_plus_percent,

				self.administered_to_illinoisans_fully_vaccinated_12_plus,
				self.administered_to_illinoisans_fully_vaccinated_12_plus_percent,
				self.administered_to_illinoisans_one_dose_12_plus,
				self.administered_to_illinoisans_one_dose_12_plus_percent,

				self.administered_to_illinoisans_fully_vaccinated_18_plus,
				self.administered_to_illinoisans_fully_vaccinated_18_plus_percent,
				self.administered_to_illinoisans_one_dose_18_plus,
				self.administered_to_illinoisans_one_dose_18_plus_percent,

				self.administered_to_illinoisans_fully_vaccinated_65_plus,
				self.administered_to_illinoisans_fully_vaccinated_65_plus_percent,
				self.administered_to_illinoisans_one_dose_65_plus,
				self.administered_to_illinoisans_one_dose_65_plus_percent,

				self.administered_to_illinois_fully_vaccinated_5_plus,
				self.administered_to_illinois_fully_vaccinated_5_plus_percent,
				self.administered_to_illinois_one_dose_5_plus,
				self.administered_to_illinois_one_dose_5_plus_percent,

				self.administered_to_illinois_fully_vaccinated_12_plus,
				self.administered_to_illinois_fully_vaccinated_12_plus_percent,
				self.administered_to_illinois_one_dose_12_plus,
				self.administered_to_illinois_one_dose_12_plus_percent,

				self.administered_to_illinois_fully_vaccinated_18_plus,
				self.administered_to_illinois_fully_vaccinated_18_plus_percent,
				self.administered_to_illinois_one_dose_18_plus,
				self.administered_to_illinois_one_dose_18_plus_percent,

				self.administered_to_illinois_fully_vaccinated_65_plus,
				self.administered_to_illinois_fully_vaccinated_65_plus_percent,
				self.administered_to_illinois_one_dose_65_plus,
				self.administered_to_illinois_one_dose_65_plus_percent)

	@classmethod
	def from_json(cls, json:dict):
		return cls(report_date=json_to_date(json["Report_Date"]), total_doses=json["Total_Delivered"],
					total_administered=json["Total_Administered"], persons_fully_vaccinated=json["Persons_Fully_Vaccinated"],
					administered_rolling_average=json["AdministeredRollAvg"],
					administered_to_illinois_fully_vaccinated_5_plus=json["Persons_Fully_Vaccinated5plus"],
					administered_to_illinois_fully_vaccinated_5_plus_percent=json["Population_Fully_Vaccinated5plus"],
					administered_to_illinois_fully_vaccinated_12_plus=json["Persons_Fully_Vaccinated12plus"],
					administered_to_illinois_fully_vaccinated_12_plus_percent=json["Population_Fully_Vaccinated12plus"],
					administered_to_illinois_fully_vaccinated_18_plus=json["Persons_Fully_Vaccinated18plus"],
					administered_to_illinois_fully_vaccinated_18_plus_percent=json["Population_Fully_Vaccinated18plus"],
					administered_to_illinois_fully_vaccinated_65_plus=json["Persons_Fully_Vaccinated65plus"],
					administered_to_illinois_fully_vaccinated_65_plus_percent=json["Population_Fully_Vaccinated65plus"],
					administered_to_illinoisans_fully_vaccinated_5_plus=json["Persons_Fully_Vaccinated5plusCDC"],
					administered_to_illinoisans_fully_vaccinated_5_plus_percent=json["Population_Fully_Vaccinated5plusCDC"],
					administered_to_illinoisans_fully_vaccinated_12_plus=json["Persons_Fully_Vaccinated12plusCDC"],
					administered_to_illinoisans_fully_vaccinated_12_plus_percent=json["Population_Fully_Vaccinated12plusCDC"],
					administered_to_illinoisans_fully_vaccinated_18_plus=json["Persons_Fully_Vaccinated18plusCDC"],
					administered_to_illinoisans_fully_vaccinated_18_plus_percent=json["Population_Fully_Vaccinated18plusCDC"],
					administered_to_illinoisans_fully_vaccinated_65_plus=json["Persons_Fully_Vaccinated65plusCDC"],
					administered_to_illinoisans_fully_vaccinated_65_plus_percent=json["Population_Fully_Vaccinated65plusCDC"],
					administered_to_illinoisans_one_dose_5_plus=json["Vaccinated5plusOneDose"],
					administered_to_illinois_one_dose_5_plus_percent=json["Vaccinated5plusPercentOneDose"],
					administered_to_illinois_one_dose_12_plus=json["Vaccinated12plusOneDose"],
					administered_to_illinois_one_dose_12_plus_percent=json["Vaccinated12plusPercentOneDose"],
					administered_to_illinois_one_dose_18_plus=json["Vaccinated18plusOneDose"],
					administered_to_illinois_one_dose_18_plus_percent=json["Vaccinated18plusPercentOneDose"],
					administered_to_illinois_one_dose_65_plus=json["Vaccinated65plusOneDose"],
					administered_to_illinois_one_dose_65_plus_percent=json["Vaccinated65plusPercentOneDose"],
					administered_to_illinois_one_dose_5_plus=json["Vaccinated5plusOneDoseCDC"],
					administered_to_illinoisans_one_dose_5_plus_percent=json["Vaccinated5plusPercentOneDoseCDC"],
					administered_to_illinoisans_one_dose_12_plus=json["Vaccinated12plusOneDoseCDC"],
					administered_to_illinoisans_one_dose_12_plus_percent=json["Vaccinated12plusPercentOneDoseCDC"],
					administered_to_illinoisans_one_dose_18_plus=json["Vaccinated18plusOneDoseCDC"],
					administered_to_illinoisans_one_dose_18_plus_percent=json["Vaccinated18plusPercentOneDoseCDC"],
					administered_to_illinoisans_one_dose_65_plus=json["Vaccinated65plusOneDoseCDC"],
					administered_to_illinoisans_one_dose_65_plus_percent=json["Vaccinated65plusPercentOneDoseCDC"])
