"""This module provides two classes to represent a full or a compressed form of Collatz sequence."""

import itertools
from typing import Tuple

import networkx as nx

class Syracuse():
	"""
	A (full) Collatz sequence instanciated with a given initial value.
	
	The instance is iterable, and gives the successive values of the Collatz sequence.
	
	!!! example
	
		```python linenums="1"
		syracuse = Syracuse(1000)
		for value in syracuse:
			print(value)
			if value == 1:
				break
		```
	
	Be aware that a Collatz sequence is infinite: once it reaches 1 (and that is apparently the case for all tested initial values until now !), the cycle 4,2,1 returns indefinitely. So make sure you have implemented a stopping condition when you iterate over the sequence.
	
	For each sequence an underlying, directional graph is implemented, and is populated the first time several attributes are read (like `total_stopping_time`, `max` and of course `graph_view`), resulting an additionnal computing duration, that can be noticeable on "big" sequences. But the duration becomes imperceptible next times those attributes are read.
	
	Furthermore, a "global" graph can be optionaly initialized, and is shared with all instances. It is principally useful to work on a large number of sequences. If a global graph population is asked during a sequence instantiation, then the local graph is automatically generated and it populates the global graph just after. Be aware that the global graph activation generates a significant amount of additional computation time.
	
	Parameters:
		initial:
			Initial value of the Collatz sequence. Must be strictly positive.
		populate_global_graph:
			If `True`, a global graph is built, and populated with the graph of the current sequence. Default is `False`
	
	Attributes:
		initial_value:
			Reminder of the initial value given for the sequence initialisation. **read-only**
		stopping_time:
			The smallest rank such that the value becomes lower than the initial one. **read-only**
		total_stopping_time:
			The smallest rank such that the value equals 1. **read-only**
		total_stopping_sequence:
			Tuple of the sequence from the initial value, to 1. **read-only**
		max:
			Maximum value of the sequence. **read-only**
		max_rank:
			Rank of the maximum value of the sequence. **read-only**
		graph_view:
			A dict-like structure representing the graph of the successive members of the current sequence. **read-only**
		global_graph (networkx.Digraph):
			The global graph shared with all sequences, gathering in the same graph all sequences' graphs instanciated with `populate_global_graph = True`. **read-only**
		
	Raises:
		ValueError:
			if `initial` is not a strictly positive integer
	"""
	
	global_graph:nx.DiGraph = nx.DiGraph()
	
	
	def __init__(self, initial:int, populate_global_graph:bool = False):
		# syracuse instance initialisation
		if not isinstance(initial, int) or (initial <= 0):
			raise ValueError
		else:
			self._initial = initial
			self._stopping_time = 0
			self._graph = nx.DiGraph()
			self._local_graph_completed = False # Flag switching to True when the instance's graph is complete
			self._populate_global_graph = populate_global_graph
			if self._populate_global_graph:
				self._generate_graph()
	
	def __iter__(self):
		# The Syracuse instance is iterable, and gives the successive values of the Collatz sequence
		Un = self._initial
		yield Un # Don't forget to yield the initial value !
		while True:
			Un = Un*3+1 if Un%2 else Un//2
			yield Un
	
	@property
	def initial_value(self) -> int:
		# Reminder of the initial value given for the sequence initialisation (read-only attribute)
		return self._initial
	
	@property
	def stopping_time(self) -> int:
		# The smallest rank such that the value becomes lower than the initial one (read-only attribute)
		#
		# The Collatz conjecture asserts that this rank is finite for every initial value strictly greater than 1. Postulating this, if `initial_value` == 1, then `stopping_time` returns 0
		
		if self._stopping_time == 0:
			if self._initial == 1:
				return self._stopping_time
			else:
				for index, value in enumerate(self):
					if value < self._initial:
						self._stopping_time = index
						return self._stopping_time
						break
		else:
			return self._stopping_time

	@property
	def total_stopping_time(self) -> int:
		# The smallest rank such that the value equals 1 (read-only attribute)
		#
		# The Collatz conjecture asserts that this rank is finite for every initial value.
		
		self._generate_graph()
		return len(self._graph) - 1
	
	@property
	def total_stopping_sequence(self) -> Tuple[int]:
		# Tuple of the sequence from the initial value, to 1 (read-only attribute)
		self._generate_graph()
		return tuple(self._graph.nodes)
	
	@property
	def max(self) -> int:
		# Maximum value of the sequence (read-only attribute)
		return max(self.total_stopping_sequence)
	
	@property
	def max_rank(self) -> int:
		# Rank of the maximum value of the sequence (read-only attribute)
		return self.total_stopping_sequence.index(self.max)
	
	@property
	def graph_view(self) -> dict:
		# A dict-like structure representing the graph of the successive members of the current sequence (read-only attribute)
		return self._graph.adj
	
	
	def _generate_graph(self):
		"""Generate the internal, (directed) graph for the current sequence"""
		if not self._local_graph_completed:
			if self._initial not in self.global_graph:
				for Un in self:
					if Un == self._initial:
						self._graph.add_node(Un)
					else:
						self._graph.add_edge(previous,Un)
					previous = Un
					
					if Un == 1:
						self._local_graph_completed = True
						break
				
				if self._populate_global_graph:
					self.global_graph.add_edges_from(self._graph.edges)
			else:
				self._graph = nx.path_graph(nx.shortest_path(self.global_graph, source=self._initial, target=1), create_using=nx.DiGraph)
				self._local_graph_completed = True
	
	
	@classmethod
	def generate_global_graph(cls, max_initial_value:int, min_initial_value:int = 1) -> nx.DiGraph:
		"""Generate a global graph gathering all Collatz sequences with initial values from `min_initial_value` to `max_initial_value`.
		
		To populate the graph, this function temporarly instanciates the needed Syracuse objects, that can cause lot of memory consumtion; nevertheless each instance are deleted before the initialization of the next one.
		The resulting graph is stored in the class attribute `global_graph`, and is returned by this function too for convenience.
		
		Parameters:
			min_initial_value:
				The minimal initial value of the proceeded sequences (default is 1)
			max_initial_value:
				The maximal initial value of the proceeded sequences
		
		Returns:
			networkx.DiGraph: A representation of the global graph of the Collatz sequences.
		
		Raises:
			ValueError:
				if `min_initial_value` or `max_initial_value` are `max_initial_value` is not a strictly positive integer
				if `max_initial_value` < `min_initial_value`
		"""
		if not isinstance(max_initial_value, int) or (max_initial_value <= 0):
			raise ValueError("max_initial_value must be a strictly positive integer")
		elif not isinstance(min_initial_value, int) or (min_initial_value <= 0):
			raise ValueError("min_initial_value must be a strictly positive integer")
		elif max_initial_value < min_initial_value:
			raise ValueError("max_initial_value must be greater than min_initial_value")
		else:
			for initial in range(min_initial_value, max_initial_value+1):
				cls(initial, populate_global_graph = True)
			return cls.global_graph
	
	@classmethod
	def total_stopping_times_range(cls, max_initial_value:int, min_initial_value:int = 1) -> Tuple[int]:
		"""Generate the tuple of the total stopping times of all Collatz sequences with initial values from `min_initial_value` to `max_initial_value`.
			
		Parameters:
			min_initial_value:
				The miniimal initial value of the proceeded sequences (default is 1)
			max_initial_value:
				The maximal initial value of the proceeded sequences
		
		Returns:
			The ordered total stopping times of the Collatz sequences
		
		Raises:
			ValueError:
				if `min_initial_value` or `max_initial_value` are `max_initial_value` is not a strictly positive integer
				if `max_initial_value` < `min_initial_value`
		"""
		if not isinstance(max_initial_value, int) or (max_initial_value <= 0):
			raise ValueError("max_initial_value must be a strictly positive integer")
		elif not isinstance(min_initial_value, int) or (min_initial_value <= 0):
			raise ValueError("min_initial_value must be a strictly positive integer")
		elif max_initial_value < min_initial_value:
			raise ValueError("max_initial_value must be greater than min_initial_value")
		else:
			total_stopping_times_list = []
			for initial in range(min_initial_value, max_initial_value+1):
				total_stopping_times_list.append(cls(initial).total_stopping_time)
			return tuple(total_stopping_times_list)
	
	@classmethod
	def max_reached_values_range(cls, max_initial_value:int, min_initial_value:int = 1) -> Tuple[int]:
		"""Generate the tuple of the maximal values reached in all Collatz sequences with initial values from `min_initial_value` to `max_initial_value`.
			
		Parameters:
			min_initial_value:
				The miniimal initial value of the proceeded sequences (default is 1)
			max_initial_value:
				The maximal initial value of the proceeded sequences
		
		Returns:
			A tuple with the ordered maximal reached values of the Collatz sequences
		
		Raises:
			ValueError:
				if `min_initial_value` or `max_initial_value` are `max_initial_value` is not a strictly positive integer
				if `max_initial_value` < `min_initial_value`
		"""
		if not isinstance(max_initial_value, int) or (max_initial_value <= 0):
			raise ValueError("max_initial_value must be a strictly positive integer")
		elif not isinstance(min_initial_value, int) or (min_initial_value <= 0):
			raise ValueError("min_initial_value must be a strictly positive integer")
		elif max_initial_value < min_initial_value:
			raise ValueError("max_initial_value must be greater than min_initial_value")
		else:
			max_reached_values_list = []
			for initial in range(min_initial_value, max_initial_value+1):
				max_reached_values_list.append(cls(initial).max)
			return tuple(max_reached_values_list)

class CompressedSyracuse(Syracuse):
	"""
	A compressed Collatz sequence instanciated with a given initial value.
	
	This class provides the same parameters, attributes and methods as the inherited Syracuse class.
	"""
	
	def __iter__(self):
		Un = self._initial
		yield Un # Don't forget to yield the initial value !
		while True:
			Un = (Un*3+1)//2 if Un%2 else Un//2
			yield Un