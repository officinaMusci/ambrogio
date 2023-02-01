from threading import Event


# Event used to interrupt threads when exceptions are raised
exit_event = Event()

# Event used to pause threads
pause_event = Event()