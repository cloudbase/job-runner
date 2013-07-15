#!/bin/bash

# terminate if a command fails
set -e 
set -o pipefail

# Required to avoid some quantum client warning messages
export EDITOR=vim

source ./keystone_vars

# Required to avoid some quantum client warning messages
export EDITOR=vim

JOB_ID=$1
IMAGE_URL=$2
IMAGE_HASH=$3

IMAGE_NAME=OpenStack_$JOB_ID
IMAGE_PATH=/tmp/$IMAGE_NAME

KEY_NAME=key1
FLAVOR_ID=13
NET_NAME=net1

EXT_NET_NAME=ext_net

echo "Downloading image from url: $IMAGE_URL"

IMAGE_PATH_TMP="$IMAGE_PATH"_tmp
/usr/bin/wget --quiet -O - $IMAGE_URL | bunzip2 > $IMAGE_PATH_TMP

echo "Converting image to VHD"

/usr/bin/qemu-img convert -O vpc $IMAGE_PATH_TMP $IMAGE_PATH

echo "Deleting temporary source image file"
rm -f $IMAGE_PATH_TMP

#TODO: check hash
#IMAGE_HASH_CALC=`sha1sum $IMAGE_PATH`

echo "Creating glance image"

#/usr/bin/bunzip2 -cd $IMAGE_PATH | /usr/bin/glance image-create --property hypervisor_type=hyperv --name $IMAGE_NAME --container-format bare --disk-format vhd
/usr/bin/glance image-create --property hypervisor_type=hyperv --name $IMAGE_NAME --container-format bare --disk-format vhd < $IMAGE_PATH > /dev/null

echo "Deleting image file"

rm -f $IMAGE_PATH

echo "Getting network id"

NET_ID=`/usr/bin/quantum net-show $NET_NAME | /bin/awk '{if (NR == 5) {print $4}}'`

echo "Booting instance"

VM_NAME=$IMAGE_NAME
VM_ID=`/usr/bin/nova boot  --flavor $FLAVOR_ID --image $IMAGE_NAME --key-name $KEY_NAME --nic net-id=$NET_ID --poll $VM_NAME | /bin/awk '{if (NR == 15) {print $4}}'`

echo "Instance id: $VM_ID"

echo "Deleting glance image"

/usr/bin/glance image-delete $IMAGE_NAME > /dev/null

echo "Getting instance port id"

PORT_ID=`/usr/bin/quantum port-list -- --device_id $VM_ID | /bin/awk '{if (NR == 4) {print $2}}'`

echo "Creating floating ip"

TMP_FILE=/tmp/$(uuidgen).txt
quantum floatingip-create $EXT_NET_NAME > $TMP_FILE
FLOAT_IP_ID=`/bin/cat $TMP_FILE | /bin/awk '{if (NR == 8) {print $4}}'`
FLOAT_IP=`/bin/cat $TMP_FILE | /bin/awk '{if (NR == 6) {print $4}}'`
rm -f $TMP_FILE

echo "Associating floating ip"

/usr/bin/quantum floatingip-associate $FLOAT_IP_ID $PORT_ID > /dev/null

echo VM_ID=$VM_ID
echo FLOATING_IP=$FLOAT_IP

