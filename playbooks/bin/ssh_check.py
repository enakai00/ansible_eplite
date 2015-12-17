#!/bin/python

from subprocess import *
import yaml, time, sys

output = Popen( [ './openstack.py', '--list' ], stdout=PIPE )
data = yaml.load(output.stdout)
hostvars = data['_meta']['hostvars']

args = sys.argv

for host in hostvars:
    if not ('openstack' in hostvars[host]
            and 'ansible_ssh_host' in hostvars[host]):
        continue
    name = hostvars[host]['openstack']['name']
    if name != args[1]:
        continue

    addr = hostvars[host]['ansible_ssh_host']
    count = 10
    while count > 0:
        try:
            print "Checking if %s:%s is reachable.... " % (name, addr),
            output = Popen( [ 'ssh', addr , 'uname' ], stdout=PIPE )
            print "ok."
            count = 0
        except:
            print "failed, try again."
            count -= 1
            time.sleep(5)
