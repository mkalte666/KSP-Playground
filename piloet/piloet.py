import krpc
import time

from .telemetry import Telemetry
from .task import Task

TICKTIME = 0.1

class Piloet:
    def __init__(self):
        self.conn = krpc.connect(name="Piloet")
        self.vessel = self.conn.space_center.active_vessel
        self.curtime = time.clock()
        #telemetry channels
        self.telemetry = Telemetry()
        self.telemetry.addChannel("ut", self.channelHelper(self.conn.space_center,"ut"))
        self.telemetry.addChannel("altitude",self.channelHelper(self.vessel.flight(),"mean_altitude"))
        self.telemetry.addChannel("apoapsis",self.channelHelper(self.vessel.orbit,"apoapsis_altitude"))
        #tasks
        self.tasks = list()

    def run(self):
        self.curtime = time.clock()
        while True:
            if time.clock()-self.curtime > TICKTIME:
                self.tick()
                self.curtime = time.clock()
            
    def tick(self):
        for task in self.tasks:
            task.tick_internal()
        pass
    
    def addTask(self, task):
        task.setPiloet(self)
        self.tasks.append(task)

    def channelHelper(self, a, b):
        return self.conn.add_stream(getattr, a, b);





