from setuptools import setup


with open("README.md", 'r') as f:
	long_description = f.read()


project_name = "covid"
git_url = "https://github.com/lwashington3/COVID.py"


setup(
	name="COVID Data Scraper",
	version="1.1.0",
	author="Len Washington III",
	author_email="l.washingtoniii.27@gmail.com",
	description="Daily Corona Scraper from the Illinois Department of Public Health",
	include_package_data=True,
	long_description=long_description,
	long_description_content_type="test/markdown",
	url=git_url,
	project_urls={
		"Bug Tracker": f"{git_url}/issues"
	},
	license="MIT",
	packages=[project_name],
	install_requires=["mysql-connector-python"],
	entry_points={
		"console_scripts": [f"{project_name}={project_name}.command_line:main"]
	},
	classifiers=[
		"Programming Language :: Python :: 3.10"
	]
)
