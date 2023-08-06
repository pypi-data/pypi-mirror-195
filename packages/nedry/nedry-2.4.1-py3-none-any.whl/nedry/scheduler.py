
class ScheduledEvent(object):
    """
    Represents a single generic scheduled event
    """
    def __init__(self, time_seconds, expiry_time, event_type, handler, *event_data):
        self.handler = handler           # Function to run when time is up
        self.event_data = event_data     # Event data, passed as a list to handler
        self.time_seconds = time_seconds # Expiry time in seconds from now
        self.expiry_time = expiry_time   # Expiry time in absolute seconds, UTC timestamp
        self.event_type = event_type     # Event type (one of ScheduledEventType)

    def time_remaining_string(self):
        return timedelta(seconds=(int(self.expiry_time) - int(_utc_time())))

    def __str__(self):
        return "%s(%s, %s, %s)" % (self.__class__.__name__, self.expiry_time,
                                   self.event_type, self.event_data)

    def __repr__(self):
        return self.__str__()


class Scheduler(object):
    """
    Handles all scheduled events in a thread
    """
    def __init__(self):
        self._active_events = []
        self._thread = None
        self._stop_event = threading.Event()
        self._lock = threading.Lock()

    def has_active_events(self):
        with self._lock:
            event_count = len(self._active_events)

        return event_count

    def stop(self):
        if self._thread is not None:
            self._stop_event.set()
            self._thread.join()
            self._thread = None

    def start(self):
        if self._thread is None:
            # Remove all expired events
            utcnow = _utc_time()
            while self._active_events[0].expiry_time <= utcnow:
                self._active_events.pop(0)

            self._thread = threading.Thread(target=self._thread_task)
            self._thread.daemon = True
            self._thread.start()

    def set_discord_bot(self, bot):
        self._discord_bot = bot

    def all_events(self):
        with self._lock:
            for e in self._active_events:
                yield e

    def _handle_expired_events(self):
        with self._lock:
            while self._active_events and (self._active_events[0].expiry_time <= _utc_time()):
                event = self._active_events.pop(0)

                if not event:
                    return

                event.handler(event.event_data)

    def _thread_task(self):
        # Loop forever
        while True:
            if not self._active_events:
                # Exit if no active events
                return

            # Figure out how long to wait until the next expiry
            with self._lock:
                expiry_time = self._active_events[0].expiry_time

            utc_now = _utc_time()

            if (expiry_time + 1) < utc_now:
                time_until_expiry = 1
            else:
                time_until_expiry = expiry_time - utc_now

            stopped = self._stop_event.wait(time_until_expiry)
            if stopped:
                self._stop_event.clear()
                return

            self._handle_expired_events()

    def _add_active_event(self, event):
        # Need to maintain the list in order of timer expiry
        index = 0
        found_later_expiry = False

        for i in range(len(self._active_events)):
            if self._active_events[i].expiry_time > event.expiry_time:
                found_later_expiry = True
                index = i
                break

        if not found_later_expiry:
            index = len(self._active_events)

        self._active_events.insert(index, event)
        return index == 0

    def save_scheduled_events(self):
        if PLUGIN_NAME in self._discord_bot.config.config.plugin_data:
           del self._discord_bot.config.config.plugin_data[PLUGIN_NAME]

        scheduled_events = []
        for event in self._active_events:
            scheduled_events.append(event.to_json())

        self._discord_bot.config.config.plugin_data[PLUGIN_NAME] = scheduled_events
        self._discord_bot.config.save_to_file()

    def load_scheduled_events(self):
        events_loaded = 0
        if PLUGIN_NAME in self._discord_bot.config.config.plugin_data:
            with self._lock:
                for event_data in self._discord_bot.config.config.plugin_data[PLUGIN_NAME]:
                    event = ScheduledEvent.from_json(event_data)

                    if _utc_time() >= event.expiry_time:
                        # Event has already expired
                        continue

                    self._add_active_event(event)
                    events_loaded += 1

        return events_loaded

    def add_event(self, mins_from_now, event_type, handler, *event_data):
        expiry_time_secs = int(_utc_time() + (mins_from_now * 60))
        event = ScheduledEvent(mins_from_now * 60, expiry_time_secs, event_type, handler, *event_data)

        with self._lock:
            first_event = len(self._active_events) == 0
            if self._active_events:
                # Other events are active, stop the thread before modifying the list
                self.stop()

            self._add_active_event(event)

            # Save state of scheduled event queue
            self.save_scheduled_events()

        # (Re)Start thread
        self.start()

        return event

    def remove_events(self, events):
        with self._lock:
            for e in events:
                if e not in self._active_events:
                    raise ValueError()

            if self._active_events:
                # Other events are active, stop the thread before modifying the list
                self.stop()

            for e in events:
                self._active_events.remove(e)

        # (Re)Start thread
        self.start()

    def get_events_of_type(self, event_type):
        with self._lock:
            return [x for x in self._active_events if x.event_type == event_type]


