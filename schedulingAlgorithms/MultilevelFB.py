from model.PreemptiveTable import PreemptiveTable
from model.Process import Process

class MultilevelFB:
	def __init__(self):
		self.processes = []
		self.table = []
		self.gantt_chart = []
		self.tables = []

	# bubble sort because i can
	def sort(self, processes):
		for i in range(len(processes)):
			for j in range(len(processes) - i - 1):
				if processes[j].arrival_time > processes[j+1].arrival_time:
					extra = processes[j]
					processes[j] = processes[j+1]
					processes[j+1] = extra
		return processes


	def perform_multilevel_fb(self, processes):
		first_level = []
		second_level = []
		third_level = []
		# Lists that just contain which processes terminated at which queues
		first_level_finishers = []
		second_level_finishers = []
		third_level_finishers = []
		# Quantum levels for the first 2 queues
		first_quantum = 4
		second_quantum = 8
		# Tracker for the total time taken
		time = 0
		self.processes += processes
		self.processes = self.sort(self.processes)
		process_list = []

		while self.processes:
			process = self.processes.pop(0)
			first_level.append(process)

		print(first_level)
		while first_level:
			process = first_level.pop(0)
			if process.arrival_time > time:
				time = process.arrival_time
			new_burst = process.burst_time - first_quantum
			# Either the process lasted first_quantum time units
			# or process.burst_time units, depending on which is smaller
			# if process.burst_time units gets picked, then the process
			# is shorter than the quantum slice
			burst_time=min(process.burst_time, first_quantum)
			print(new_burst)
			waiting_time = time - process.arrival_time
			added_process = Process(process.name, process.arrival_time, burst_time=burst_time, interval=burst_time, start_time=time, waiting_time=waiting_time, turn_around_time=waiting_time+burst_time)

			# A new_burst that's <= 0 implies a completed process
			if new_burst <= 0:
				added_process.completion_time = burst_time + time
			# A new_burst that's > 0 implies demotion due to unfinished task
			else:
				process.burst_time -= first_quantum
				second_level.append(process)

			process.turn_around_time = added_process.turn_around_time
			process_list.append(added_process)
			self.gantt_chart.append(added_process)
			time += burst_time
			first_level_finishers.append(added_process)

		print(second_level)
		while second_level:
			process = second_level.pop(0)
			print(process.turn_around_time)
			if process.arrival_time > time:
				time = process.arrival_time
			new_burst = process.burst_time - second_quantum
			# Either the process lasted first_quantum time units
			# or process.burst_time units, depending on which is smaller
			# if process.burst_time units gets picked, then the process
			# is shorter than the quantum slice
			burst_time=min(process.burst_time, second_quantum)
			print(new_burst)
			waiting_time = time - process.arrival_time - process.turn_around_time
			added_process = Process(process.name, process.arrival_time, burst_time=burst_time, interval=burst_time, start_time=time, waiting_time=waiting_time, turn_around_time=waiting_time+burst_time, waiting_queue_time=waiting_time)

			# A new_burst that's <= 0 implies a completed process
			if new_burst <= 0:
				added_process.completion_time = burst_time + time
			# A new_burst that's > 0 implies demotion due to unfinished task
			else:
				process.burst_time -= second_quantum
				third_level.append(process)

			process_list.append(added_process)
			self.gantt_chart.append(added_process)
			time += burst_time
			second_level_finishers.append(added_process)
		
		while third_level:
			process = third_level.pop(0)
			self.gantt_chart.append(process)
			waiting_time = time - process.arrival_time - process.turn_around_time
			process.waiting_time = waiting_time
			process.start_time = time
			process.waiting_queue_time = waiting_time
			process.completion_time = process.start_time + process.burst_time
			process.interval = process.burst_time
			process.turn_around_time = process.waiting_time + process.burst_time
			process_list.append(process)
			time += process.burst_time
			third_level_finishers.append(process)

		self.table = PreemptiveTable(process_list)
		return (first_level_finishers,second_level_finishers,third_level_finishers, self.gantt_chart, self.table)


# USAGE lagay na lang to sa index.py:
    # fb = MultilevelFB()
    # first, second, third, gantt_chart, table = fb.perform_multilevel_fb(processes, processes_2, processes_3)
    # is_multilevel=False
    # print(f"First Level: {first}")
    # print(f"Second Level: {second}")
    # print(f"Third Level: {third}")
    # print(f"Gantt: {gantt_chart}")