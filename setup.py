from setuptools import setup, find_packages

with open("requirements.txt") as f:
    content = f.readlines()
requirements = [x.strip() for x in content]

setup(name="EnergyProfile",
      version="1.0",
      description="You can access information of the Greenhouse Gas (in terms of CO2 equivalent) footprint of electricity consumption.",
      packages=find_packages(),
      include_package_data=True,  # includes in package files from MANIFEST.in
      install_requires=requirements)
