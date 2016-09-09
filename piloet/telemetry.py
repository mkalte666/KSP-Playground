class Telemetry:
    def __init__(self):
        self.channels = dict()

    def addChannel(self, name, chan):
        self.channels[name] = chan

    def getChannel(self, name):
        return self.channels[name]()