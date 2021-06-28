from flask import Flask

from model.Process import Process
from schedulingAlgorithms.non_preemptive.FirstComeFirstServe import FirstComeFirstServe
from schedulingAlgorithms.non_preemptive.ShortestJobFirst import ShortestJobFirst
from schedulingAlgorithms.non_preemptive.PriorityQueue import PriorityQueue

app = Flask(__name__)


def sjf(_processes):
    sjf_ = ShortestJobFirst()
    sjf_.perform_shortest_job_first(_processes)
    print(sjf_.table)


def fcfs(_processes):
    fcfs_ = FirstComeFirstServe()
    fcfs_.perform_first_come_first_serve(_processes)
    print(fcfs_.table)


def priority_queue(_processes):
    pq = PriorityQueue()
    pq.perform_priority_queue(_processes)
    print(pq.table)


if __name__ == '__main__':
    processes = []
    #
    # with open('inputs/fcfs.txt') as f:
    #     Lines = f.readlines()
    #     for line in Lines:
    #         name, arrival_time, burst_time = line.split('\t')
    #         processes.append(Process(name, int(arrival_time), int(burst_time)))
    #
    # sjf(processes)


    with open('inputs/priority.txt') as f:
        Lines = f.readlines()
        for line in Lines:
            name, arrival_time, burst_time, priority = line.split('\t')
            processes.append(Process(name, int(arrival_time), int(burst_time), int(priority)))

        priority_queue(processes)

    # app.run(debug=True)
