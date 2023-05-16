# Object-Centric-Alignments

The algorithm implemented in this repository, computes object-centric alignments.
An example of how to use the algorithm can be found in the getting-started-example jupyter notebook.

## Installation

To run the getting-started-example jupyter notebook one needs to install the requirements with pipenv:

```
pipenv install
```

## Usage

To compute object centric alignments one needs to import the function calculate_oc_alignments.
The visualization functionality is given by the alignment_viz function.
For the example we also import additional functionality that lets us import object-centric event logs and object-centric Petri nets.

```
# core import of the alignment calculation algorithm
from algorithm import calculate_oc_alignments

# import for visualization
from visualization import alignment_viz

# supporting imports to import object-centric event logs and object-centric Petri nets

# imports to load object-centric event logs and discover accepting object-centric Petri net
from localocpa.objects.log.importer.ocel import factory as ocel_import_factory_json
from localocpa.algo.discovery.ocpn import algorithm as ocpn_discovery_factory

# some example accepting object-centric petri nets
from test_ocpns import TestOCPNS
```

Here we will first of all import an object-centric event log.
Afterwards we will discover a perfectly fitting object-centric Petri net and we will also import a pre-defined one.

```
# load the object-centric event log
ocel_filename = "sample-logs/jsonocel/paper-example.jsonocel"
ocel = ocel_import_factory_json.apply(ocel_filename)

# discover a perfectly fitting accepting object centric petri net from the object-centric event log
discovered_ocpn = ocpn_discovery_factory.apply(ocel, parameters={"debug": False})

# load a predefined accepting object-centric Petri net that will detect deviations in the given object centric event log
ocpn = TestOCPNS().paper_example()[0]
```

Finally, we can compute the alignments and visualize them like shown in the following:

```
# align all the process execution in the event log with an accepting oject-centric Petri net
alignments_discovered_ocpn = calculate_oc_alignments(ocel, discovered_ocpn)
alignments_ocpn = calculate_oc_alignments(ocel, ocpn)

# visualize the alignment for the first process execution for both accepting object-centric Petri net
alignment_viz(next(iter(alignments_discovered_ocpn.values())))
alignment_viz(next(iter(alignments_ocpn.values())))
```