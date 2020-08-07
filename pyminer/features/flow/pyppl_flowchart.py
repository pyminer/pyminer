"""Flowchart generator for PyPPL."""
from pathlib import Path
from copy import deepcopy
from graphviz import Digraph # pylint: disable=import-error
from pyppl.plugin import hookimpl
from pyppl.logger import logger

__version__ = "0.1.3"

THEMES = dict(
	default = dict(
		base = dict(
			shape     = 'box',
			style     = 'rounded,filled',
			fillcolor = '#ffffff',
			color     = '#000000',
			fontcolor = '#000000',
		),
		start = dict(
			style = 'filled',
			color = '#259229', # green
		),
		end = dict(
			style = 'filled',
			color = '#d63125', # red
		),
		procset = dict(
			style = 'filled',
			color = '#eeeeee', # almost white
		),
		edge = dict(),
		edge_hidden = dict(style = 'dashed'),
	),

	dark = dict(
		base = dict(
			shape     = 'box',
			style     = 'rounded,filled',
			fillcolor = '#555555',
			color     = '#ffffff',
			fontcolor = '#ffffff',
		),
		start = dict(
			style    = 'filled',
			color    = '#59b95d', # green
			penwidth = 2,
		),
		end = dict(
			style = 'filled',
			color = '#ea7d75', # red
			penwidth = 2,
		),
		procset = dict(
			style = 'filled',
			color = '#eeeeee', # almost white
		),
		edge = dict(),
		edge_hidden = dict(style = 'dashed'),
	)
)

ROOTGROUP = '__ROOT__'

class Flowchart:
	"""@API
	Draw flowchart for pipelines
	"""

	def __init__(self, fcfile, dotfile):
		"""@API
		The flowchart constructor
		@params:
			fcfile (file): The flowchart file.
			dotfile (file): The dot file.
		"""
		self.fcfile  = Path(fcfile)
		self.dotfile = Path(dotfile)
		fmt          = self.fcfile.suffix
		fmt          = 'svg' if not fmt else fmt[1:]
		self.graph   = Digraph('PyPPL', format = fmt)
		self.theme   = THEMES['default']
		self.nodes   = {}
		self.starts  = []
		self.ends    = []
		self.links   = []

	def set_theme(self, theme, base = 'default'):
		"""@API
		Set the theme to be used
		@params:
			theme (str|dict): The theme, could be the key of Flowchart.
				- THEMES or a dict of a theme definition.
			base (str): The base theme to be based on you pass custom theme
		"""
		if isinstance(theme, dict):
			self.theme = deepcopy(THEMES[base])
			for key, val in self.theme.items():
				val.update(theme.get(key, {}))
		elif not theme:
			self.theme = THEMES[base]
		else:
			self.theme = THEMES[theme]

	def add_node(self, node, role = None):
		"""@API
		Add a node to the chart
		@params:
			node (Proc): The process node
			role (str): Is it a starting node, an ending node or None. Default: `None`.
		"""
		if role == 'start' and node not in self.starts:
			self.starts.append(node)
		if role == 'end' and node not in self.ends:
			self.ends.append(node)
		gname = node.procset or ROOTGROUP
		if gname not in self.nodes:
			self.nodes[gname] = []
		if node not in self.nodes[gname]:
			self.nodes[gname].append(node)

	def add_link(self, node1, node2, has_hidden = False):
		"""@API
		Add a link to the chart
		@params:
			node1 (Proc): The first process node.
			node2 (Proc): The second process node.
			has_hidden (bool): Whether there are processes hidden along the link
		"""
		if not has_hidden and (node1, node2, True) in self.links:
			self.links.remove((node1, node2, True))

		if has_hidden and (node1, node2, False) in self.links:
			return

		if (node1, node2, has_hidden) not in self.links:
			self.links.append((node1, node2, has_hidden))

	def _assemble(self):
		"""
		Assemble the graph for printing and rendering
		"""
		# nodes
		for group, nodes in self.nodes.items():
			graph = self.graph if group == ROOTGROUP else Digraph("cluster_%s" % group)
			for node in nodes:
				# copy the theme
				theme  = deepcopy(self.theme['base'])
				if node in self.starts:
					theme.update(self.theme['start'])
				if node in self.ends:
					theme.update(self.theme['end'])
				if node.desc != 'No description.':
					theme['tooltip'] = node.desc
				graph.node(node.shortname, **{k:str(v) for k, v in theme.items()})
			if group != ROOTGROUP:
				graph.attr(label = group, **{k:str(v) for k,v in self.theme['procset'].items()})
				self.graph.subgraph(graph)

		# edges
		for node1, node2, has_hidden in self.links:
			self.graph.edge(
				node1.shortname,
				node2.shortname,
				**{k:str(v) for k,v in self.theme[
					'edge_hidden' if has_hidden else 'edge'].items()})

	def generate(self):
		"""@API
		Generate the dot file and graph file.
		"""
		self._assemble()
		self.graph.save(self.dotfile)
		self.graph.render(self.fcfile.parent.joinpath(self.fcfile.stem), cleanup = True)

def _get_mate(proc):
	nextprocs = proc.nexts
	ret = []
	for nproc in nextprocs:
		if nproc.config.flowchart_hide:
			ret.extend([(np[0], True) for np in _get_mate(nproc)])
		else:
			ret.append((nproc, False))
	return ret

def flowchart(ppl, fcfile = None, dotfile = None):
	"""
	Generate graph in dot language and visualize it.
	@params:
		dotfile (file): Where to same the dot graph.
			- Default: `None` (`path.splitext(sys.argv[0])[0] + ".pyppl.dot"`)
		fcfile (file):  The flowchart file.
			- Default: `None` (`path.splitext(sys.argv[0])[0] + ".pyppl.svg"`)
			- For example: run `python pipeline.py` will save it to `pipeline.pyppl.svg`
	@returns:
		(PyPPL): The pipeline object itself.
	"""
	fcfile  = fcfile or Path('.').joinpath('%s.pyppl.svg' % ppl.name)
	fcfile = Path(fcfile)
	dotfile = dotfile if dotfile else Path(fcfile).with_suffix('.dot')
	dotfile = Path(dotfile)

	fchart  = Flowchart(fcfile = fcfile, dotfile = dotfile)
	fchart.set_theme(ppl.procs[0].config.flowchart_theme)

	for start in ppl.starts:
		if start.config.flowchart_hide:
			raise ValueError('Cannot hide start process: %s' % start.name)
		fchart.add_node(start, 'start')
	for end in ppl.ends:
		if end.config.flowchart_hide:
			raise ValueError('Cannot hide end process: %s' % end.name)
		fchart.add_node(end, 'end')

	for proc in ppl.procs:
		if proc.config.flowchart_hide:
			if len(proc.depends) > 1 and len(proc.nexts) > 1:
				raise ValueError('Cannot hide processes [%s] with multiple \
					dependenders and multiple dependendees.' % proc.name)
			continue # pragma: no cover (wired this is not reported)
		fchart.add_node(proc)
		if not proc.nexts:
			continue

		for mproc, has_hidden in _get_mate(proc):
			fchart.add_link(proc, mproc, has_hidden)

	fchart.generate()
	logger.fchart('Flowchart file saved to: %s', fchart.fcfile)
	logger.fchart('DOT file saved to: %s', fchart.dotfile)
	return ppl

@hookimpl
def setup(config):
	"""Add default config"""
	config.config.flowchart_theme = None

@hookimpl
def logger_init(logger):
	"""Add log level"""
	logger.add_level('fchart')

@hookimpl
def proc_init(proc):
	"""Add config for process"""
	proc.add_config('flowchart_hide', default = False,
		converter = bool, runtime = 'ignore')

@hookimpl
def pyppl_init(ppl):
	"""Initiate pipeline"""
	ppl.add_method(flowchart, require = 'start')
