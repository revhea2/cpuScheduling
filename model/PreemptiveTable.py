class PreemptiveTable:

    def __init__(self, processes):
        self.processes = processes
        self.average_waiting_time = 0
        self.average_turn_around_time = 0
        self.calculate_avg_waiting_time()
        self.calculate_avg_turn_around_time()

    def calculate_avg_waiting_time(self):
        total = 0
        for process in self.processes:
            total += process.waiting_time
        self.average_waiting_time = total / len(self.processes)

    def calculate_avg_turn_around_time(self):
        total = 0
        for process in self.processes:
            total += process.turn_around_time
        self.average_turn_around_time = total / len(self.processes)

    def __str__(self):
        output = "P\tAT\tBT\tST\tWQT\tCT\tPWT\tWT\tTAT\n"
        for process in self.processes:
            output += f"{process.name}\t{process.arrival_time}\t{process.burst_time}\t{process.start_time}\t{process.waiting_queue_time}\t{process.completion_time}\t" \
                      f"{process.partial_waiting_time}\t{process.waiting_time}\t{process.turn_around_time}\n"

        output += f"Average waiting time: {round(self.average_waiting_time, 2)}\n"
        output += f"Average turn around time: {round(self.average_turn_around_time, 2)}\n"
        return output
