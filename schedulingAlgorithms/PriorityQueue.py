from model.PreemptiveTable import PreemptiveTable
from model.Table import Table
from model.Process import Process


class PriorityQueue:

    def __init__(self):
        self.processes = []
        self.table = None
        self.gantt_chart = []

    def has_arriving_process(self, time):
        for i in range(len(self.processes)):
            if self.processes[i].arrival_time == time:
                return i
        return -1

    def sorted_insert(self, queue, process):
        for i in range(len(queue)):
            if process.priority < queue[i].priority:
                queue.insert(i, process)
                return
        queue.append(process)

    def perform_np_priority_queue(self, processes):
        self.gantt_chart = []
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
                self.sorted_insert(queue, process)

                n = self.has_arriving_process(time)

            if current_process is None:
                current_process = queue.pop(0)
                current_process.start_time = time

                self.gantt_chart.append(current_process)

            if current_process.current_burst_time == 0:
                current_process.completion_time = time
                current_process.waiting_time = current_process.start_time - current_process.arrival_time
                current_process.turn_around_time = current_process.waiting_time + current_process.burst_time
                process_list.append(current_process)

                if len(queue) > 0:
                    self.gantt_chart[-1].interval = time - self.gantt_chart[-1].start_time

                    current_process = queue.pop(0)
                    current_process.start_time = time

                    gantt_process = Process(current_process.name, current_process.arrival_time,
                                            current_process.burst_time)
                    gantt_process.start_time = time
                    self.gantt_chart.append(gantt_process)
                else:
                    current_process = None

            if current_process is None:
                break

            time += 1
            current_process.current_burst_time -= 1

        self.gantt_chart[-1].interval = time - self.gantt_chart[-1].start_time
        self.table = Table(process_list)

    def add_waiting_queue_time(self, queue):
        for i in range(len(queue)):
            if queue[i].start_time is not None:
                queue[i].waiting_queue_time += 1

    def perform_p_priority_queue(self, processes):
        self.gantt_chart = []

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
                self.sorted_insert(queue, process)

                n = self.has_arriving_process(time)

            if current_process is None:
                current_process = queue.pop(0)
                current_process.start_time = time

                self.gantt_chart.append(current_process)

            if current_process.current_burst_time == 0:
                current_process.completion_time = time
                current_process.partial_waiting_time = current_process.start_time - current_process.arrival_time
                current_process.waiting_time = current_process.waiting_queue_time + current_process.partial_waiting_time
                current_process.turn_around_time = current_process.waiting_time + current_process.burst_time

                process_list.append(current_process)

                if len(queue) > 0:
                    self.gantt_chart[-1].interval = time - self.gantt_chart[-1].start_time

                    current_process = queue.pop(0)

                    gantt_process = Process(current_process.name, current_process.arrival_time, current_process.burst_time )
                    gantt_process.start_time = time
                    self.gantt_chart.append(gantt_process)

                    if current_process.start_time is None:
                        current_process.start_time = time
                else:
                    current_process = None

            else:
                if len(queue) > 0:
                    if queue[0].priority < current_process.priority:
                        self.gantt_chart[-1].interval = time - self.gantt_chart[-1].start_time
                        # swap if the priority in the poll is lesser
                        queue[0], current_process = current_process, queue[0]
                        current_process.start_time = time

                        self.gantt_chart.append(current_process)

            if current_process is None and len(queue) == 0 and len(self.processes) == 0:
                break

            self.add_waiting_queue_time(queue)
            time += 1
            current_process.current_burst_time -= 1

        self.gantt_chart[-1].interval = time - self.gantt_chart[-1].start_time

        self.table = PreemptiveTable(process_list)
