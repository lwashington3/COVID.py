from datetime import date, datetime as dt


def iter_check(obj, type_name, name=None):
	if not hasattr(obj, "__iter__"):
		raise ValueError(f"{name} needs to be an iterable object, not: {obj.__name__}")
	for inner in obj:
		if not isinstance(inner, type_name):
			raise ValueError(f"Every object in the races iterable must be a {type_name.__name__} object, not: {inner.__name__}")
	return obj if isinstance(obj, list) else list(obj)


def json_to_date(json) -> date:
	test_date = f"{json['testDate']['year']}-{json['testDate']['month']}-{json['testDate']['day']}"
	return dt.strptime(test_date, "%Y-%m-%d").date()


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
			raise ValueError(f"The test date must be a datetime.date object, not: {last_updated_date.__name__}")
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
		self.deaths_7_day_rolling_avg = deaths_7_day_rolling_avg

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
		raise StopIteration

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
			raise ValueError(f"The last updated date must be a datetime.date object, not: {last_updated_date.__name__}")
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
	def __init__(self, county_name, administered_count):
		self.county_name = county_name
		self.administered_count = administered_count

	@property
	def county_name(self) -> str:
		return self._county_name

	@county_name.setter
	def county_name(self, county_name: str):
		if not isinstance(county_name, str):
			county_name = str(county_name)
		self._county_name = county_name

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

	@classmethod
	def from_json(cls, json:dict):
		county_name = json["CountyName"]
		administered_count = int(json["AdministeredCount"])
		return cls(county_name, administered_count)


class Administration:
	def __init__(self, last_updated_date, vaccine_administrations, current_vaccine_administration):
		self.last_updated_date = last_updated_date
		self.vaccine_administrations = vaccine_administrations
		self.current_vaccine_administration = current_vaccine_administration

	def __iter__(self):
		for vaccine_admin in self.vaccine_administrations:
			yield vaccine_admin
		raise StopIteration

	def __getitem__(self, item):
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
			raise ValueError(f"The current_vaccine_administration must be a VaccineAdministration object, not: {vaccine_admin.__name__}")
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
		self.color = color

	@classmethod
	def from_json(cls, json:dct):
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
		self._age_group = age_group

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
		self.color = color

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
			raise ValueError(f"The demographics object must be a Demographics object, not: {demographics.__name__}")
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
		raise StopIteration

	def __getitem__(self, item):
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
			raise ValueError(f"The last updated date must be a datetime.date object, not: {last_updated_date.__name__}")
		self._last_updated_date = last_updated_date

	@property
	def county_demographics(self) -> list[CountyDemographic]:
		return self._county_demographics

	@county_demographics.setter
	def county_demographics(self, county_demographics:list[CountyDemographic]):
		if not hasattr(county_demographics, "__iter__"):
			raise ValueError(f"The county demographics need to be an iterable object, not: {county_demographics.__name__}")
		for demographic in county_demographics:
			if not isinstance(demographic, CountyDemographic):
				raise ValueError(f"Every object in the county_demographic iterable must be a CountyDemographics object, not: {demographic.__name__}")
		if isinstance(county_demographics, list):
			self._county_demographics = county_demographics
		else:
			self._county_demographics = list(county_demographics)

	@classmethod
	def from_json(cls, json:dct):
		last_updated_date = json_to_date(json["lastUpdatedDate"])
		county_demographics = [CountyDemographic.from_json(demographic) for demographic in json["county_demographics"]]
		return cls(last_updated_date, county_demographics)
