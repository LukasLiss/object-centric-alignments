# core import of the alignment calculation algorithm
import helperfunctions
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

from localocpa.visualization.oc_petri_net import factory as ocpn_vis_factory
from visualization import alignment_viz
from alignment import Alignment, Move, DefinedModelMove, UndefinedModelMove, SynchronousMove, UndefinedSynchronousMove, LogMove

from datetime import datetime

import matplotlib.pyplot as plt

# Setting up the evaluation environment

# ----------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------
x = []
y_time = []
y_memory = []

for size_of_net in range(12, 13, 1):
    for degree_of_parallelity_help in range(1, 10, 1):
        degree_of_parallelity = degree_of_parallelity_help / 10
        for fitness_help in range(8, 7, -1):
            fitness = fitness_help / 10

            x.append(degree_of_parallelity)

            dejure_ocpn, defacto_ocel = helperfunctions.create_evaluation_data(size_of_net, degree_of_parallelity, fitness)

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
                # if alignment exist then visualize it
                abbreviations = {
                    "Create Purchase Requisition": "CPR",
                    "Create Purchase Order": "CPO",
                    "Receive Goods": "RG",
                    "Issue Goods Receipt": "IGR",
                    "Verify Material": "VM",
                    "Plan Goods Issue": "PGI",
                    "Goods Issue": "GI",
                    "Receive Invoice": "RI",
                    "Clear Invoice": "CI",
                    "PURCHREQ": "PR",
                    "MATERIAL": "M",
                    "PURCHORD": "PO",
                    "GDSRCPT": "G",
                    "INVOICE": "I"

                }
                alignment_viz(next(iter(resulting_alignment.values())), abbreviations)

                y_time.append(result / n)
                y_memory.append(helperfunctions.get_mem_total(snapshot))

                # save information to file
                f = open("evaluation_results.txt", "a")
                f.write(f"{size_of_net};{degree_of_parallelity};{fitness};{result / n};{helperfunctions.get_mem_total(snapshot)}\n")
                f.close()

# visualize plots
fig, ax = plt.subplots()

ax.plot(x, y_time, ".r-")
# ax.set(xlabel="fitness", ylabel="time (s)", xlim=(max(x), min(x)))
#ax.set(xlabel="# transitions in de jure net", ylabel="time (s)")
ax.set(xlabel="fraction of parallel transitions", ylabel="time (s)")

plt.show()

# ----------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------

# create log

# pn, ocel = helperfunctions.create_evaluation_data(8, 0.5, 0.5)
# ocpn_vis_factory.save(ocpn_vis_factory.apply(pn), "my_created_pn_evaluation.png")
#
# resulting_alignment = calculate_oc_alignments(ocel, pn)
# alignment_viz(next(iter(resulting_alignment.values())))

print("Done")
