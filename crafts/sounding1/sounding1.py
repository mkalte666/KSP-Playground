#!python3
#import stuff so we find everything
import sys
sys.path.append('../../')

import piloet.piloet as piloet
import piloet.task as task


# tasks here
class SoundStager(task.Task):
    def init(self):
        self.piloet.vessel.control.throttle = 1.0
        self.piloet.vessel.control.activate_next_stage()

    def cleanup(self):
        self.piloet.vessel.control.activate_next_stage()

    def tick(self):
        if self.timeRunning > 1.0:
            self.done = True
# startup everything

pilot = piloet.Piloet()

#add tasks
pilot.addTask(SoundStager())

#run! 
pilot.run()
