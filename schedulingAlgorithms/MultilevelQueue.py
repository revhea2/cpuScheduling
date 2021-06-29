from schedulingAlgorithms.FirstComeFirstServe import FirstComeFirstServe
from schedulingAlgorithms.RoundRobin import RoundRobin
from schedulingAlgorithms.ShortestJobFirst import ShortestJobFirst


class MultilevelQueue:

    def __init__(self):
        self.processes = []
        self.table = None
        self.gantt_chart_levels = []
        self.tables = []

    def perform_multilevel_queue(self, processes_1, processes_2, processes_3):
        rr = RoundRobin()
        rr.perform_round_robin(processes_1, 5)
        self.gantt_chart_levels.append(rr.gantt_chart)
        self.tables.append(rr.table)

        sjf_ = ShortestJobFirst()
        sjf_.perform_np_shortest_job_first(processes_2, rr.gantt_chart[-1].start_time)
        self.gantt_chart_levels.append(sjf_.gantt_chart)
        self.tables.append(sjf_.table)

        fcfs = FirstComeFirstServe()
        fcfs.perform_np_first_come_first_serve(processes_3, sjf_.gantt_chart[-1].start_time)
        self.gantt_chart_levels.append(fcfs.gantt_chart)
        self.tables.append(fcfs.table)
