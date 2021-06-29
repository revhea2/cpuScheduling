from model.PreemptiveTable import PreemptiveTable
from model.Process import Process


class MultilevelQueue:

    def __init__(self):
        self.table = None
        self.gantt_chart = []
        self.table = []

    def has_arriving_process(self, time, processes):
        for i in range(len(processes)):
            if processes[i].arrival_time == time:
                return i
        return -1

    def add_waiting_queue_time(self, queue):
        for i in range(len(queue)):
            if queue[i].start_time is not None:
                queue[i].waiting_queue_time += 1

    def add_all_arriving_per_processes_queue_level(self, time, processes, queue, level):
        n = self.has_arriving_process(time, processes)

        # if there are arriving processes
        while n >= 0:
            process = processes.pop(n)
            process.current_burst_time = process.burst_time
            queue[level].append(process)

            n = self.has_arriving_process(time, processes)

    def perform_multilevel_queue(self, processes_1, processes_2, processes_3):

        self.gantt_chart = []
        queue = [
            [],
            [],
        ]

        quantum_slice = 5
        slice_count = quantum_slice
        current_process = None
        process_list = []
        time = 0
        level = 0

        while True:
            self.add_all_arriving_per_processes_queue_level(time, processes_1, queue, 0)
            self.add_all_arriving_per_processes_queue_level(time, processes_2, queue, 1)

            if current_process is None:
                current_process = queue[level].pop(0)
                current_process.start_time = time

                # for the illustration of gantt chart
                self.gantt_chart.append(current_process)

            if level == 0:


                if current_process.current_burst_time == 0:
                    current_process.completion_time = time
                    current_process.partial_waiting_time = current_process.start_time - current_process.arrival_time
                    current_process.waiting_time = current_process.waiting_queue_time + current_process.partial_waiting_time
                    current_process.turn_around_time = current_process.waiting_time + current_process.burst_time
                    process_list.append(current_process)

                    if len(queue[0]) > 0:
                        self.gantt_chart[-1].interval = time - self.gantt_chart[-1].start_time
                        current_process = queue[level].pop(0)

                        if current_process.start_time is None:
                            current_process.start_time = time
                        gantt_process = Process(current_process.name, current_process.arrival_time,
                                                current_process.burst_time)
                        gantt_process.start_time = time

                        self.gantt_chart.append(gantt_process)

                        slice_count = quantum_slice
                    else:
                        current_process = None

                else:
                    if len(queue[0]) > 0:
                        if slice_count == 0:

                            self.gantt_chart[-1].interval = time - self.gantt_chart[-1].start_time

                            temp = queue[0].pop(0)
                            queue[0].append(current_process)
                            current_process = temp
                            if current_process.start_time is None:
                                current_process.start_time = time

                            gantt_process = Process(current_process.name, current_process.arrival_time,
                                                    current_process.burst_time)
                            gantt_process.start_time = time
                            self.gantt_chart.append(gantt_process)
                            slice_count = quantum_slice
                    else:
                        if slice_count == 0:
                            self.gantt_chart[-1].interval = time - self.gantt_chart[-1].start_time

                            gantt_process = Process(current_process.name, current_process.arrival_time,
                                                    current_process.burst_time)
                            gantt_process.start_time = time
                            self.gantt_chart.append(gantt_process)

                if current_process is None and len(processes_1) == 0:
                    self.gantt_chart[-1].interval = time - self.gantt_chart[-1].start_time
                    level = 1
                    continue

                self.add_waiting_queue_time(queue[0])
                time += 1
                current_process.current_burst_time -= 1
                slice_count -= 1

            else:
                if current_process.current_burst_time == 0:
                    current_process.completion_time = time
                    current_process.partial_waiting_time = current_process.start_time - current_process.arrival_time
                    current_process.waiting_time = current_process.waiting_queue_time + current_process.partial_waiting_time
                    current_process.turn_around_time = current_process.waiting_time + current_process.burst_time
                    process_list.append(current_process)

                    if len(queue[level]) > 0:
                        self.gantt_chart[-1].interval = time - self.gantt_chart[-1].start_time
                        current_process = queue[level].pop(0)

                        gantt_process = Process(current_process.name, current_process.arrival_time,
                                                current_process.burst_time)
                        gantt_process.start_time = time
                        self.gantt_chart.append(gantt_process)

                        if current_process.start_time is None:
                            current_process.start_time = time

                    else:
                        current_process = None

                else:
                    if len(queue[level]) > 0:

                        if queue[level][0].current_burst_time < current_process.current_burst_time:
                            self.gantt_chart[-1].interval = time - self.gantt_chart[-1].start_time

                            # swap if the remaining time in the queue is lesser
                            queue[level][0], current_process = current_process, queue[level][0]
                            current_process.start_time = time

                            # for the gantt chart visual
                            self.gantt_chart.append(current_process)

                if current_process is None:
                    break

                self.add_waiting_queue_time(queue[1])
                time += 1
                current_process.current_burst_time -= 1

        self.gantt_chart[-1].interval = time - self.gantt_chart[-1].start_time
        self.gantt_chart.append(Process("", 0, 0, start_time= self.gantt_chart[-1].interval +self.gantt_chart[-1].start_time))

        self.table = PreemptiveTable(process_list)

    def add_time_process(self, processes, additional_time):
        for i in range(processes):
            processes[i].start_time += additional_time
            processes[i].arrival_time += additional_time
            processes[i].completion_time = additional_time
