import os
import os.path
import shutil
import time
import signal
import ptrace.linux_proc
from ptrace.ctypes_tools import formatAddress
import ptrace.ctypes_tools

# make sure the backup file does not already exist and create directories
def prep_backupfile(bfile, pid):
    # takes absolute path to the new (regular) file: /some/path/filename
    # split into ("/some/path", "filename")
    bfile_split = os.path.split(bfile.strip('/'))
    # split path "/some/path" into array of parts ["some","path"]
    parts = bfile_split[0].split('/') # only use path up to filename
    path = '/'
    for part in parts:
        new_path = os.path.join(path, part)
        if os.path.exists(new_path) == False: # if path does not exists, create folder
            os.mkdir(new_path)
        if os.path.isdir(new_path) == False:  # if path is not a folder, create alternative path
            new_part = part + '_' + str(pid)
            new_path = os.path.join(new_path, new_part)
            if os.path.exists(new_path):
                c = 1
                c_part = new_part + '_' + str(c)
                new_path = os.path.join(new_path, c_part)
                while os.path.exists(new_path):
                    c += 1
                    c_part = new_part + '_' + str(c)
                    new_path = os.path.join(new_path, c_part)
                os.mkdir(new_path)
        path = new_path
    bfile = os.path.join(path, bfile_split[1]) # final path
    #if os.path.exists(bfile):
    #    bfile = bfile.rstrip('/') + "_" + str(pid)
    bfile = bfile.rstrip('/') + "_" + str(pid)
    if os.path.exists(bfile):
        c = 1
        new_bfile = bfile.rstrip('/') + "_" + str(c)
        while os.path.exists(new_bfile):
            c += 1
            new_bfile = bfile.rstrip('/') + "_" + str(c)
        bfile = new_bfile
    return bfile
   
def syscall_print(syscall):
    text = syscall.format()
    if syscall.result is not None:
        text = "%-40s = %s" % (text, syscall.result_text)
    prefix = []
    prefix.append("[%s]" % syscall.process.pid)
    if prefix:
        text = ''.join(prefix) + ' ' + text
    print(text)

class ehandler:
    def __init__(self):
        self.opath = "files"
        if os.path.exists(self.opath):
            print("{:} already exists. Exiting.".format(self.opath))
            exit(1)
        pass
    def syscall_enter(self, syscall):
        #syscall_print(syscall)

        if syscall.name == "unlink":
            syscall_print(syscall)

            # prepare path of file to save
            targetname = syscall.arguments[0].getText().strip('\'')
            if os.path.isabs(targetname) == False:
                cwd = ptrace.linux_proc.readProcessLink(syscall.process.pid, 'cwd')
                targetname = os.path.join(cwd, targetname)
            targetname = os.path.realpath(targetname)

            # prepare path of backup file and copy the contents
            bfile = os.path.join(self.opath, targetname.strip('/'))
            bfile = os.path.realpath(bfile)
            if not os.path.isdir(targetname):
                bfile = prep_backupfile(bfile, syscall.process.pid)
                print("{:}: copy {:} to {:}".format(syscall.process.pid, targetname, bfile))
                shutil.copyfile(targetname, bfile)

        if syscall.name == "unlinkat":
            syscall_print(syscall)

            # prepare path of file to save
            targetname = syscall.arguments[1].getText().strip('\'')

            if os.path.isabs(targetname) == False:
                arg0 = ptrace.ctypes_tools.uint2int32(syscall.arguments[0].value)
                
                #if syscall.arguments[0].value < 0:  # AT_FDCWD
                if arg0 < 0:  # AT_FDCWD
                    cwd = ptrace.linux_proc.readProcessLink(syscall.process.pid, 'cwd')
                    targetname = os.path.join(cwd, targetname)
                else: # use value as filedescriptor
                    fd_dir = ptrace.linux_proc.readProcessLink(syscall.process.pid, "fd/{:}".format(arg0))
                    targetname = os.path.join(fd_dir, targetname)
            targetname = os.path.realpath(targetname)

            # prepare path of backup file and copy the contents
            bfile = os.path.join(self.opath, targetname.strip('/'))
            bfile = os.path.realpath(bfile)
            if not os.path.isdir(targetname):
                bfile = prep_backupfile(bfile, syscall.process.pid)
                print("{:}: copy {:} to {:}".format(syscall.process.pid, targetname, bfile))
                shutil.copyfile(targetname, bfile)
                   



    def syscall_exit(self, syscall):
        pass
    def process_new(self, process):
        process.cmd = []
    def process_exec(self, process):
        # assign process command line to process object
        process.cmd = ptrace.linux_proc.readProcessCmdline(process.pid)
        print("{:}: {:}".format(process.pid, process.cmd))


