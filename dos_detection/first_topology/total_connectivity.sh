#!/bin/sh
#creating a connection between s2 and s4


#S1
sudo ovs-ofctl add-flow s1 in_port=1,actions=output:2,3,4
sudo ovs-ofctl add-flow s1 in_port=2,actions=output:1,3,4
sudo ovs-ofctl add-flow s1 in_port=3,actions=output:1,2,4
sudo ovs-ofctl add-flow s1 in_port=4,actions=output:1,2,3



#S2
sudo ovs-ofctl add-flow s2 in_port=2,actions=output:1,3
sudo ovs-ofctl add-flow s2 in_port=3,actions=output:1,2
sudo ovs-ofctl add-flow s2 in_port=1,actions=output:2,3


#S3
sudo ovs-ofctl add-flow s3 in_port=1,actions=output:2,3,4,5
sudo ovs-ofctl add-flow s3 in_port=2,actions=output:1,3,4,5
sudo ovs-ofctl add-flow s3 in_port=3,actions=output:1,2,4,5
sudo ovs-ofctl add-flow s3 in_port=4,actions=output:1,2,3,5
sudo ovs-ofctl add-flow s3 in_port=5,actions=output:1,2,3,4


#S4
sudo ovs-ofctl add-flow s4 in_port=1,actions=output:2
sudo ovs-ofctl add-flow s4 in_port=2,actions=output:1