job-runner
==========

Lightweight application created for running jobs on demand with a RESTful API interface and a scalable backend. Job queues are based on Zeromq.

Setup on CentOS 6.4
===================

wget -O /etc/yum.repos.d/home:fengshuo:zeromq.repo http://download.opensuse.org/repositories/home:/fengshuo:/zeromq/CentOS_CentOS-6/home:fengshuo:zeromq.repo
yum -y install zeromq
yum -y install python-zmq
yum -y install python-flask
