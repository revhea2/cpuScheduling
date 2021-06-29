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
        #this array for the illustration of gantt
        self.gantt_chart = []

        self.processes = processes
        # sets the time and queue
        time = 0
        queue = []

        # initializes current process
        current_process = None
        process_list = []

        # start of fcfs
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
            if current_process.current_burst_time == 0:

                # for the tabulation of the processes in FCFS algorithm -- >
                current_process.completion_time = time
                current_process.waiting_time = current_process.start_time - current_process.arrival_time
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
                    current_process.start_time = time

                    # for illustration of gantt chart
                    self.gantt_chart.append(current_process)

                # if there is none, then there are no more processes to be executed
                else:
                    current_process = None

            # terminates the program since there are no processes to be executed
            if current_process is None:
                break


            # updates the total units of time taken
            time += 1
            # decrements the burst time of the current process
            current_process.current_burst_time -= 1

        # for illustration of gantt chart
        self.gantt_chart[-1].interval = time - self.gantt_chart[-1].start_time

        # for the tabulation of the FCFS algorithm
        self.table = Table(process_list)
