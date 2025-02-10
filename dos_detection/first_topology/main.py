#!/usr/bin/python3

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import OVSKernelSwitch, RemoteController
from mininet.cli import CLI
from mininet.link import TCLink
import subprocess
import time
from datetime import datetime

class NetworkSlicingTopo(Topo):
    def __init__(self):
        #initialize topology
        Topo.__init__(self)

        #create template host,switch and Link

        host_config = dict(inNamespace=True)
        link_config = dict() #total capacity of the link 10Mbps
        host_link_config = dict()

        #create routers nodes - 4 routers in our case
        for i in range(4):
            sconfig = {"dpid": "%016x" % (i+1)}
            self.addSwitch("s%d" % (i+1), **sconfig)

        #create host nodes - 7 host nodes

        self.addHost("dns",ip="10.0.0.10")

        for i in range(1, 4):
            self.addHost("web" + str(i),ip="10.0.0." + str(i))

        #ISP
        self.addHost("r1",ip="10.0.0.5")
        self.addHost("r2",ip="10.0.0.6")

        #Rete aziendale
        self.addHost("intra",ip="10.0.0.7")

        #Host
        self.addHost("cap",ip="10.0.0.8")

        #add links
        self.addLink("s1", "s3")
        self.addLink("s3", "s2")
        self.addLink("s2", "s4")

        self.addLink("intra", "s1")
        self.addLink("r1","s1",bw=70)
        self.addLink("r2","s2",bw=70)
        self.addLink("dns","s4")
        self.addLink("web1","s3",bw=50)
        self.addLink("web2","s3",bw=50)
        self.addLink("web3","s3",bw=50)
        self.addLink("cap","s1",bw=70)

topos = {"networkslicingtopo": (lambda: NetworkSlicingTopo())}

if __name__=="__main__":
    topo = NetworkSlicingTopo()
    net = Mininet(
        topo=topo,
        controller=RemoteController('c0', ip='127.0.0.1'),
        switch=OVSKernelSwitch,
        build=False,
        autoSetMacs=True,
        autoStaticArp=True,
        link=TCLink,
    )

    net.build()
    net.start()
    subprocess.run("bash total_connectivity.sh", shell=True, check=True)

    webservers = ['web1','web2','web3']
    for i in range(3):
        webserver = webservers[i]
        cmd = "sudo python3 custom_http_server.py &"
        print("Running '{}' at web{}".format(cmd, i+1))
        net.get(webserver).cmd(cmd)
        time.sleep(0.2)

    print("Starting the local DNS service")
    net.get('dns').cmd("python3 dns.py &")
    time.sleep(0.2)

    net.get('intra').cmd("python3 simulator.py &")
    for i in range(20):
        net.get('r1').cmd("python3 simulator.py &")

    # Start PCAP capture loop in the background
    print("Starting rotating PCAP capture on s1-eth4...")
    net.get('s1').cmd("""
        while true; do 
            timestamp=$(date +%H%M%S)
            sudo timeout 30 tcpdump -i s1-eth4 -w /tmp/capture_$timestamp.pcap &
            wait
        done &
    """)

    print("Start monitoring the network for DoS attacks...")
    net.get('cap').cmd("python3 cap_scripts/cap_main.py &")
    time.sleep(0.2)
        
    CLI(net)
    net.stop()