from model.Process import Process
from schedulingAlgorithms.FirstComeFirstServe import FirstComeFirstServe
from schedulingAlgorithms.RoundRobin import RoundRobin
from schedulingAlgorithms.ShortestJobFirst import ShortestJobFirst
from schedulingAlgorithms.PriorityQueue import PriorityQueue

from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html', table=table, gantt_chart=gantt_chart)


def sjf_np(_processes):
    sjf_ = ShortestJobFirst()
    sjf_.perform_np_shortest_job_first(_processes)

    gantt_chart = sjf_.gantt_chart

    print(sjf_.table)
    for process in sjf_.gantt_chart:
        print(process.name, process.start_time, process.interval)
    return sjf_.table


def sjf_p(_processes):
    sjf_ = ShortestJobFirst()
    sjf_.perform_p_shortest_job_first(_processes)
    print(sjf_.table)
    gantt_chart = sjf_.gantt_chart

    for process in sjf_.gantt_chart:
        print(process.name, process.start_time, process.interval)

    return sjf_.table


def fcfs(_processes):
    fcfs_ = FirstComeFirstServe()
    fcfs_.perform_np_first_come_first_serve(_processes)
    print(fcfs_.table)

    for process in fcfs_.gantt_chart:
        print(process.name, process.start_time, process.interval)

    gantt_chart = fcfs_.gantt_chart

    return fcfs_.table


def priority_queue_np(_processes):
    pq = PriorityQueue()
    pq.perform_np_priority_queue(_processes)
    print(pq.table)

    for process in pq.gantt_chart:
        print(process.name, process.start_time, process.interval)

    gantt_chart = pq.gantt_chart
    return pq.table


def priority_queue_p(_processes):
    pq = PriorityQueue()
    pq.perform_p_priority_queue(_processes)
    print(pq.table)

    for process in pq.gantt_chart:
        print(process.name, process.arrival_time, process.start_time, process.interval)

    gantt_chart = pq.gantt_chart
    return pq.table


def round_robin(_processes):
    rr = RoundRobin()
    rr.perform_round_robin(_processes, 8)
    print(rr.table)
    for process in rr.gantt_chart:
        print(process.name)
    return rr.table


if __name__ == '__main__':
    processes = []
    gantt_chart = []
    #
    # with open('inputs/fcfs.txt') as f:
    #     Lines = f.readlines()
    #     for line in Lines:
    #         name, arrival_time, burst_time = line.split('\t')
    #         processes.append(Process(name, int(arrival_time), int(burst_time)))
    #
    # table = fcfs(processes)

    with open('inputs/priority.txt') as f:
        Lines = f.readlines()
        for line in Lines:
            name, arrival_time, burst_time, priority = line.split('\t')
            processes.append(Process(name, int(arrival_time), int(burst_time), priority=int(priority)))

    table = priority_queue_p(processes)

    # with open('inputs/rr.txt') as f:
    #     Lines = f.readlines()
    #     for line in Lines:
    #         name, arrival_time, burst_time = line.split('\t')
    #         processes.append(Process(name, int(arrival_time), int(burst_time)))
    #
    # table = round_robin(processes)

    app.run(debug=True)
