from model.PreemptiveTable import PreemptiveTable


class RoundRobin:

    def __init__(self):
        self.processes = []
        self.table = None

    def has_arriving_process(self, time):
        for i in range(len(self.processes)):
            if self.processes[i].arrival_time == time:
                return i
        return -1


    def add_waiting_queue_time(self, queue):
        for i in range(len(queue)):
            if queue[i].start_time is not None:
                queue[i].waiting_queue_time += 1

    def perform_round_robin(self, processes, quantum_slice):
        self.processes = processes
        time = 0
        queue = []


        slice_count = quantum_slice
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
                current_process.partial_waiting_time = current_process.start_time - current_process.arrival_time
                current_process.waiting_time = current_process.waiting_queue_time + current_process.partial_waiting_time
                current_process.turn_around_time = current_process.waiting_time + current_process.burst_time
                process_list.append(current_process)

                if len(queue) > 0:
                    current_process = queue.pop(0)
                    if current_process.start_time is None:
                        current_process.start_time = time
                    slice_count = quantum_slice
                else:
                    current_process = None

            else:
                if len(queue) > 0:
                    if slice_count == 0:
                        # swap if the remaining time in the queue is lesser
                        temp = queue.pop(0)
                        queue.append(current_process)
                        current_process = temp
                        if current_process.start_time is None:
                            current_process.start_time = time
                        slice_count = quantum_slice

            if current_process is None and len(queue) and len(self.processes):
                break

            self.add_waiting_queue_time(queue)
            time += 1
            current_process.current_burst_time -= 1
            slice_count -= 1

        self.table = PreemptiveTable(process_list)
