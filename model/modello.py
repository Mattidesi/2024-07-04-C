from database.DAO import DAO
import networkx as nx

class Model:
    def __init__(self):
        self._grafo = nx.DiGraph()
        self.idMap = {}
        self._nodes = []
    def getYears(self):
        return DAO.getYears()

    def getShapes(self,year: int):
        return DAO.getShapes(year)

    def buildGraph(self,year: int,shape: str):
        self._grafo.clear()
        self._nodes = DAO.getAllNodes(year,shape)
        print( self._nodes)

        self._grafo.add_nodes_from( self._nodes)

        for node in self._grafo.nodes:
            self.idMap[node.id] = node

        edges = DAO.getAllEdges(year,shape,self.idMap)

        for edge in edges:
            if self._grafo.has_edge(edge.d1,edge.d2):
                pass
            else:
                self._grafo.add_edge(edge.d1,edge.d2,weight = edge.weight)

    def getGraphDetails(self):
        return len(self._grafo.nodes), len(self._grafo.edges)

    def getBestWeight(self):
        result = []

        for edge in self._grafo.edges.values():
            result.append((edge[0],edge[1],edge['weight']))

        result.sort(key = lambda x:x[2],reverse=True)

        return result[0:5]

