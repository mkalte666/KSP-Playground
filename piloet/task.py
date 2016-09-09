import piloet

class Task:
    def __init__(self, nextTask=None):
        self.nextTask=nextTask
        self.done=False
        self.timeRunning = 0.0
        self.didInit=False
        self.didCleanup=False
        self.piloet = None
    def setNext(self, nextTask):
        self.nextTask = nextTask
        self.nextTask.setPiloet(self.piloet)

    def setPiloet(self, p):
        self.piloet = p
        if self.nextTask != None:
            self.nextTask.setPiloet(self.piloet)

    def tick_internal(self):
        if self.done:
            if self.didCleanup == False:
                self.cleanup()
                self.didCleanup = True
            if self.nextTask != None:
                self.nextTask.tick_internal()
        else:
            if self.didInit == False:
                self.init()
                self.didInit = True
            self.tick()
            self.timeRunning += 0.1
    def init(self):
        pass
    def cleanup(self):
        pass

    def tick(self):
        pass
