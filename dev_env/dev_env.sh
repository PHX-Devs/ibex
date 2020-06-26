# for dev environments!
# be responsible, please oh please don't deploy to prod with these options
setenforce 0
systemctl stop firewalld
systemctl disable firewalld