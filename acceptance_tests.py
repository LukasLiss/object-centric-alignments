import unittest

from algorithm import calculate_oc_alignments, all_valid_bindings, process_execution_net_from_process_execution, preprocessing_dejure_net, create_synchronous_product_net, dijkstra

from localocpa.objects.log.importer.ocel import factory as ocel_import_factory
from localocpa.algo.discovery.ocpn import algorithm as ocpn_discovery_factory

from localocpa.objects.oc_petri_net.obj import ObjectCentricPetriNet, Marking
from helperfunctions import FrozenMarking
from localocpa.objects.log.ocel import OCEL
import collections.abc
from alignment import Alignment

from test_ocpns import TestOCPNS

import copy

def get_total_cost_of_aligment(alignments, defacto_ocel):
    alignment_cost_total = 0
    for variant_id, alignment in alignments.items():
        alignment_cost_total += len(defacto_ocel.variants_dict[variant_id]) * alignment.get_cost()
    return alignment_cost_total


class TestObjectCentricAligments(unittest.TestCase):

    def setUp(self):
        # Dejure Model as a petri net
        self.ocpn = TestOCPNS().paper_example()[0]

        # OCEL used for process executions
        ocel_filename = "sample-logs/jsonocel/paper-example.jsonocel"
        self.ocel = ocel_import_factory.apply(ocel_filename)


    def test_single_variant_perfectly_aligned(self):
        # Dejure Model as a petri net
        dejure_filename = "sample-logs/jsonocel/p2p-normal.jsonocel"
        dejure_ocel = ocel_import_factory.apply(dejure_filename)
        dejure_ocpn = ocpn_discovery_factory.apply(dejure_ocel, parameters={"debug": False})

        # OCEL used for process executions
        defacto_filename = "sample-logs/jsonocel/p2p-normal-01-variant.jsonocel"
        defacto_ocel = ocel_import_factory.apply(defacto_filename)

        resulting_alignment = calculate_oc_alignments(defacto_ocel, dejure_ocpn)

        self.assertEqual(get_total_cost_of_aligment(resulting_alignment, defacto_ocel), 0)

    def test_multiple_variants(self):
        # Dejure Model as a petri net
        dejure_filename = "sample-logs/jsonocel/p2p-normal.jsonocel"
        dejure_ocel = ocel_import_factory.apply(dejure_filename)
        dejure_ocpn = ocpn_discovery_factory.apply(dejure_ocel, parameters={"debug": False})

        # OCEL used for process executions
        defacto_filename = "sample-logs/jsonocel/p2p-normal.jsonocel"
        defacto_ocel = ocel_import_factory.apply(defacto_filename)

        resulting_alignment = calculate_oc_alignments(defacto_ocel, dejure_ocpn)

        # all are perfectly fitting
        self.assertEqual(get_total_cost_of_aligment(resulting_alignment, defacto_ocel), 0)
        # each variant was aligned
        self.assertEqual(len(resulting_alignment.values()), len(defacto_ocel.variants_dict.keys()))

    def test_wrong_input_ocel(self):
        # Dejure Model as a petri net
        dejure_filename = "sample-logs/jsonocel/p2p-normal.jsonocel"
        dejure_ocel = ocel_import_factory.apply(dejure_filename)
        dejure_ocpn = ocpn_discovery_factory.apply(dejure_ocel, parameters={"debug": False})

        self.assertRaises(Exception, lambda: calculate_oc_alignments(None, dejure_ocpn))

    def test_wrong_input_pn(self):
        # OCEL used for process executions
        defacto_filename = "sample-logs/jsonocel/p2p-normal.jsonocel"
        defacto_ocel = ocel_import_factory.apply(defacto_filename)

        self.assertRaises(Exception, lambda: calculate_oc_alignments(defacto_ocel, None))

    def test_None_input_both(self):
        self.assertRaises(Exception, lambda: calculate_oc_alignments(None, None))

    def test_mixed_input_ocel_pn(self):
        # Dejure Model as a petri net
        dejure_filename = "sample-logs/jsonocel/p2p-normal.jsonocel"
        dejure_ocel = ocel_import_factory.apply(dejure_filename)
        dejure_ocpn = ocpn_discovery_factory.apply(dejure_ocel, parameters={"debug": False})

        # OCEL used for process executions
        defacto_filename = "sample-logs/jsonocel/p2p-normal-01-variant.jsonocel"
        defacto_ocel = ocel_import_factory.apply(defacto_filename)

        self.assertRaises(Exception, lambda: calculate_oc_alignments(dejure_ocpn, defacto_ocel))

    def test_paper_example(self):
        # Dejure Model as a petri net
        ocpn = TestOCPNS().paper_example()[0]

        # OCEL used for process executions
        ocel_filename = "sample-logs/jsonocel/paper-example.jsonocel"
        ocel = ocel_import_factory.apply(ocel_filename)

        resulting_alignment = calculate_oc_alignments(ocel, ocpn)


        self.assertEqual(get_total_cost_of_aligment(resulting_alignment, ocel), 6)

    def test_silent_transitions(self):
        # OCEL used for process executions
        ocel_filename = "sample-logs/jsonocel/paper-example.jsonocel"
        ocel = ocel_import_factory.apply(ocel_filename)

        # Dejure Model as a petri net
        discovered_ocpn = ocpn_discovery_factory.apply(ocel, parameters={"debug": False})

        resulting_alignment = calculate_oc_alignments(ocel, discovered_ocpn)


        self.assertLess(get_total_cost_of_aligment(resulting_alignment, ocel), 1)

    def test_nue_net_functionality(self):
        # Dejure Model as a petri net
        ocpn = TestOCPNS().nue_net_required()[0]

        # OCEL used for process executions
        ocel_filename = TestOCPNS().nue_net_required()[1]
        ocel = ocel_import_factory.apply(ocel_filename)

        resulting_alignment = calculate_oc_alignments(ocel, ocpn)


        self.assertGreaterEqual(get_total_cost_of_aligment(resulting_alignment, ocel), 1)

    def test_inter_object_dependencies_functionality(self):
        # Dejure Model as a petri net
        ocpn = TestOCPNS().inter_object_dependencies()[0]

        # OCEL used for process executions
        ocel_filename = TestOCPNS().inter_object_dependencies()[1]
        ocel = ocel_import_factory.apply(ocel_filename)

        resulting_alignment = calculate_oc_alignments(ocel, ocpn)


        self.assertGreaterEqual(get_total_cost_of_aligment(resulting_alignment, ocel), 1)

    def test_seperate_object_instances_functionality(self):
        # Dejure Model as a petri net
        ocpn = TestOCPNS().seperate_object_instances()[0]

        # OCEL used for process executions
        ocel_filename = TestOCPNS().seperate_object_instances()[1]
        ocel = ocel_import_factory.apply(ocel_filename)

        resulting_alignment = calculate_oc_alignments(ocel, ocpn)


        self.assertGreaterEqual(get_total_cost_of_aligment(resulting_alignment, ocel), 1)

    def test_single_shortest_path_functionality(self):
        # Dejure Model as a petri net
        ocpn = TestOCPNS().running_example()[0]

        # OCEL used for process executions
        ocel_filename = TestOCPNS().running_example()[1]
        ocel = ocel_import_factory.apply(ocel_filename)

        resulting_alignment = calculate_oc_alignments(ocel, ocpn)


        self.assertGreaterEqual(get_total_cost_of_aligment(resulting_alignment, ocel), 1)

    def test_skip_by_silent_functionality(self):
        # Dejure Model as a petri net
        ocpn = TestOCPNS().silent_transitions()[0]

        # OCEL used for process executions
        ocel_filename = TestOCPNS().silent_transitions()[1]
        ocel = ocel_import_factory.apply(ocel_filename)

        resulting_alignment = calculate_oc_alignments(ocel, ocpn)

        self.assertGreater(get_total_cost_of_aligment(resulting_alignment, ocel), 0)
        self.assertLess(get_total_cost_of_aligment(resulting_alignment, ocel), 1)

    def test_deviations_can_compensate(self):
        # Dejure Model as a petri net
        ocpn = TestOCPNS().paper_example()[0]

        # OCEL used for process executions
        ocel_filename = "sample-logs/jsonocel/paper-example.jsonocel"
        ocel = ocel_import_factory.apply(ocel_filename)

        resulting_alignment = calculate_oc_alignments(ocel, ocpn)

        # they are not allowed to compensate each other
        self.assertGreater(get_total_cost_of_aligment(resulting_alignment, ocel), 0)

    def test_mine_defined_cost_net(self):
        # Dejure Model as a petri net
        dejure_filename = "sample-logs/jsonocel/p2p-normal.jsonocel"
        dejure_ocel = ocel_import_factory.apply(dejure_filename)
        dejure_ocpn = ocpn_discovery_factory.apply(dejure_ocel, parameters={"debug": False})

        # OCEL used for process executions
        defacto_filename = "sample-logs/jsonocel/p2p-01-variant-cost-03.jsonocel"
        defacto_ocel = ocel_import_factory.apply(defacto_filename)

        resulting_alignment = calculate_oc_alignments(defacto_ocel, dejure_ocpn)

        self.assertEqual(get_total_cost_of_aligment(resulting_alignment, defacto_ocel), 3)

    def test_mine_defined_cost_0_net(self):
        # Dejure Model as a petri net
        dejure_filename = "sample-logs/jsonocel/p2p-normal.jsonocel"
        dejure_ocel = ocel_import_factory.apply(dejure_filename)
        dejure_ocpn = ocpn_discovery_factory.apply(dejure_ocel, parameters={"debug": False})

        # OCEL used for process executions
        defacto_filename = "sample-logs/jsonocel/p2p-01-variant-cost-00.jsonocel"
        defacto_ocel = ocel_import_factory.apply(defacto_filename)

        resulting_alignment = calculate_oc_alignments(defacto_ocel, dejure_ocpn)

        self.assertEqual(get_total_cost_of_aligment(resulting_alignment, defacto_ocel), 0)

    def test_mine_defined_cost_7_net(self):
        # Dejure Model as a petri net
        dejure_filename = "sample-logs/jsonocel/p2p-normal.jsonocel"
        dejure_ocel = ocel_import_factory.apply(dejure_filename)
        dejure_ocpn = ocpn_discovery_factory.apply(dejure_ocel, parameters={"debug": False})

        # OCEL used for process executions
        defacto_filename = "sample-logs/jsonocel/p2p-01-variant-cost-07.jsonocel"
        defacto_ocel = ocel_import_factory.apply(defacto_filename)

        resulting_alignment = calculate_oc_alignments(defacto_ocel, dejure_ocpn)

        self.assertEqual(get_total_cost_of_aligment(resulting_alignment, defacto_ocel), 7)


    # white box tests

    def test_ocpn_deepcopy(self):
        ocpn = copy.deepcopy(self.ocpn)
        self.assertEqual(isinstance(ocpn, ObjectCentricPetriNet), True)

    def test_process_execution_net(self):
        for variant_id in self.ocel.variants:
            ocpn = copy.deepcopy(self.ocpn)
            # ocpn_vis_factory.save(ocpn_vis_factory.apply(ocpn), "post_deepcopy_net.png")

            indirect_id = self.ocel.variants_dict[variant_id][0]  # XXX Check before that it is not empty
            process_execution = self.ocel.process_executions[indirect_id]

            # Each process execution is a list of event ids
            # Create Event Net
            px_net, px_initial_marking_list, px_final_marking_list = process_execution_net_from_process_execution(self.ocel,
                                                                                                                  indirect_id,
                                                                                                                  process_execution,
                                                                                                                  '%Y-%m-%d %H:%M:%S%z')
            self.assertEqual(isinstance(px_net, ObjectCentricPetriNet), True)
            break

    def test_process_execution_net_markings(self):
        for variant_id in self.ocel.variants:
            ocpn = copy.deepcopy(self.ocpn)
            # ocpn_vis_factory.save(ocpn_vis_factory.apply(ocpn), "post_deepcopy_net.png")

            indirect_id = self.ocel.variants_dict[variant_id][0]  # XXX Check before that it is not empty
            process_execution = self.ocel.process_executions[indirect_id]

            # Each process execution is a list of event ids
            # Create Event Net
            px_net, px_initial_marking_list, px_final_marking_list = process_execution_net_from_process_execution(self.ocel,
                                                                                                                  indirect_id,
                                                                                                                  process_execution,
                                                                                                                  '%Y-%m-%d %H:%M:%S%z')
            self.assertEqual(isinstance(px_initial_marking_list, collections.abc.Sequence), True)
            self.assertEqual(isinstance(px_final_marking_list, collections.abc.Sequence), True)
            break

    def test_process_execution_wrong_time_format(self):
        for variant_id in self.ocel.variants:
            ocpn = copy.deepcopy(self.ocpn)
            # ocpn_vis_factory.save(ocpn_vis_factory.apply(ocpn), "post_deepcopy_net.png")

            indirect_id = self.ocel.variants_dict[variant_id][0]  # XXX Check before that it is not empty
            process_execution = self.ocel.process_executions[indirect_id]

            # Each process execution is a list of event ids
            # Create Event Net
            self.assertRaises(Exception, lambda: process_execution_net_from_process_execution(
                self.ocel,
                indirect_id,
                process_execution,
                'abcd'))
            break

    def test_preprocessing_adds_arcs(self):
        for variant_id in self.ocel.variants:
            ocpn = copy.deepcopy(self.ocpn)
            # ocpn_vis_factory.save(ocpn_vis_factory.apply(ocpn), "post_deepcopy_net.png")

            indirect_id = self.ocel.variants_dict[variant_id][0]  # XXX Check before that it is not empty
            process_execution = self.ocel.process_executions[indirect_id]
            # ocpn_vis_factory.save(ocpn_vis_factory.apply(px_net), "px_net.png")
            # Preprocessing of ocpn to remove variable arcs
            dejure_initial_marking_list, dejure_final_marking_list = preprocessing_dejure_net(self.ocel, indirect_id, ocpn)

            number_of_transitions_before = len(self.ocpn.transitions)
            number_of_transitions_after = len(ocpn.transitions)

            self.assertNotEqual(number_of_transitions_after, number_of_transitions_before)
            break

    def test_preprocessing_results_in_OCPN(self):
        for variant_id in self.ocel.variants:
            ocpn = copy.deepcopy(self.ocpn)
            # ocpn_vis_factory.save(ocpn_vis_factory.apply(ocpn), "post_deepcopy_net.png")

            indirect_id = self.ocel.variants_dict[variant_id][0]  # XXX Check before that it is not empty
            process_execution = self.ocel.process_executions[indirect_id]
            # ocpn_vis_factory.save(ocpn_vis_factory.apply(px_net), "px_net.png")
            # Preprocessing of ocpn to remove variable arcs
            dejure_initial_marking_list, dejure_final_marking_list = preprocessing_dejure_net(self.ocel, indirect_id, ocpn)

            self.assertEqual(isinstance(ocpn, ObjectCentricPetriNet), True)
            break

    def test_preprocessing_markings(self):
        for variant_id in self.ocel.variants:
            ocpn = copy.deepcopy(self.ocpn)
            # ocpn_vis_factory.save(ocpn_vis_factory.apply(ocpn), "post_deepcopy_net.png")

            indirect_id = self.ocel.variants_dict[variant_id][0]  # XXX Check before that it is not empty
            process_execution = self.ocel.process_executions[indirect_id]
            # ocpn_vis_factory.save(ocpn_vis_factory.apply(px_net), "px_net.png")
            # Preprocessing of ocpn to remove variable arcs
            dejure_initial_marking_list, dejure_final_marking_list = preprocessing_dejure_net(self.ocel, indirect_id, ocpn)

            self.assertEqual(isinstance(dejure_initial_marking_list, collections.abc.Sequence), True)
            self.assertEqual(isinstance(dejure_final_marking_list, collections.abc.Sequence), True)
            break

    def test_create_synchronous_product_net_markings(self):
        for variant_id in self.ocel.variants:
            ocpn = copy.deepcopy(self.ocpn)
            # ocpn_vis_factory.save(ocpn_vis_factory.apply(ocpn), "post_deepcopy_net.png")

            indirect_id = self.ocel.variants_dict[variant_id][0]  # XXX Check before that it is not empty
            process_execution = self.ocel.process_executions[indirect_id]

            # Each process execution is a list of event ids
            # Create Event Net
            px_net, px_initial_marking_list, px_final_marking_list = process_execution_net_from_process_execution(self.ocel,
                                                                                                                  indirect_id,
                                                                                                                  process_execution,
                                                                                                                  '%Y-%m-%d %H:%M:%S%z')
            # ocpn_vis_factory.save(ocpn_vis_factory.apply(px_net), "px_net.png")
            # Preprocessing of ocpn to remove variable arcs
            dejure_initial_marking_list, dejure_final_marking_list = preprocessing_dejure_net(self.ocel, indirect_id, ocpn)
            # Create Synchronous Product Net
            sync_pn, sync_initial_marking, sync_final_marking = create_synchronous_product_net(px_net,
                                                                                               px_initial_marking_list,
                                                                                               px_final_marking_list,
                                                                                               ocpn,
                                                                                               dejure_initial_marking_list,
                                                                                               dejure_final_marking_list)
            self.assertEqual(isinstance(sync_initial_marking, FrozenMarking), True)
            self.assertEqual(isinstance(sync_final_marking, FrozenMarking), True)
            break



    def test_create_synchronous_product_net(self):
        for variant_id in self.ocel.variants:
            ocpn = copy.deepcopy(self.ocpn)
            # ocpn_vis_factory.save(ocpn_vis_factory.apply(ocpn), "post_deepcopy_net.png")

            indirect_id = self.ocel.variants_dict[variant_id][0]  # XXX Check before that it is not empty
            process_execution = self.ocel.process_executions[indirect_id]

            # Each process execution is a list of event ids
            # Create Event Net
            px_net, px_initial_marking_list, px_final_marking_list = process_execution_net_from_process_execution(self.ocel,
                                                                                                                  indirect_id,
                                                                                                                  process_execution,
                                                                                                                  '%Y-%m-%d %H:%M:%S%z')
            # ocpn_vis_factory.save(ocpn_vis_factory.apply(px_net), "px_net.png")
            # Preprocessing of ocpn to remove variable arcs
            dejure_initial_marking_list, dejure_final_marking_list = preprocessing_dejure_net(self.ocel, indirect_id, ocpn)
            # Create Synchronous Product Net
            sync_pn, sync_initial_marking, sync_final_marking = create_synchronous_product_net(px_net,
                                                                                               px_initial_marking_list,
                                                                                               px_final_marking_list,
                                                                                               ocpn,
                                                                                               dejure_initial_marking_list,
                                                                                               dejure_final_marking_list)
            self.assertEqual(isinstance(sync_pn, ObjectCentricPetriNet), True)
            break

    def test_all_valid_bindings(self):
        for variant_id in self.ocel.variants:
            ocpn = copy.deepcopy(self.ocpn)
            # ocpn_vis_factory.save(ocpn_vis_factory.apply(ocpn), "post_deepcopy_net.png")

            indirect_id = self.ocel.variants_dict[variant_id][0]  # XXX Check before that it is not empty
            process_execution = self.ocel.process_executions[indirect_id]

            # Each process execution is a list of event ids
            # Create Event Net
            px_net, px_initial_marking_list, px_final_marking_list = process_execution_net_from_process_execution(self.ocel,
                                                                                                                  indirect_id,
                                                                                                                  process_execution,
                                                                                                                  '%Y-%m-%d %H:%M:%S%z')
            # ocpn_vis_factory.save(ocpn_vis_factory.apply(px_net), "px_net.png")
            # Preprocessing of ocpn to remove variable arcs
            dejure_initial_marking_list, dejure_final_marking_list = preprocessing_dejure_net(self.ocel, indirect_id, ocpn)
            # Create Synchronous Product Net
            sync_pn, sync_initial_marking, sync_final_marking = create_synchronous_product_net(px_net,
                                                                                               px_initial_marking_list,
                                                                                               px_final_marking_list,
                                                                                               ocpn,
                                                                                               dejure_initial_marking_list,
                                                                                               dejure_final_marking_list)

            break


    def test_dijkstra_search(self):
        for variant_id in self.ocel.variants:
            ocpn = copy.deepcopy(self.ocpn)
            # ocpn_vis_factory.save(ocpn_vis_factory.apply(ocpn), "post_deepcopy_net.png")

            indirect_id = self.ocel.variants_dict[variant_id][0]  # XXX Check before that it is not empty
            process_execution = self.ocel.process_executions[indirect_id]

            # Each process execution is a list of event ids
            # Create Event Net
            px_net, px_initial_marking_list, px_final_marking_list = process_execution_net_from_process_execution(self.ocel,
                                                                                                                  indirect_id,
                                                                                                                  process_execution,
                                                                                                                  '%Y-%m-%d %H:%M:%S%z')
            # ocpn_vis_factory.save(ocpn_vis_factory.apply(px_net), "px_net.png")
            # Preprocessing of ocpn to remove variable arcs
            dejure_initial_marking_list, dejure_final_marking_list = preprocessing_dejure_net(self.ocel, indirect_id, ocpn)
            # Create Synchronous Product Net
            sync_pn, sync_initial_marking, sync_final_marking = create_synchronous_product_net(px_net,
                                                                                               px_initial_marking_list,
                                                                                               px_final_marking_list,
                                                                                               ocpn,
                                                                                               dejure_initial_marking_list,
                                                                                               dejure_final_marking_list)
            # Search for shortest path in Synchronous Product Net
            alignment_for_variant = dijkstra(sync_pn, sync_initial_marking, sync_final_marking)

            self.assertEqual(isinstance(alignment_for_variant, Alignment), True)
            break

    def test_dijkstra_wrong_ini_marking(self):
        for variant_id in self.ocel.variants:
            ocpn = copy.deepcopy(self.ocpn)
            # ocpn_vis_factory.save(ocpn_vis_factory.apply(ocpn), "post_deepcopy_net.png")

            indirect_id = self.ocel.variants_dict[variant_id][0]  # XXX Check before that it is not empty
            process_execution = self.ocel.process_executions[indirect_id]

            # Each process execution is a list of event ids
            # Create Event Net
            px_net, px_initial_marking_list, px_final_marking_list = process_execution_net_from_process_execution(self.ocel,
                                                                                                                  indirect_id,
                                                                                                                  process_execution,
                                                                                                                  '%Y-%m-%d %H:%M:%S%z')
            # ocpn_vis_factory.save(ocpn_vis_factory.apply(px_net), "px_net.png")
            # Preprocessing of ocpn to remove variable arcs
            dejure_initial_marking_list, dejure_final_marking_list = preprocessing_dejure_net(self.ocel, indirect_id, ocpn)
            # Create Synchronous Product Net
            sync_pn, sync_initial_marking, sync_final_marking = create_synchronous_product_net(px_net,
                                                                                               px_initial_marking_list,
                                                                                               px_final_marking_list,
                                                                                               ocpn,
                                                                                               dejure_initial_marking_list,
                                                                                               dejure_final_marking_list)

            self.assertRaises(Exception, lambda: dijkstra(sync_pn, None, sync_final_marking))
            break

    def test_dijkstra_wrong_final_marking(self):
        for variant_id in self.ocel.variants:
            ocpn = copy.deepcopy(self.ocpn)
            # ocpn_vis_factory.save(ocpn_vis_factory.apply(ocpn), "post_deepcopy_net.png")

            indirect_id = self.ocel.variants_dict[variant_id][0]  # XXX Check before that it is not empty
            process_execution = self.ocel.process_executions[indirect_id]

            # Each process execution is a list of event ids
            # Create Event Net
            px_net, px_initial_marking_list, px_final_marking_list = process_execution_net_from_process_execution(
                self.ocel,
                indirect_id,
                process_execution,
                '%Y-%m-%d %H:%M:%S%z')
            # ocpn_vis_factory.save(ocpn_vis_factory.apply(px_net), "px_net.png")
            # Preprocessing of ocpn to remove variable arcs
            dejure_initial_marking_list, dejure_final_marking_list = preprocessing_dejure_net(self.ocel, indirect_id,
                                                                                              ocpn)
            # Create Synchronous Product Net
            sync_pn, sync_initial_marking, sync_final_marking = create_synchronous_product_net(px_net,
                                                                                               px_initial_marking_list,
                                                                                               px_final_marking_list,
                                                                                               ocpn,
                                                                                               dejure_initial_marking_list,
                                                                                               dejure_final_marking_list)

            self.assertRaises(Exception, lambda: dijkstra(sync_pn, sync_initial_marking, None))
            break


    def test_dijkstra_wrong_sync_pn(self):
        for variant_id in self.ocel.variants:
            ocpn = copy.deepcopy(self.ocpn)
            # ocpn_vis_factory.save(ocpn_vis_factory.apply(ocpn), "post_deepcopy_net.png")

            indirect_id = self.ocel.variants_dict[variant_id][0]  # XXX Check before that it is not empty
            process_execution = self.ocel.process_executions[indirect_id]

            # Each process execution is a list of event ids
            # Create Event Net
            px_net, px_initial_marking_list, px_final_marking_list = process_execution_net_from_process_execution(
                self.ocel,
                indirect_id,
                process_execution,
                '%Y-%m-%d %H:%M:%S%z')
            # ocpn_vis_factory.save(ocpn_vis_factory.apply(px_net), "px_net.png")
            # Preprocessing of ocpn to remove variable arcs
            dejure_initial_marking_list, dejure_final_marking_list = preprocessing_dejure_net(self.ocel, indirect_id,
                                                                                              ocpn)
            # Create Synchronous Product Net
            sync_pn, sync_initial_marking, sync_final_marking = create_synchronous_product_net(px_net,
                                                                                               px_initial_marking_list,
                                                                                               px_final_marking_list,
                                                                                               ocpn,
                                                                                               dejure_initial_marking_list,
                                                                                               dejure_final_marking_list)

            self.assertRaises(Exception, lambda: dijkstra(None, sync_initial_marking, sync_final_marking))
            break


    def test_computation_of_valid_bindings(self):
        for variant_id in self.ocel.variants:
            ocpn = copy.deepcopy(self.ocpn)
            # ocpn_vis_factory.save(ocpn_vis_factory.apply(ocpn), "post_deepcopy_net.png")

            indirect_id = self.ocel.variants_dict[variant_id][0]  # XXX Check before that it is not empty
            process_execution = self.ocel.process_executions[indirect_id]

            # Each process execution is a list of event ids
            # Create Event Net
            px_net, px_initial_marking_list, px_final_marking_list = process_execution_net_from_process_execution(
                self.ocel,
                indirect_id,
                process_execution,
                '%Y-%m-%d %H:%M:%S%z')
            # ocpn_vis_factory.save(ocpn_vis_factory.apply(px_net), "px_net.png")
            # Preprocessing of ocpn to remove variable arcs
            dejure_initial_marking_list, dejure_final_marking_list = preprocessing_dejure_net(self.ocel, indirect_id,
                                                                                              ocpn)
            # Create Synchronous Product Net
            sync_pn, sync_initial_marking, sync_final_marking = create_synchronous_product_net(px_net,
                                                                                               px_initial_marking_list,
                                                                                               px_final_marking_list,
                                                                                               ocpn,
                                                                                               dejure_initial_marking_list,
                                                                                               dejure_final_marking_list)

            number_of_valid_bindings = len(all_valid_bindings(sync_pn, sync_initial_marking))
            self.assertGreater(number_of_valid_bindings, 0)
            break

    def test_valid_bindings_wrong_input(self):
        for variant_id in self.ocel.variants:
            ocpn = copy.deepcopy(self.ocpn)
            # ocpn_vis_factory.save(ocpn_vis_factory.apply(ocpn), "post_deepcopy_net.png")

            indirect_id = self.ocel.variants_dict[variant_id][0]  # XXX Check before that it is not empty
            process_execution = self.ocel.process_executions[indirect_id]

            # Each process execution is a list of event ids
            # Create Event Net
            px_net, px_initial_marking_list, px_final_marking_list = process_execution_net_from_process_execution(
                self.ocel,
                indirect_id,
                process_execution,
                '%Y-%m-%d %H:%M:%S%z')
            # ocpn_vis_factory.save(ocpn_vis_factory.apply(px_net), "px_net.png")
            # Preprocessing of ocpn to remove variable arcs
            dejure_initial_marking_list, dejure_final_marking_list = preprocessing_dejure_net(self.ocel, indirect_id,
                                                                                              ocpn)
            # Create Synchronous Product Net
            sync_pn, sync_initial_marking, sync_final_marking = create_synchronous_product_net(px_net,
                                                                                               px_initial_marking_list,
                                                                                               px_final_marking_list,
                                                                                               ocpn,
                                                                                               dejure_initial_marking_list,
                                                                                               dejure_final_marking_list)

            self.assertRaises(Exception, lambda: all_valid_bindings(None, sync_initial_marking))
            break

if __name__ == '__main__':
    unittest.main()