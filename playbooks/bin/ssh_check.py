#!/bin/python

from subprocess import *
import yaml, time, sys

output = Popen(['./openstack.py', '--list'], stdout=PIPE)
data = yaml.load(output.stdout)
hostvars = data['_meta']['hostvars']

args = sys.argv

succeed = 0
for host in hostvars:
    if not ('openstack' in hostvars[host]
            and 'ansible_ssh_host' in hostvars[host]):
        continue
    name = hostvars[host]['openstack']['name']
    if name != args[1]:
        continue

    addr = hostvars[host]['ansible_ssh_host']
    count = 12
    while count > 0:
        print "Checking if %s:%s is reachable.... " % (name, addr),
        rc = call(['ssh', '-oStrictHostKeyChecking=no', addr , 'uname'])
        if rc == 0:
            print "ok."
            succeed = 1
            break
        else:
            print "failed, try again."
            count -= 1
            time.sleep(10)

if succeed != 1:
    print "Failed."
    sys.exit(1)

