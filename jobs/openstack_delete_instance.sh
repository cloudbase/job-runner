#!/bin/bash

# terminate if a command fails
set -e
set -o pipefail

JOB_ID=$1
VM_ID=$2

# Required to avoid some quantum client warning messages
EDITOR=vim

source keystone_vars

echo "Getting the port id for VM: $VM_ID"
PORT_ID=`/usr/bin/quantum port-list -- --device_id $VM_ID | /bin/awk '{if (NR == 4) {print $2}}'`

echo "Getting the floating ip associated to port id: $PORT_ID"
FLOAT_IP_ID=`/usr/bin/quantum floatingip-list | /bin/awk -v port_id="$PORT_ID" '{if (NR > 3 && $8==port_id) { print $2 }}'`

echo "Deleting floating ip: $FLOAT_IP_ID"
/usr/bin/quantum floatingip-delete $FLOAT_IP_ID

echo "Deleting VM: $VM_ID"
/usr/bin/nova delete $VM_ID

