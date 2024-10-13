python3 strace.py -f --show-pid --trace-exec --enter --event-handler=eh_examples/event_count/ehandler.py -- bash -c "/usr/bin/sleep 1; /usr/bin/sleep 1;/usr/bin/sleep 1"
