import os
import time
import signal
import ptrace.linux_proc
from ptrace.ctypes_tools import formatAddress

class ehandler:
    def __init__(self):
        pass
    def syscall_enter(self, syscall):
        if (syscall.name == "clock_nanosleep" or syscall.name == "nanosleep"):
            if hasattr(syscall.process, "cmd") and len(syscall.process.cmd)>0 and syscall.process.cmd[0] == '/usr/bin/sleep':
                print("current address before detaching:", formatAddress(syscall.instr_pointer))
                print()
                # send SIGSTOP to tracee
                # see https://stackoverflow.com/questions/39733919/detaching-gdb-without-resuming-the-inferior
                os.kill(syscall.process.pid, signal.SIGSTOP)
                # detach from tracee
                syscall.process.detach()
                # let strace.py exec gdb instead
                os.execv("/usr/bin/gdb",["/usr/bin/gdb","-p",str(syscall.process.pid)])
    def syscall_exit(self, syscall):
        pass
    def process_new(self, process):
        process.cmd = []
    def process_exec(self, process):
        # assign process command line to process object
        process.cmd = ptrace.linux_proc.readProcessCmdline(process.pid)


