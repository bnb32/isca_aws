#!/bin/bash

sudo mkdir -p /data

#Put /data/cold/shared into fstab
sudo sed -i '/fs-3fd3cdbf.efs.us-east-1.amazonaws.com/d' /etc/fstab
sudo sh -c "echo 'fs-3fd3cdbf.efs.us-east-1.amazonaws.com:/     /data   nfs4     nfsvers=4.1,rsize=1048576,wsize=1048576,hard,timeo=600,retrans=2,noresvport    0   0' >> /etc/fstab"   

# Mount fstab
sudo mount -a

# Create Home Environment Link
mkdir -p ~/environment
ln -sf /data ~/environment/data
