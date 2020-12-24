# change into apps folder
cd ../cfBroker

# login
cf login -a https://api.dev.cfdev.sh --skip-ssl-validation -u admin -p admin -o cfdev-org -s cfdev-space

# push app
cf push cf-broker

# regisrter broker in cloud foundry
cf create-service-broker cf-broker admin admin https://cf-broker.dev.cfdev.sh

# make service plans visible
cf enable-service-access "Cloud Foundry"