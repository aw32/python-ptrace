python3 strace.py -f --show-pid --show-ip --trace-exec --enter --event-handler=eh_examples/call_gdb/ehandler.py -- bash -c "/usr/bin/sleep 1"
