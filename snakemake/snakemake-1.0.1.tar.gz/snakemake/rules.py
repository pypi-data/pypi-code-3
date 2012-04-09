# -*- coding: utf-8 -*-

import os, re, sys
from snakemake.jobs import Job
from snakemake.io import IOFile, protected, temp
from snakemake.exceptions import MissingInputException, AmbiguousRuleException, CyclicGraphException, RuleException, ProtectedOutputException

__author__ = "Johannes Köster"

class Namedlist(list):
	"""
	A list that additionally provides functions to name items. Further,
	it is hashable, however the hash does not consider the item names.
	"""
	def __init__(self, toclone = None, fromdict = None):
		"""
		Create the object.
		
		Arguments
		toclone  -- another Namedlist that shall be cloned
		fromdict -- a dict that shall be converted to a Namedlist (keys become names) 
		"""
		super(Namedlist, self).__init__()
		self._names = dict()
		
		if toclone:
			self.extend(toclone)
			if isinstance(toclone, Namedlist):
				self.take_names(toclone.get_names())
		if fromdict:
			for key, item in fromdict.items():
				self.append(item)
				self.add_name(key)

	def add_name(self, name):
		"""
		Add a name to the last item.
		
		Arguments
		name -- a name
		"""
		self.set_name(name, len(self) - 1)
	
	def set_name(self, name, index):
		"""
		Set the name of an item.
		
		Arguments
		name  -- a name
		index -- the item index
		"""
		self._names[name] = index
		setattr(self, name, self[index])
			
	def get_names(self):
		"""
		Get the defined names as (name, index) pairs.
		"""
		for name, index in self._names.items():
			yield name, index
	
	def take_names(self, names):
		"""
		Take over the given names.
		
		Arguments
		names -- the given names as (name, index) pairs
		"""
		for name, index in names:
			self.set_name(name, index)
	
	def __hash__(self):
		return hash(tuple(self))

	def __str__(self):
		return " ".join(self)

class Rule:
	def __init__(self, name, workflow, lineno = None, snakefile = None):
		"""
		Create a rule
		
		Arguments
		name -- the name of the rule
		"""
		self.name = name
		self.message = None
		self.input = Namedlist()
		self.output = Namedlist()
		self.threads = 1
		self.regex_output = []
		self.wildcard_names = set()
		self.workflow = workflow
		self.lineno = lineno
		self.snakefile = snakefile

	def has_wildcards(self):
		"""
		Return True if rule contains wildcards.
		"""
		return bool(self.wildcard_names)

	def set_input(self, *input, **kwinput):
		"""
		Add a list of input files. Recursive lists are flattened.
		
		Arguments
		input -- the list of input files
		"""
		for item in input:
			self._set_inoutput_item(item, self.input)
		for name, item in kwinput.items():
			self._set_inoutput_item(item, self.input, name = name)

	def set_output(self, *output, **kwoutput):
		"""
		Add a list of output files. Recursive lists are flattened.
		
		Arguments
		output -- the list of output files
		"""
		for item in output:
			self._set_inoutput_item(item, self.output)
		for name, item in kwoutput.items():
			self._set_inoutput_item(item, self.output, name = name)
		
		for item in self.output:
			wildcards = item.get_wildcard_names()
			if self.wildcard_names:
				if self.wildcard_names != wildcards:
					raise SyntaxError("Not all output files of rule {} contain the same wildcards. ".format(self.name))
			else:
				self.wildcard_names = wildcards
			self.regex_output.append(item.regex())
	
	def _set_inoutput_item(self, item, inoutput, name=None):
		"""
		Set an item to be input or output.
		
		Arguments
		item     -- the item
		inoutput -- either a Namedlist of input or output items
		name     -- an optional name for the item
		"""
		if isinstance(item, str):
			item = IOFile.create(item)
		
		if isinstance(item, IOFile):
			inoutput.append(item)
			if name:
				inoutput.add_name(name)
		else:
			try:
				for i in item:
					self._set_inoutput_item(i, inoutput)
			except TypeError:
				raise SyntaxError("Input and output files must be specified as strings.")

	def set_message(self, message):
		"""
		Set the message that is displayed when rule is executed.
		"""
		self.message = message
	
	def set_threads(self, threads):
		self.threads = threads
		
	def _expand_wildcards(self, requested_output):
		""" Expand wildcards depending on the requested output. """
		if requested_output:
			wildcards = self.get_wildcards(requested_output)
			missing_wildcards = set(wildcards.keys()) - self.wildcard_names 
		elif self.has_wildcards():				
			missing_wildcards = self.wildcard_names
		else:
			return Namedlist(self.input), Namedlist(self.output), dict()
		
		if missing_wildcards:
			raise RuleException("Could not resolve wildcards in rule {}:\n{}".format(self.name, "\n".join(self.wildcard_names)), lineno = self.lineno, snakefile = self.snakefile)

		try:
			input = Namedlist(i.apply_wildcards(wildcards) for i in self.input)
			output = Namedlist(o.apply_wildcards(wildcards) for o in self.output)
			input.take_names(self.input.get_names())
			output.take_names(self.output.get_names())
			return input, output, wildcards
		except KeyError as ex:
			# this can only happen if an input file contains an unresolved wildcard.
			raise RuleException("Wildcards in input file of rule {} do not appear in output files:\n{}".format(self, str(ex)), lineno = self.lineno, snakefile = self.snakefile)

	@staticmethod
	def _get_missing_files(files):
		""" Return the tuple of files that are missing form the given ones. """
		return tuple(f for f in files if not os.path.exists(f))
	
	@staticmethod
	def _has_missing_files(files):
		""" Return True if any of the given files does not exist. """
		for f in files:
			if not os.path.exists(f):
				return True
		return False
	
	def run(self, requested_output = None, forceall = False, forcethis = False, give_reason = False, jobs = dict(), dryrun = False, touch = False, quiet = False, visited = set(), jobcounter = None):
		"""
		Run the rule.
		
		Arguments
		requested_output -- the optional requested output file
		forceall         -- whether all required rules shall be executed, even if the files already exist
		forcethis        -- whether this rule shall be executed, even if the files already exist
		jobs             -- dictionary containing all jobs currently queued
		dryrun           -- whether rule execution shall be only simulated
		visited          -- set of already visited pairs of rules and requested output
		"""
		if (self, requested_output) in visited:
			raise CyclicGraphException(self, lineno = self.lineno, snakefile = self.snakefile)
		visited.add((self, requested_output))
		
		input, output, wildcards = self._expand_wildcards(requested_output)
		
		if (output, self) in jobs:
			return jobs[(output, self)]
		
		missing_input_exceptions = list()
		protected_output_exceptions = list()
		
		files_produced_with_error = set()
		todo = set()
		produced = dict()
		for rule, file in self.workflow.get_producers(input, exclude=self):
			try:
				job = rule.run(
					file, 
					forceall = forceall, 
					jobs = jobs, 
					dryrun = dryrun, 
					give_reason = give_reason,
					touch = touch, 
					quiet = quiet, 
					visited = set(visited), 
					jobcounter = jobcounter)
				if file in produced:
					raise AmbiguousRuleException(produced[file], rule, lineno = self.lineno, snakefile = self.snakefile)
				if job.needrun:
					todo.add(job)
				produced[file] = rule
			except (ProtectedOutputException, MissingInputException) as ex:
				if isinstance(ex, ProtectedOutputException):
					protected_output_exceptions.append(ex)
				else:
					missing_input_exceptions.append(ex)
				files_produced_with_error.add(file)
		
		missing_input = self._get_missing_files(set(input) - produced.keys())
		if missing_input:
			raise MissingInputException(
				rule = self,
				files = set(missing_input) - files_produced_with_error, 
				include = missing_input_exceptions,
				lineno = self.lineno, 
				snakefile = self.snakefile
			)
		
		need_run, reason = self._need_run(forcethis or forceall, todo, input, output)
		
		protected_output = self._get_protected_output(output) if need_run else None
		if protected_output or protected_output_exceptions:
			raise ProtectedOutputException(self, protected_output, include = protected_output_exceptions, lineno = self.lineno, snakefile = self.snakefile)
			
		for f in input:
			f.need()
			
		wildcards = Namedlist(fromdict = wildcards)
		
		job = Job(
			self.workflow,
			rule = self, 
			message = self.get_message(input, output, wildcards, reason if give_reason else None),
			input = input,
			output = output,
			wildcards = wildcards,
			threads = self.threads,
			depends = todo,
			dryrun = dryrun,
			touch = touch,
			needrun = need_run,
		)
		jobs[(output, self)] = job
		
		if jobcounter and need_run:
			jobcounter.add()
		
		return job

	@staticmethod
	def _get_protected_output(output):
		return [o for o in output if os.path.exists(o) and not os.access(o, os.W_OK)]

	def check(self):
		"""
		Check if rule is well defined.
		"""
		if self.output and not self.has_run():
			raise RuleException("Rule {} defines output but does not have a \"run\" definition.".format(self.name), lineno = self.lineno, snakefile = self.snakefile)

	def _need_run(self, force, todo, input, output):
		""" Return True if rule needs to be run. """
		if self.has_run():
			if force:
				return True, "Forced rule execution."
			if todo:
				todo_output = set()
				for job in todo:
					todo_output.update(job.output)
				return True, "Updated input files: {}".format(", ".join(set(input) & set(todo_output)))
			if self._has_missing_files(output):
				return True, "Missing output files: {}".format(", ".join(self._get_missing_files(output)))
			if not output:
				return True, ""
			mintime = min(o.mtime() for o in output)
			newer = [i for i in input if os.path.exists(i) and i.is_newer(mintime)]
			if newer:
				return True, "Input files newer than output files: {}".format(", ".join(newer))
			return False, ""
		return False, ""

	def get_run(self):
		""" Return the run method. """
		return self.workflow.get_run(self)

	def has_run(self):
		""" Return True if rule has a run method. """
		return self.workflow.has_run(self)

	def get_message(self, input, output, wildcards, reason, showmessage = True):
		"""
		Get the message that shall be printed upon rule execution.
		
		Arguments
		input       -- the input of the rule
		output      -- the output of the rule
		wildcards   -- the wildcards of the rule
		showmessage -- whether a user defined message shall be printed instead if existing  
		"""
		if self.message and showmessage:
			variables = dict(globals())
			variables.update(locals())
			msg = self.message.format(**variables)
			if reason:
				msg += "\n" + reason
			return msg

		msg = "rule " + self.name
		if input or output:
			msg += ":"
		if input:
			msg += "\n\tinput: {}".format(", ".join(input))
		if output:
			msg += "\n\toutput: {}".format(", ".join(output))
		if reason:
			msg += "\n\t" + reason
		return msg

	def is_producer(self, requested_output):
		"""
		Returns True if this rule is a producer of the requested output.
		"""
		for o in self.regex_output:
			match = re.match(o, requested_output)
			if match and len(match.group()) == len(requested_output):
				return True
		return False

	def get_wildcards(self, requested_output):
		"""
		Update the given wildcard dictionary by matching regular expression output files to the requested concrete ones.
		
		Arguments
		wildcards -- a dictionary of wildcards
		requested_output -- a concrete filepath
		"""
		bestmatchlen = 0
		bestmatch = None
		for o in self.regex_output:
			match = re.match(o, requested_output)
			if match and len(match.group()) == len(requested_output):
				l = self.get_wildcard_len(match.groupdict())
				if not bestmatch or bestmatchlen > l:
					bestmatch = match.groupdict()
					bestmatchlen = l
		return bestmatch
	
	@staticmethod
	def get_wildcard_len(wildcards):
		"""
		Return the length of the given wildcard values.
		
		Arguments
		wildcards -- a dict of wildcards
		"""
		return sum(map(len, wildcards.values()))

	def __repr__(self):
		return self.name
