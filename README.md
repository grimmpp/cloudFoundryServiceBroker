# CloudFoundryServiceBroker

This service brokers makes it possible to book Cloud Foundry Organizations or Admin Access to Cloud Foundry in the Cloud Foundry Marketplace. 

The intention of this functionality is to offer Share Cloud Foundry Cluster for developers and for service providers. Developers can order Cloud Foundry Organizations and service providers can order admin access, so that they can register their service brokers or so that they can e.g. manage Application Security Groups for their service instances.

## How to use Service Plans
### Cloud Foundry Organization as a Service

Create new organization: `cf create-service "Cloud Foundry" "CF Org" test_org -c '{\"name\":\"test_org\"}'`  
Change organization name: `cf update-service test_org -c '{\"name\":\"test_org2\"}'`  
Change quota of organization: `cf update-service test_org -c '{\"quota\":\"runaway\"}'`  
Delete organization: `cf delete-service test_org`  

### Cloud Foundry Admin Access as a Service
Create new service instance (only service/no account): `cf create-service "Cloud Foundry" "CF Admin Access" myAdminAccess`  
Create service key/admin account: `cf create-service-key myAdminAccess myAdminServiceKey`  
Delete service key: `cf delete-service-key myAdminAccess myAdminServiceKey`  
Delete service instance: `cf service-key myAdminAccess myAdminServiceKey`  

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