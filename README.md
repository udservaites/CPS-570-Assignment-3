# Homework #3 Traceroute in Python
## CPS 570 Spring 2018
## K Rebecca Servaites

#### This program implements the tracert functionality using a python script. This program can implement the tracert in serial and parallel form. 
#### The library scapy was used to create, send, and receive the packets. This program was written using Python 2, but it should also work with Python 3.
#### How to install scapy:

##### 1.  Visit https://scapy.readthedocs.io/en/latest/installation.html#installing-scapy-v2-x for instructions on how to install the library

##### 2. 



### Report

ICMP works much better than the udp in the packet construction. UDP had a tendency to lose packets at servers and never completer the tracert. ICMp is also much faster than the UDP packets. 