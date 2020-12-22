
# start or deploy cfBroker

# regisrter in cf
cf create-service-broker cf-broker admin admin http://cf-broker.com:5000
cf enable-service-access "Cloud Foundry"

# create service instance/org
cf create-service "Cloud Foundry" "CF Org" test_org -c '{\"name\":\"test_org\"}'
# check it
cf orgs | grep test_org

# rename service instance/org
cf update-service test_org -c '{\"name\":\"test_org2\"}'
# check it
cf orgs | grep test_org
# change it back
cf update-service test_org -c '{\"name\":\"test_org\"}'

# change quota of service instance/org
cf update-service test_org -c '{\"quota\":\"runaway\"}'
# check it
cf org test_org | grep quota

# delete service instance/org
cf delete-service test_org -f
# check it
cf orgs | grep test_org