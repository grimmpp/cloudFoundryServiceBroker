# CloudFoundryServiceBroker

This service brokers makes it possible to book Cloud Foundry Organizations or Admin Access to Cloud Foundry in the Cloud Foundry Marketplace. 

The intention of this functionality is to offer Share Cloud Foundry Cluster for developers and for service providers. Developers can order Cloud Foundry Organizations and service providers can order admin access, so that they can register their service brokers or so that they can e.g. manage Application Security Groups for their service instances.

## Service Plans
### Cloud Foundry Organization as a Service
### Cloud Foundry Admin Access as a Service

## How to configure
In `cfBroker/settings.yml` you can enter and overwrite the predefined settings which are used for development.
In addition to that you can also overwrite single values by using environment variables. The mapping between the values in `cfBroker/settings.yml` and the environment variables can be found in `cfBroker/applicationSettings.py`.

## How to install
### Install package for development
python setup.py develop

## How to start
### Start Broker Locally
You can either start the broker in the project directory with `python main.py` or in the `cfBroker` folder by using `python app.py`.

## How to test
### Run Unit Tests
In order to run the unit tests just execute `python -m unittest discover -v` in the project directory.
### Run Manual Command Line Tests
In the test folder `test` you can find `cfRealAdminPlanTest.ps1` and `cfRealOrgPlanTest.ps1` which contain manual sample calls in order to test the broker functionality.