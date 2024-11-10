from dataclasses import dataclass

from model.sighting import Sighting


@dataclass
class Edge:
    id1: Sighting
    id2: Sighting
    weight: float