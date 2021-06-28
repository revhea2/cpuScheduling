class PTable:

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
        output = "P\tAT\tBT\tST\tCT\tWT\tTAT\n"
        for process in self.processes:
            output += f"{process.name}\t{process.arrival_time}\t{process.burst_time}\t{process.start_time}\t{process.completion_time}\t" \
                      f"{process.waiting_time}\t{process.turn_around_time}\n"

        output += f"Average waiting time: {self.average_waiting_time}\n"
        output += f"Average turn around time: {self.average_turn_around_time}\n"
        return output
