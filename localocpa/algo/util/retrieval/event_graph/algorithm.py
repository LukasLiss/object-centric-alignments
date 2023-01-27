from localocpa.algo.util.retrieval.event_graph.versions import classic
from localocpa.objects.graph.event_graph.obj import EventGraph

CLASSIC = "classic"

VERSIONS = {CLASSIC: classic.apply}


def apply(ocel, variant=CLASSIC, parameters=None) -> EventGraph:
    return VERSIONS[variant](ocel, parameters=parameters)
