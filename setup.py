import setuptools

from packageInfo import package_name, package_version

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
   name=package_name,
   version=package_version,
   author='Philipp Grimm',
   author_email="grimm_philipp@web.de",
   description='CF Broker for creating and ordering CF Orgs, Admin Accounts, ...',
   long_description=long_description,
   long_description_content_type="text/markdown",
   url = "https://github.com/grimmpp/cloudFoundryServiceBroker",
   packages=setuptools.find_packages(),
   classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
   python_requires='>=3.6',
)