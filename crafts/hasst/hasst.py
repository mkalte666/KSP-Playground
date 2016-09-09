#!python3
#import stuff so we find everything
import sys
sys.path.append('../../')
import piloet.piloet as piloet
import piloet.task as task

# tasks here
class ThrustWait(task.Task):
    def init(self):
        self.piloet.vessel.control.throttle = 1.0
        self.piloet.vessel.auto_pilot.target_pitch_and_heading(90,90)
        self.piloet.vessel.auto_pilot.engage()
        self.piloet.vessel.control.activate_next_stage()
    def tick(self):
        if self.timeRunning > 2.0:
            self.done = True

    def cleanup(self):
        self.piloet.vessel.control.activate_next_stage()

class SecondStage(task.Task):
    def tick(self):
        engine = self.piloet.vessel.parts.with_title("RD-103")[0].engine
        if engine.thrust < 1.0:
            self.done = true
    
    def cleanup(self):
        self.piloet.vessel.control.activate_next_stage()
# startup everything

pilot = piloet.Piloet()
#add tasks

pilot.addTask(ThrustWait(SecondStage()))

#run! 
pilot.run()
