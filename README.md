job-runner
==========

Lightweight application created for running jobs on demand with a RESTful API interface and a scalable backend. Job queues are based on Zeromq.

Setup on Red Hat Enterprise Linux 6.4 or CentOS 6.4
===================================================

wget -O /etc/yum.repos.d/home:fengshuo:zeromq.repo http://download.opensuse.org/repositories/home:/fengshuo:/zeromq/CentOS_CentOS-6/home:fengshuo:zeromq.repo
yum -y install zeromq python-zmq
yum install -y python-flask python-netaddr python-six python-iso8601 python-eventlet
yum install -y python-d2to1

python setup.py install

cp scripts/* /etc/init.d/
useradd jobrunner
mkdir /var/log/jobrunner
chown jobrunner.jobrunner /var/log/jobrunner/ 
mkdir /var/run/jobrunner
chown jobrunner.jobrunner /var/run/jobrunner/ 

# Start the services based on your configuration. For example:

# Frontend / web node:
service cloudbase-job-queue start
service cloudbase-job-publisher start

# Backend worker node:
service cloudbase-job-worker start

# On Red Hat Enterprise Linux, Fedora, CentOS, SL, you can set the service to start automatically:

chkconfig cloudbase-job-queue on
chkconfig cloudbase-job-publisher on
chkconfig cloudbase-job-worker on

# Note: the jobs will run with the "jobrunner" account, verify permissions accordingly.

