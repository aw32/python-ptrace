This is a fork of `python-ptrace`. See the <https://github.com/vstinner/python-ptrace> for the original README.

This fork extends `strace.py` to support easier handling of events.
Use `--event-handler` to specify a Python script that handles strace events.
This allows for easy filtering of syscalls and reacting to interesting syscalls.
See the `eh_examples` folder for the following examples:

* `event_count`: Count specific syscalls from certain processes and delay the syscall execution.
* `call_gdb`: Catch a specific syscall from a specific process, detach from the process and attach using gdb.
* `backup`: Catch `unlink` and `unlinkat` syscalls and create backups of the (to be) deleted files.

Some functionality is only available, if `strace.py` is called with specific arguments, e.g. `--show-ip` for instruction pointer access.
See the `strace.py` code for the standard functionality to figure out how to access or print certain information.
