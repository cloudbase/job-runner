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

import flask
import zmq
import json
import uuid

from zmq import devices


app = flask.Flask(__name__)

context = None
socket = None
pd = None

def bind():
    global socket, context, pd

    #start_queue()

    context = zmq.Context()
    #socket = context.socket(zmq.PUB)
    socket = context.socket(zmq.PUSH)
    #socket = context.socket(zmq.REQ)
    socket.connect("tcp://127.0.0.1:4001")
    socket.setsockopt(zmq.IDENTITY, 'pub')
    #socket.setsockopt(zmq.SNDHWM, 100)
    #socket.bind("tcp://*:4001")

def enqueue_job(data):
    global socket
    if not socket:
        bind()

    socket.send_json(data)

def start_queue():
    pd = devices.ProcessDevice(zmq.QUEUE, zmq.ROUTER, zmq.DEALER)
    pd.bind_in('tcp://*:4001')
    pd.bind_out('tcp://*:4002')
    pd.setsockopt_in(zmq.IDENTITY, 'ROUTER')
    pd.setsockopt_out(zmq.IDENTITY, 'DEALER')
    pd.start()


@app.route('/jobs/new', methods = ['POST'])
def new_job():
    request_data = flask.request.json

    auth_key = request_data['auth_key']
    if auth_key != 'change_me_asap_please':
        raise Exception('The provided auth_key is not valid')

    job_id = str(uuid.uuid4()) 

    # Copy relevant dict content
    data = {}
    data['job_name'] = request_data.get('job_name', 'default')
    data['job_args'] = request_data.get('job_args', [])
    data['return_url'] = request_data.get('return_url', None)
    data['job_id'] = job_id

    enqueue_job(data)

    return json.dumps({'job_id':job_id})

if __name__ == '__main__':
    app.run(debug = True, port=4000)


