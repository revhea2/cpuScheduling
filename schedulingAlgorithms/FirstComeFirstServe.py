from model.Table import Table


class FirstComeFirstServe:

    def __init__(self):
        self.processes = []
        self.table = None
        self.gantt_chart = []

    def has_arriving_process(self, time):
        for i in range(len(self.processes)):
            if self.processes[i].arrival_time == time:
                return i
        return -1

    def perform_np_first_come_first_serve(self, processes):
        self.processes = processes
        time = 0
        queue = []

        current_process = None
        process_list = []
        while True:
            n = self.has_arriving_process(time)

            # if there are arriving processes
            while n >= 0:
                process = self.processes.pop(n)

                process.current_burst_time = process.burst_time
                queue.append(process)

                n = self.has_arriving_process(time)

            if current_process is None:
                current_process = queue.pop(0)
                current_process.start_time = time

            if current_process.current_burst_time == 0:
                current_process.completion_time = time
                current_process.waiting_time = current_process.start_time - current_process.arrival_time
                current_process.turn_around_time = current_process.waiting_time + current_process.burst_time
                process_list.append(current_process)

                if len(queue) > 0:
                    current_process = queue.pop(0)
                    current_process.start_time = time
                else:
                    current_process = None

            if current_process is None:
                break

            time += 1
            current_process.current_burst_time -= 1

        self.table = Table(process_list)

