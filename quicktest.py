# core import of the alignment calculation algorithm
import helperfunctions
from algorithm import calculate_oc_alignment_given_variant_id

from multiprocessing import Pool

# general ocpa import to help setting up testing environments
from localocpa.objects.log.importer.csv import factory as ocel_import_factory
from localocpa.objects.log.importer.ocel import factory as ocel_import_factory_json
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

from localocpa.algo.util.filtering.log.variant_filtering import filter_infrequent_variants
from localocpa.algo.util.filtering.log.activity_filtering import filter_infrequent_activities

filename = "sample-logs/bpi2017/BPI2017-Final.csv"
object_types = ["application", "offer"]
parameters = {"obj_names":object_types,
              "val_names":[],
              "act_name":"event_activity",
              "time_name":"event_timestamp",
              "sep":","}
print("Import started")
ocel = ocel_import_factory.apply(file_path= filename,parameters = parameters)
print("Import done")


filtered_ocel_activities = filter_infrequent_activities(ocel, 0.5)
filtered_ocel = filter_infrequent_variants(filtered_ocel_activities, 0.5)
# print(len(filtered_ocel.variants))

dejure_ocpn = ObjectCentricPetriNet(name="Silent Transition")

p1 = ObjectCentricPetriNet.Place(name="p1", object_type="application", initial=True)
dejure_ocpn.places.add(p1)
p2 = ObjectCentricPetriNet.Place(name="p2", object_type="application")
dejure_ocpn.places.add(p2)
p3 = ObjectCentricPetriNet.Place(name="p3", object_type="application")
dejure_ocpn.places.add(p3)
p4 = ObjectCentricPetriNet.Place(name="p4", object_type="application", final=True)
dejure_ocpn.places.add(p4)
p5 = ObjectCentricPetriNet.Place(name="p5", object_type="offer", initial=True)
dejure_ocpn.places.add(p5)
p6 = ObjectCentricPetriNet.Place(name="p6", object_type="offer")
dejure_ocpn.places.add(p6)
p7 = ObjectCentricPetriNet.Place(name="p7", object_type="offer")
dejure_ocpn.places.add(p7)
p8 = ObjectCentricPetriNet.Place(name="p8", object_type="offer", final=True)
dejure_ocpn.places.add(p8)

t1 = ObjectCentricPetriNet.Transition(name="Create application", label="Create application")
dejure_ocpn.transitions.add(t1)
t2 = ObjectCentricPetriNet.Transition(name="Accept", label="Accept")
dejure_ocpn.transitions.add(t2)
t3 = ObjectCentricPetriNet.Transition(name="Create offer", label="Create offer")
dejure_ocpn.transitions.add(t3)
t4 = ObjectCentricPetriNet.Transition(name="Send (mail and online)", label="Send (mail and online)")
dejure_ocpn.transitions.add(t4)
t5 = ObjectCentricPetriNet.Transition(name="Call", label="Call")
dejure_ocpn.transitions.add(t5)
t6 = ObjectCentricPetriNet.Transition(name="Validate", label="Validate")
dejure_ocpn.transitions.add(t6)
t7 = ObjectCentricPetriNet.Transition(name="s1", label="s1", silent=True)
dejure_ocpn.transitions.add(t7)
t8 = ObjectCentricPetriNet.Transition(name="s2", label="s2", silent=True)
dejure_ocpn.transitions.add(t8)

#1
dejure_ocpn.add_arc(ObjectCentricPetriNet.Arc(p1, t1))
dejure_ocpn.add_arc(ObjectCentricPetriNet.Arc(t1, p2))
dejure_ocpn.add_arc(ObjectCentricPetriNet.Arc(p2, t2))
dejure_ocpn.add_arc(ObjectCentricPetriNet.Arc(p5, t3))
dejure_ocpn.add_arc(ObjectCentricPetriNet.Arc(t2, p3))
# 6
dejure_ocpn.add_arc(ObjectCentricPetriNet.Arc(p3, t3))
dejure_ocpn.add_arc(ObjectCentricPetriNet.Arc(t3, p3))
dejure_ocpn.add_arc(ObjectCentricPetriNet.Arc(t3, p6))
dejure_ocpn.add_arc(ObjectCentricPetriNet.Arc(p6, t4))
dejure_ocpn.add_arc(ObjectCentricPetriNet.Arc(p3, t5))
# 11
dejure_ocpn.add_arc(ObjectCentricPetriNet.Arc(t5, p3))
dejure_ocpn.add_arc(ObjectCentricPetriNet.Arc(p3, t6))
dejure_ocpn.add_arc(ObjectCentricPetriNet.Arc(t8, p3))
dejure_ocpn.add_arc(ObjectCentricPetriNet.Arc(t4, p7))
dejure_ocpn.add_arc(ObjectCentricPetriNet.Arc(p7, t5))
# 16
dejure_ocpn.add_arc(ObjectCentricPetriNet.Arc(p7, t7))
dejure_ocpn.add_arc(ObjectCentricPetriNet.Arc(t5, p8))
dejure_ocpn.add_arc(ObjectCentricPetriNet.Arc(t7, p8))
dejure_ocpn.add_arc(ObjectCentricPetriNet.Arc(t6, p4))
dejure_ocpn.add_arc(ObjectCentricPetriNet.Arc(p4, t8))


# Alignments

# print(len(filtered_ocel_activities.variants))

for variant_key in filtered_ocel.variants_dict.keys():
    print("Start Alignment calculation")
    alignment = calculate_oc_alignment_given_variant_id(filtered_ocel, dejure_ocpn, variant_key, '%Y-%m-%d %H:%M:%S.%f')
    print("Done with alignment calculation")
    alignment_viz(alignment)
    break