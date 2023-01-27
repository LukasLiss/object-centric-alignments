import unittest

from algorithm import calculate_oc_alignments

from localocpa.objects.log.importer.ocel import factory as ocel_import_factory
from localocpa.algo.discovery.ocpn import algorithm as ocpn_discovery_factory

from test_ocpns import TestOCPNS


def get_total_cost_of_aligment(alignments, defacto_ocel):
    alignment_cost_total = 0
    for variant_id, alignment in alignments.items():
        alignment_cost_total += len(defacto_ocel.variants_dict[variant_id]) * alignment.get_cost()
    return alignment_cost_total


class TestObjectCentricAligments(unittest.TestCase):

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

        # all are perfrctly fitting
        self.assertEqual(get_total_cost_of_aligment(resulting_alignment, defacto_ocel), 0)
        # each variant was aligned
        self.assertEqual(len(resulting_alignment.values()), len(defacto_ocel.variants_dict.keys()))


if __name__ == '__main__':
    unittest.main()