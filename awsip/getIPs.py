#!/usr/bin/python3

details = []
ips = []
with open('details', 'r') as fin:
    for line in fin:
        details.append(line)

for item in details:
    ip = '.'.join(item.split(': ')[1].split('.')[0].split('-')[1:])
    ips.append(ip.strip())

with open('ips', 'w') as fout:
    for ip in ips:
        fout.write(ip+'\n')
print(','.join(ips))
