from model.PreemptiveTable import PreemptiveTable
from model.Process import Process


class RoundRobin:

    def __init__(self):
        self.processes = []
        self.table = None
        self.gantt_chart = []

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
        # this array for the illustration of gantt
        self.gantt_chart = []

        # gets the parameter value to the global processes
        # so that we can access all processes anywhere
        self.processes = processes

        # sets the time and queue
        time = 0
        queue = []

        # sets the slice count
        # slice count is the counter of how many quantum slice is left
        slice_count = quantum_slice

        # initializes current process
        # current process is the process being executed
        current_process = None

        # initializes the storage for the processes tabulation illustration of RR algorithm
        process_list = []

        # start of RR
        while True:
            # gets all the arriving processes --- >
            n = self.has_arriving_process(time)

            # add all arriving processes to the queue
            while n >= 0:
                process = self.processes.pop(n)

                process.current_burst_time = process.burst_time
                queue.append(process)

                n = self.has_arriving_process(time)

            # end of the block -- >

            # gets the available process in the queue if no process is being executed
            if current_process is None:
                current_process = queue.pop(0)
                current_process.start_time = time

                # for the illustration of gantt chart
                self.gantt_chart.append(current_process)

            # check if the process has terminated
            # current burst time is the remaining time left for the process before its completion
            if current_process.current_burst_time == 0:

                # for the tabulation illustration of the processes in RR algorithm -- >
                # this block adds the current process in the tabulation of RR algorithm
                current_process.completion_time = time
                current_process.partial_waiting_time = current_process.start_time - current_process.arrival_time
                current_process.waiting_time = current_process.waiting_queue_time + current_process.partial_waiting_time
                current_process.turn_around_time = current_process.waiting_time + current_process.burst_time
                process_list.append(current_process)
                # end block -- >

                # checks if there are any remaining processes in the queue
                if len(queue) > 0:
                    # for illustration of gantt chart
                    self.gantt_chart[-1].interval = time - self.gantt_chart[-1].start_time

                    # since the current process has been terminated
                    # dequeue the next process
                    # the dequeued process will be the new process that will be executed
                    current_process = queue.pop(0)

                    # sets the start time for the tabulation illustration of RR Algorithm
                    if current_process.start_time is None:
                        current_process.start_time = time


                    # for illustration of gantt chart
                    gantt_process = Process(current_process.name, current_process.arrival_time,
                                            current_process.burst_time)
                    gantt_process.start_time = time
                    self.gantt_chart.append(gantt_process)


                    # sets the slice count back to the original count
                    slice_count = quantum_slice

                # if there is none, then there are no more processes to be executed
                else:
                    current_process = None

            # if the process still has remaining current burst time
            # the process is not yet completed
            else:

                # checks if there are any remaining processes in the queue
                if len(queue) > 0:

                    # checks if there are any remaining processes in the queue
                    if slice_count == 0:
                        # for illustration of gantt chart
                        self.gantt_chart[-1].interval = time - self.gantt_chart[-1].start_time

                        # this is where the round happens
                        # current process is added to the end of queue since its time slice is up
                        temp = queue.pop(0)
                        queue.append(current_process)

                        # since the current process has been terminated (because of time slicing)
                        # dequeue the next process from the queue
                        # the dequeued process will be the new process that will be executed a.k.a current process
                        current_process = temp

                        # for illustration of gantt chart
                        if current_process.start_time is None:
                            current_process.start_time = time
                        gantt_process = Process(current_process.name, current_process.arrival_time,
                                                current_process.burst_time)
                        gantt_process.start_time = time
                        self.gantt_chart.append(gantt_process)

                        # sets the slice count back to the original count
                        slice_count = quantum_slice

                # no more remaining process left in the queue
                # this block is for illustration of gantt chart
                else:
                    if slice_count == 0:
                        self.gantt_chart[-1].interval = time - self.gantt_chart[-1].start_time
                        gantt_process = Process(current_process.name, current_process.arrival_time,
                                                current_process.burst_time)
                        gantt_process.start_time = time
                        self.gantt_chart.append(gantt_process)

            # terminates the program since there are no processes to be executed
            if current_process is None:
                break


            # adds the waiting queue time in every processes in the queue
            self.add_waiting_queue_time(queue)

            # updates the total units of time taken
            time += 1
            # decrements the burst time of the current process and the time slice
            current_process.current_burst_time -= 1
            slice_count -= 1

        # for illustration of gantt chart
        self.gantt_chart[-1].interval = time - self.gantt_chart[-1].start_time
        self.gantt_chart.append(
            Process("", 0, 0, start_time=self.gantt_chart[-1].interval + self.gantt_chart[-1].start_time))



        self.table = PreemptiveTable(process_list)
