from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in amh_rentals_erpnext/__init__.py
from amh_rentals_erpnext import __version__ as version

setup(
	name="amh_rentals_erpnext",
	version=version,
	description="ERPNext Customizations for AMH Rentals",
	author="Fahim Ali Zain",
	author_email="fahimalizain@gmail.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
