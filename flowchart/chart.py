"""FlowChart chart module
"""
import pygraphviz
import pygraphviz.graphviz

_ACTION_CREATE = 1

__all__ = ['FlowChart']


def stacks(func):
    """Decorator to create an edge from the last added node
    """
    def wrapper(self, *args, **kwargs):
        label = kwargs.pop('label', None)
        last = kwargs.pop('last', None)
        weight = kwargs.pop('weight', 0)
        node = func(self, *args, **kwargs)
        if last is None:
            last = self.last.pop()
        else:
            self.last.pop()
        if not isinstance(last, list):
            last = [last]
        for last_node in last:
            edge = self._edge(last_node, node)
            edge.attr['weight'] = weight
            if label is not None:
                edge.attr['xlabel'] = label
        self.last.append(node)
        return node
    return wrapper


class FlowChart(object):
    """FlowChart class
    """
    def __init__(self, start='START'):
        base = self.graph = pygraphviz.AGraph(name='chart', directed=True)
        self._id = 0
        self.graph.graph_attr['splines'] = 'ortho'
        self.graph.graph_attr['rank'] = 'min'
        self.graph.graph_attr['rankdir'] = 'TB'
        self.graph.graph_attr['size'] = '10,10'
        self.start_node = self._terminal(start)
        self.last = [self.start_node]

    def _swimlane(self, *nodes):
        subgraph = self.graph.subgraph()
        subgraph.graph_attr['rank'] = 'same'
        subgraph.graph_attr['rankdir'] = 'LR'
        for node in nodes:
            subgraph.add_node(node.get_name())
            # pygraphviz.graphviz.agsubnode(subgraph.handle, node.handle, _ACTION_CREATE)
            # pygraphviz.Node(subgraph, node.get_name(), node.handle)

    def _node(self, contents):
        name = 'node-{}'.format(self._id)
        self._id += 1
        self.graph.add_node(name)
        node = self.graph.get_node(name)
        # nodeh = pygraphviz.graphviz.agnode(self.graph.handle, name, _ACTION_CREATE)
        # node = pygraphviz.Node(self.graph, name, nodeh)
        node.attr['label'] = contents
        return node

    def _edge(self, last, node, label=None):
        # edgeh = pygraphviz.graphviz.agedge(self.graph.handle, last.handle,
        #                                    node.handle, label, _ACTION_CREATE)
        # return pygraphviz.Edge(self.graph, eh=edgeh, key=label)
        self.graph.add_edge(last.name, node.name, key=label)
        return self.graph.get_edge(last.name, node.name)

    def _terminal(self, contents):
        """Adds a start or end node

        This is a rounded rectangle
        """
        node = self._node(contents)
        node.attr['shape'] = 'rectangle'
        node.attr['style'] = 'rounded'
        return node

    def _shaped(self, contents, shape='rectangle'):
        """Adds a shaped graphviz node
        """
        node = self._node(contents)
        node.attr['shape'] = shape
        return node

    @contextmanager
    def side_process(self):
        self.tmp_graph = self.graph
        self.graph = self.graph.subgraph()
        self.graph.graph_attr['rank'] = 'same'
        self.graph.graph_attr['rankdir'] = 'LR'
        self.last.append(self.last[-1])
        yield
        self.last.pop()
        self.graph = self.tmp_graph

    @stacks
    def process(self, contents):
        """Adds a process node

        This is a rectangle
        """
        node = self._shaped(contents)
        return node

    @stacks
    def prepare(self, contents):
        """Adds a preparation node

        This is a hexagon
        """
        node = self._shaped(contents, 'hexagon')
        return node

    @stacks
    def decision(self, contents):
        """Adds a decision node

        This is a diamond
        """
        node = self._shaped(contents, 'diamond')
        return node

    def connector(self, contents):
        """Adds an unconnected connector node

        This is a circle
        """
        node = self._shaped(contents, 'circle')
        return node

    def flow(self, node, label=None, weight=0, last=None):
        """Create a directed edge to a node
        """
        if last is None:
            last = self.last[-1]
        edge = self._edge(last, node)
        if label is not None:
            edge.attr['xlabel'] = label
        edge.attr['weight'] = weight
        edge.attr['color'] = '#BDE5F8'
        edge.attr['fontcolor'] = '#00529B'
        # edge.attr['constraint'] = False
        return edge

    def fail(self, node, *args, **kwargs):
        """Create a red "fail" directed edge
        """
        edge = self.flow(node, 'fail', *args, **kwargs)
        edge.attr['color'] = '#FFBABA'
        edge.attr['fontcolor'] = '#D8000C'
        return edge

    def success(self, node, *args, **kwargs):
        """Create a green "success" directed edge
        """
        edge = self.flow(node, 'success', *args, **kwargs)
        edge.attr['color'] = '#DFF2BF'
        edge.attr['fontcolor'] = '#4F8A10'
        return edge

    def save(self, imagename='chart.png'):
        """Export this flowchart to an image or dot file
        """
        self.graph.layout('dot')
        # self.graph.write('chart.dot')
        self.graph.draw(imagename)
