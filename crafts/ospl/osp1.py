#!python3
#import stuff so we find everything
import sys
import math
sys.path.append('../../')
import piloet.piloet as piloet
import piloet.task as task

# tasks here
class ThrustWait(task.Task):
    def init(self):
        self.piloet.vessel.auto_pilot.engage()
        self.piloet.vessel.control.activate_next_stage()
    def tick(self):
        if self.timeRunning > 2.0:
            self.done = True

    def cleanup(self):
        self.piloet.vessel.control.activate_next_stage()

class SecondStage(task.Task):
    def tick(self):
        pass
        #engine = self.piloet.vessel.parts.with_title("RD-103")[0].engine
        #if engine.thrust < 1.0:
        #    self.done = true
    
    def cleanup(self):
        self.piloet.vessel.control.activate_next_stage()

class AscendGuidance(task.Task):
    def init(self):
        self.piloet.vessel.auto_pilot.engage()
        self.piloet.vessel.auto_pilot.target_pitch_and_heading(90,90)
        self.turnStartAltitude = 100.0
        self.turnEndAltitude = 80000.0
        self.turnHalfDegrees = 25000.0
        self.targetAltitude = 200000.0
        self.k = -(math.log((90.0-45.0)/90.0,math.e)/self.turnHalfDegrees)
        self.turnFunc = lambda x: 90.0-90.0*pow(math.e,-self.k*x)
    def cleanup(self):
        pass

    def tick(self):
        alt = self.piloet.telemetry.getChannel("altitude")
        p = 0 # up is default
        if self.piloet.telemetry.getChannel("apoapsis") > self.targetAltitude:
            p = 95 #slightly down so we dont rais the apogee further
        else:
            if alt > self.turnStartAltitude and alt < self.turnEndAltitude:
                p = self.turnFunc(alt)
            elif alt > self.turnEndAltitude:
                p = 80 # still raise them apogee
        #set target
        p = 90 - p
        self.piloet.vessel.auto_pilot.target_pitch_and_heading(p,90)

# startup everything

pilot = piloet.Piloet()
#add tasks

pilot.addTask(ThrustWait(SecondStage()))
pilot.addTask(AscendGuidance())

#run! 
pilot.run()
