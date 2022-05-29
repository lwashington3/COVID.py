from datetime import date


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
			raise ValueError("")
		self._last_updated_date = last_updated_date

	@property
	def vaccine_administrations(self) -> list[VaccineAdministration]:
		return self._vaccine_administrations

	@vaccine_administrations.setter
	def vaccine_administrations(self, vaccine_administrations):
		if not hasattr(vaccine_administrations, "__iter__"):
			raise ValueError(f"The vaccine administrations need to be an iterable object, not: {vaccine_administrations.__name__}")
		for vaccine_admin in vaccine_administrations:
			if not isinstance(vaccine_admin, VaccineAdministration):
				raise ValueError(f"Every object in the vaccine_administrations iterable must be a VaccineAdministration object, not: {vaccine_admin.__name__}")
		if isinstance(vaccine_administrations, list):
			self._vaccine_administrations = vaccine_administrations
		else:
			self._vaccine_administrations = list(vaccine_administrations)

	@property
	def current_vaccine_administration(self) -> VaccineAdministration:
		return self._current_vaccine_administration

	@current_vaccine_administration.setter
	def current_vaccine_administration(self, current_vaccine_administration):
		if not isinstance(current_vaccine_administration, VaccineAdministration):
			raise ValueError(f"The current_vaccine_administration must be a VaccineAdministration object, not: {vaccine_admin.__name__}")
		self._current_vaccine_administration = current_vaccine_administration


class VaccineAdministration:
	def __init__(self):
		pass

	@property
	def county_name(self) -> str:
		return self._county_name

	@county_name.setter
	def county_name(self, county_name: str):
		if not isinstance(county_name, str):
			county_name = str(county_name)
		self._county_name = county_name
