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

import sys
import zmq

from oslo.config import cfg
from jobrunner.openstack.common import log as logging

opts = [
    cfg.StrOpt('queue_pull_uri', default='tcp://127.0.0.1:4001', help='Zmq pull queue uri'),
    cfg.StrOpt('queue_push_uri', default='tcp://*:4002', help='Zmq push queue uri'),
]

CONF = cfg.CONF
CONF.register_opts(opts, 'jobqueue')

LOG = logging.getLogger(__name__)


def main():
    CONF(sys.argv[1:])
    logging.setup('jobqueue')

    context = zmq.Context(1)

    # Socket facing clients
    frontend = context.socket(zmq.PULL)
    frontend.bind(CONF.jobqueue.queue_pull_uri)

    # Socket facing services
    backend  = context.socket(zmq.PUSH)
    backend.bind(CONF.jobqueue.queue_push_uri)

    zmq.device(zmq.QUEUE, frontend, backend)

    frontend.close()
    backend.close()
    context.term()

if __name__ == "__main__":
    main()
