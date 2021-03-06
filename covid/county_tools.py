from enum import Enum


def generate_placeholders(number:int) -> str:
	return ("%s," * number).strip(",")


# region Overall Data Links
def get_county_data_link() -> str:
	return "http://www.dph.illinois.gov/sitefiles/CountyList.json?nocache=1"


def get_age_race_link() -> str:
	return "https://idph.illinois.gov/DPHPublicInformation/api/COVID/GetCountyDemographics?countyName="


def get_overall_data_link() -> str:
	return "https://idph.illinois.gov/DPHPublicInformation/api/COVID/GetIllinoisCases"
# endregion


def get_vaccine_details_link() -> str:
	return "https://idph.illinois.gov/DPHPublicInformation/api/covidvaccine/getStatewideVaccineDetails"


def get_vaccine_administration_link() -> str:
	return "https://idph.illinois.gov/DPHPublicInformation/api/covidVaccine/getVaccineAdministration?countyName="


class County(Enum):
	Adams = "Adams"
	Alexander = "Alexander"
	Bond = "Bond"
	Boone = "Boone"
	Brown = "Brown"
	Bureau = "Bureau"
	Calhoun = "Calhoun"
	Carroll = "Carroll"
	Cass = "Cass"
	Champaign = "Champaign"
	Chicago = "Chicago"
	Christian = "Christian"
	Clark = "Clark"
	Clay = "Clay"
	Clinton = "Clinton"
	Coles = "Coles"
	Cook = "Cook"
	Crawford = "Crawford"
	Cumberland = "Cumberland"
	De_Witt = "De Witt"
	DeKalb = "DeKalb"
	Douglas = "Douglas"
	DuPage = "DuPage"
	Edgar = "Edgar"
	Edwards = "Edwards"
	Effingham = "Effingham"
	Fayette = "Fayette"
	Ford = "Ford"
	Franklin = "Franklin"
	Fulton = "Fulton"
	Gallatin = "Gallatin"
	Greene = "Greene"
	Grundy = "Grundy"
	Hamilton = "Hamilton"
	Hancock = "Hancock"
	Hardin = "Hardin"
	Henderson = "Henderson"
	Henry = "Henry"
	Illinois = "Illinois"
	Iroquois = "Iroquois"
	Jackson = "Jackson"
	Jasper = "Jasper"
	Jefferson = "Jefferson"
	Jersey = "Jersey"
	Jo_Daviess = "Jo Daviess"
	Johnson = "Johnson"
	Kane = "Kane"
	Kankakee = "Kankakee"
	Kendall = "Kendall"
	Knox = "Knox"
	Lake = "Lake"
	LaSalle = "LaSalle"
	Lawrence = "Lawrence"
	Lee = "Lee"
	Livingston = "Livingston"
	Logan = "Logan"
	Macon = "Macon"
	Macoupin = "Macoupin"
	Madison = "Madison"
	Marion = "Marion"
	Marshall = "Marshall"
	Mason = "Mason"
	Massac = "Massac"
	McDonough = "McDonough"
	McHenry = "McHenry"
	McLean = "McLean"
	Menard = "Menard"
	Mercer = "Mercer"
	Monroe = "Monroe"
	Montgomery = "Montgomery"
	Morgan = "Morgan"
	Moultrie = "Moultrie"
	Ogle = "Ogle"
	Out_Of_State = "Out Of State"
	Peoria = "Peoria"
	Perry = "Perry"
	Piatt = "Piatt"
	Pike = "Pike"
	Pope = "Pope"
	Pulaski = "Pulaski"
	Putnam = "Putnam"
	Randolph = "Randolph"
	Richland = "Richland"
	Rock_Island = "Rock Island"
	Saline = "Saline"
	Sangamon = "Sangamon"
	Schuyler = "Schuyler"
	Scott = "Scott"
	Shelby = "Shelby"
	St_Clair = "St. Clair"
	Stark = "Stark"
	Stephenson = "Stephenson"
	Tazewell = "Tazewell"
	Unassigned = "Unassigned"
	Union = "Union"
	Vermilion = "Vermilion"
	Wabash = "Wabash"
	Warren = "Warren"
	Washington = "Washington"
	Wayne = "Wayne"
	White = "White"
	Whiteside = "Whiteside"
	Will = "Will"
	Williamson = "Williamson"
	Winnebago = "Winnebago"
	Woodford = "Woodford"


def county_to_link(link:str, county:County) -> str:
	return link + county.value.replace(" ", "%20")


def county_to_sql(county:County) -> str:
	return county.value.replace(" ", "_").replace(".", "")
