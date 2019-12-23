#!/usr/bin/python3
import os
import time

class MemInterval():
    def __init__(self):
        self.min = 1024**4 # 1T
        self.max = 0

    def update(self, value):
        self.min = min(self.min, value)
        self.max = max(self.max, value)

    def sub(self):
        return self.max - self.min

class MemInfo(object):
    def __init__(self, node):
        self.node = node
        self.total = 0
        self.used = MemInterval()
        self.free = MemInterval()
        self.shared = MemInterval()
        self.bufcache = MemInterval()
        self.avail = MemInterval()
        self.usage = 0
        local_cmd = "free"
        remote_cmd = "ssh %s free" % node
        self.cmd = local_cmd if node == "" or node == "localhost" else remote_cmd
        self.logfile = open("%s.mem.log" % node, "w")
        self.updateMemInfo(init = True)

    def __del__(self):
        self.logfile.close()

    def updateMemInfo(self, init = False):
        stream = os.popen(self.cmd)
        output = stream.read()
        memInfo = list(map(int, output.split('\n')[1].split()[1:]))
        self.total = memInfo[0]
        self.used.update(memInfo[1])
        self.free.update(memInfo[2])
        self.shared.update(memInfo[3])
        self.bufcache.update(memInfo[4])
        self.avail.update(memInfo[5])
        self.maxusage = max(self.avail.sub(), self.usage)
        self.logfile.write(output)


class ClusterManager(object):
    nodes = []
    mems = {}

    def __init__(self, nodes):
        self.nodes = nodes
        for node in nodes:
            # TODO: check if node is localhost
            # TODO: check if 2 nodes are same
            if node == "":
                node = "localhost"
            self.mems[node] = MemInfo(node)

    def __del__(self):
        # self.printSummary()
        pass

    def humanReadable(self, value, unit = 'k'):
        #TODO: update unit
        units = ['KB', 'MB', 'GB']
        idx = 0
        while value > 1024:
            value = value / 1024
            idx += 1
        return str(value) + units[idx]

    def printSummary(self, *args):
        maxMemUsage = {}
        for node in self.nodes:
            maxMemUsage[node] = self.humanReadable(self.mems[node].maxusage)
        print(maxMemUsage)
        with open('log', 'w') as fout:
            fout.write(str(maxMemUsage))
            fout.write('\n')

    def collect(self, interval = 1):
        while True:
            for _, mem in self.mems.items():
                mem.updateMemInfo()
            time.sleep(interval)

if __name__ == "__main__":
    nodes = []
    with open('nodes', 'r') as fin:
        for line in fin:
            nodes.append(line.strip())
    cm = ClusterManager(nodes)
    # import atexit
    # atexit.register(cm.printSummary, None, None)
    import signal
    signal.signal(signal.SIGTERM, cm.printSummary)
    signal.signal(signal.SIGINT, cm.printSummary)
    print('Start monitoring...')
    cm.collect(interval = 0.1)

