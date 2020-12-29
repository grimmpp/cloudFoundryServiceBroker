
# start or deploy cfBroker

cf login -a https://api.dev.cfdev.sh --skip-ssl-validation -u admin -p admin -o cfdev-org -s cfdev-space

# regisrter in cf
cf create-service-broker cf-broker admin admin http://cf-broker.com:5000
cf update-service-broker cf-broker admin admin http://cf-broker.com:5000
cf enable-service-access "Cloud Foundry"

# create service instance/admin access
cf create-service "Cloud Foundry" "CF Admin Access" myAdminAccess
# check it
cf services | grep myAdminAccess

# create binding/admin user
cf create-service-key myAdminAccess myAdminServiceKey
# check it
cf service-key myAdminAccess myAdminServiceKey

# you can try to login by using the credentials and check if you can see all orgs, then you have got admin rights

# delete binding/admin user
cf delete-service-key myAdminAccess myAdminServiceKey -f
# check it
cf service-key myAdminAccess myAdminServiceKey
# you can also check if the user does not exist anymore
cf curl /v2/users
