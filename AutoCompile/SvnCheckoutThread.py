import commands
import threading


class SvnCheckoutThread(threading.Thread):
    def __init__(self, command):
        super(SvnCheckoutThread, self).__init__()
        self.command = command

    def run(self):
        commands.getstatusoutput(self.command)
