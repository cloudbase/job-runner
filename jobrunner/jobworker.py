# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright 2013 Cloudbase Solutions Srl
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import json
import os
import subprocess
import sys
import urllib2
import zmq

from oslo.config import cfg
from jobrunner.openstack.common import log as logging

opts = [
    cfg.ListOpt('jobs', default='', help='job_name:path comma separated values'),
    cfg.StrOpt('queue_pull_uri', default='tcp://127.0.0.1:4002', help='Zmq pull queue uri'),
]

CONF = cfg.CONF
CONF.register_opts(opts, 'jobworker')

LOG = logging.getLogger(__name__)


def exec_proc(args):
    p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
    return (out, err)

def post_data(url, data):
   r = urllib2.Request(url, data=json.dumps(data))
   urllib2.urlopen(r)

def _get_jobs_dict():
   return dict([[a.strip() for a in v.split(':')]
                 for v in CONF.jobworker.jobs])

def exec_job(data):
    jobs = _get_jobs_dict()
    job_name = data['job_name']
    job_path = jobs.get(job_name, None)
    if not job_path:
        raise Exception('Job %s not defined' % job_name)

    args = [job_path, data['job_id']] + data['job_args']    
    out, err = exec_proc(args)

    return_url = data.get('return_url', None)
    if return_url:
        return_data = {}
        return_data['job_id'] = data['job_id']
        if out:
            return_data['out'] = out
        if err:
            return_data['err'] = err

        post_data(return_url, return_data)

def get_messages():
    context = zmq.Context()
    socket = context.socket(zmq.PULL)
    socket.setsockopt(zmq.IDENTITY, 'sub')

    socket.connect(CONF.jobworker.queue_pull_uri)

    while True:
        try:
            data = socket.recv_json()
            exec_job(data)
        except Exception, ex:
           print ex

    socket.close()
    context.term()

def main():
    CONF(sys.argv[1:])
    logging.setup('jobworker')

    jobs = _get_jobs_dict()
    if not jobs:
        LOG.warning("No jobs defined!")

    get_messages()

if __name__ == '__main__':
    main()
