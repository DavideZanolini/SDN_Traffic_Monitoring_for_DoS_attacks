#!/bin/sh
#creating a connection between each host


#S1
sudo ovs-ofctl add-flow s1 in_port=1,actions=output:2,3,4,5
sudo ovs-ofctl add-flow s1 in_port=2,actions=output:1,3,4,5
sudo ovs-ofctl add-flow s1 in_port=3,actions=output:1,2,4,5
sudo ovs-ofctl add-flow s1 in_port=4,actions=output:1,2,3,5
sudo ovs-ofctl add-flow s1 in_port=5,actions=output:1,2,3,4




#S2
sudo ovs-ofctl add-flow s2 in_port=2,actions=output:1,3
sudo ovs-ofctl add-flow s2 in_port=3,actions=output:1,2
sudo ovs-ofctl add-flow s2 in_port=1,actions=output:2,3