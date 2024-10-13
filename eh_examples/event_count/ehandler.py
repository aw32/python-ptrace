import os
import time
import signal
import ptrace.linux_proc

class ehandler:
    def __init__(self):
        # counter for all processes
        self.num = 3
    def syscall_enter(self, syscall):
        if syscall.name == "clock_nanosleep" or syscall.name == "nanosleep":
            print(syscall.name, self.num, syscall.process.cmd)
        if (syscall.name == "clock_nanosleep" or syscall.name == "nanosleep"):
            if hasattr(syscall.process, "cmd") and len(syscall.process.cmd)>0 and syscall.process.cmd[0] == '/usr/bin/sleep':
                if self.num == 1:
                    print("Delay 3rd sleep call from /usr/bin/sleep processes")
                    time.sleep(5)
                if self.num > 0:
                    self.num -= 1
    def syscall_exit(self, syscall):
        pass
    def process_new(self, process):
        process.cmd = []
    def process_exec(self, process):
        # assign process command line to process object
        process.cmd = ptrace.linux_proc.readProcessCmdline(process.pid)


