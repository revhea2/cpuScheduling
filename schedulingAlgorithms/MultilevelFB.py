from model.Table import Table
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


	def perform_multilevel_fb(self, processes_1, processes_2, processes_3):
		first_level = []
		second_level = []
		third_level = []
		# Lists that just contain which processes terminated at which queues
		first_level_finishers = []
		second_level_finishers = []
		third_level_finishers = []
		# Quantum levels for the first 2 queues
		first_quantum = 5
		second_quantum = 10
		# Tracker for the total time taken
		time = 0
		self.processes += processes_1 + processes_2 + processes_3
		self.processes = self.sort(self.processes)
		process_list = []

		while self.processes:
			process = self.processes.pop(0)
			first_level.append(process)

		print(first_level)
		while first_level:
			process = first_level.pop(0)
			new_burst = process.burst_time - first_quantum
			if new_burst <= 0:
				new_burst = 0
				# Either the process lasted first_quantum time units
				# or process.burst_time units, depending on which is smaller
				# if process.burst_time units gets picked, then the process
				# is shorter than the quantum slice
				added_process = Process(process.name, process.arrival_time, burst_time=min(process.burst_time, first_quantum), interval=min(process.burst_time, first_quantum), start_time=time, waiting_time=time-process.arrival_time, turn_around_time=time-process.arrival_time+min(process.burst_time, first_quantum))
				process_list.append(added_process)
				self.gantt_chart.append(added_process)
				time += min(process.burst_time, second_quantum)
				first_level_finishers.append(added_process)
			# If the process is not finished, demote it 
			else:
				process.burst_time -= first_quantum
				second_level.append(process)

		while second_level:
			process = second_level.pop(0)
			new_burst = process.burst_time - second_quantum
			if new_burst <= 0:
				new_burst = 0
				added_process = Process(process.name, process.arrival_time, burst_time=min(process.burst_time, second_quantum), start_time=time, interval=min(process.burst_time, second_quantum), waiting_time=time-process.arrival_time, turn_around_time=time-process.arrival_time+min(process.burst_time, second_quantum))
				process_list.append(added_process)
				time += min(process.burst_time, second_quantum)
				self.gantt_chart.append(added_process)
				second_level_finishers.append(added_process)
			else:
				process.burst_time -= second_quantum
				third_level.append(process)
		
		while third_level:
			process = third_level.pop(0)
			process.interval = process.burst_time
			process.start_time = time
			time += process.burst_time
			self.gantt_chart.append(process)
			process_list.append(added_process)
			third_level_finishers.append(process)
		
		self.table = Table(process_list)
		return (first_level_finishers,second_level_finishers,third_level_finishers, self.gantt_chart, self.table)


# USAGE lagay na lang to sa index.py:
    # fb = MultilevelFB()
    # first, second, third, gantt_chart, table = fb.perform_multilevel_fb(processes, processes_2, processes_3)
    # is_multilevel=False
    # print(f"First Level: {first}")
    # print(f"Second Level: {second}")
    # print(f"Third Level: {third}")
    # print(f"Gantt: {gantt_chart}")