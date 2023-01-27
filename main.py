# core import of the alignment calculation algorithm
from algorithm import calculate_oc_alignments

# general ocpa import to help setting up testing environments
from localocpa.objects.log.importer.ocel import factory as ocel_import_factory
from localocpa.algo.discovery.ocpn import algorithm as ocpn_discovery_factory
from localocpa.objects.oc_petri_net.obj import ObjectCentricPetriNet

# imports for evaluation
import timeit
import tracemalloc
from helperfunctions import display_memory_details_top, display_memory_total
from test_ocpns import TestOCPNS

from visualization import alignment_viz
from alignment import Alignment, Move, DefinedModelMove, UndefinedModelMove, SynchronousMove, UndefinedSynchronousMove, LogMove

# Setting up the evaluation environment

use_own_test_case = True

dejure_ocpn = None
defacto_ocel = None

test_ocpns = TestOCPNS()
dejure_ocpn, defacto_filename = test_ocpns.inter_object_dependencies()
defacto_ocel = ocel_import_factory.apply(defacto_filename)

# Inform user
print()
print("Starting Evaluation")
print()

# Repetition
n = 1
do_memory = True
do_time = True

# Time analysis
if do_time:
    t = timeit.Timer(lambda:  calculate_oc_alignments(defacto_ocel, dejure_ocpn))
    result = t.timeit(n)

# Memory analysis
if do_memory:
    tracemalloc.start()

    resulting_alignment = calculate_oc_alignments(defacto_ocel, dejure_ocpn)

    snapshot = tracemalloc.take_snapshot()

# General analysis
variant_count = len(defacto_ocel.variants)
process_execution_count = len(defacto_ocel.process_executions)
event_count = len(defacto_ocel.process_execution_mappings.keys())
object_type_count = len(defacto_ocel.object_types)

place_count = len(dejure_ocpn.places)
transition_count = len(dejure_ocpn.transitions)
variable_arc_count = 0
for place in dejure_ocpn.places:
    for in_arc in place.in_arcs:
        if in_arc.variable:
            variable_arc_count += 1
    for out_arc in place.out_arcs:
        if out_arc.variable:
            variable_arc_count += 1

if do_memory:
    alignment_cost_total = 0
    alignment_count = 0
    for variant_id, alignment in resulting_alignment.items():
        alignment_count += 1
        alignment_cost_total += len(defacto_ocel.variants_dict[variant_id]) * alignment.get_cost()

# Print analysis results
print()
print("----------------------------------------")
print("-------------- Evaluation --------------")
print("----------------------------------------")
print()
if do_time:
    print(f"Execution time is {result / n} seconds")
print()
print("----------------------------------------")
print()
if do_memory:
    display_memory_total(snapshot)
print()
print("----------------------------------------")
print()
print(f"# Variants: {variant_count}")
print(f"# Process Executions: {process_execution_count}")
print(f"# Events: {event_count}")
print(f"# Object Types: {object_type_count}")
print(f"# Places: {place_count}")
print(f"# Transitions: {transition_count}")
print(f"# Variable Arcs: {variable_arc_count}")
if do_memory:
    print(f"# Total Alignment Cost: {alignment_cost_total}")
    print(f"Total alignment Count: {alignment_count}")

if do_memory:
    alignment_viz(next(iter(resulting_alignment.values())))
