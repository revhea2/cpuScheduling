class NpProcess:

    def __init__(self, name, arrival_time, burst_time, start_time=None, completion_time=None, waiting_time=None,
                 turn_around_time=None, priority=None, current_burst_time=None):
        self.name = name
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.start_time = start_time
        self.completion_time = completion_time
        self.waiting_time = waiting_time
        self.turn_around_time = turn_around_time
        self.priority = priority
        self.current_burst_time = current_burst_time
