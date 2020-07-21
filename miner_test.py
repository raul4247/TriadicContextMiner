import unittest
from collections import Counter

import configs
from DyadicContext import DyadicContext
from TriadicContext import TriadicContext


class MyTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        triadic_context = TriadicContext.read_triadic_context(configs.input_file)

        context, objects_count, attributes_count = TriadicContext.to_dyadic(triadic_context)
        self.dyadic_context = DyadicContext(context, objects_count, attributes_count)
        self.dyadic_context.save(configs.dyadic_file)

        # dyadic_context.mine_concepts(configs.dyadic_file, configs.concepts_file)
        self.dyadic_context.read_concepts_from_file(configs.concepts_file)

        self.dyadic_context.iPred()
        self.dyadic_context.save_links(configs.links_file)

        self.dyadic_context.compute_feature_generators()

    def test_generators(self):
        self.assertEqual(Counter(
            self.dyadic_context.generators[self.dyadic_context.concepts[frozenset({'4', '3', '5', '2', '1'})]]),
            Counter(
                [frozenset({'Ra'}), frozenset({'Nd'}), frozenset({'Pd'}), frozenset({'Ka'}), frozenset({'Pa'})]))
        self.assertEqual(
            Counter(self.dyadic_context.generators[self.dyadic_context.concepts[frozenset({'4', '2', '3', '5'})]]),
            Counter(
                [frozenset({'Rb'})]))
        self.assertEqual(
            Counter(self.dyadic_context.generators[self.dyadic_context.concepts[frozenset({'4', '1', '3', '5'})]]),
            Counter(
                [frozenset({'Kb'})]))

        self.assertEqual(
            Counter(self.dyadic_context.generators[self.dyadic_context.concepts[frozenset({'4', '3', '5'})]]), Counter(
                [frozenset({'Rb', 'Kb'})]))
        self.assertEqual(
            Counter(self.dyadic_context.generators[self.dyadic_context.concepts[frozenset({'4', '1', '3'})]]), Counter(
                [frozenset({'Pb'})]))
        self.assertEqual(
            Counter(self.dyadic_context.generators[self.dyadic_context.concepts[frozenset({'4', '3'})]]), Counter(
                [frozenset({'Pb', 'Rb'})]))
        self.assertEqual(
            Counter(self.dyadic_context.generators[self.dyadic_context.concepts[frozenset({'1', '3', '5'})]]), Counter(
                [frozenset({'Sa'})]))
        self.assertEqual(
            Counter(self.dyadic_context.generators[self.dyadic_context.concepts[frozenset({'3', '5'})]]), Counter(
                [frozenset({'Rb', 'Sa'})]))
        self.assertEqual(
            Counter(self.dyadic_context.generators[self.dyadic_context.concepts[frozenset({'1', '3'})]]), Counter(
                [frozenset({'Pb', 'Sa'})]))
        self.assertEqual(Counter(self.dyadic_context.generators[self.dyadic_context.concepts[frozenset({'3'})]]),
                         Counter(
                             [frozenset({'Pb', 'Rb', 'Sa'})]))
        self.assertEqual(
            Counter(self.dyadic_context.generators[self.dyadic_context.concepts[frozenset({'4', '2', '1'})]]), Counter(
                [frozenset({'Nb'})]))
        self.assertEqual(
            Counter(self.dyadic_context.generators[self.dyadic_context.concepts[frozenset({'4', '2'})]]), Counter(
                [frozenset({'Sd'}), frozenset({'Nb', 'Rb'})]))

        self.assertEqual(
            Counter(self.dyadic_context.generators[self.dyadic_context.concepts[frozenset({'1', '4'})]]), Counter(
                [frozenset({'Kb', 'Nb'}), frozenset({'Nb', 'Pb'})]))

        self.assertEqual(Counter(self.dyadic_context.generators[self.dyadic_context.concepts[frozenset({'4'})]]),
                         Counter(
                             [frozenset({'Pb', 'Sd'}), frozenset({'Sd', 'Kb'}), frozenset({'Pb', 'Nb', 'Rb'}),
                              frozenset({'Kb', 'Nb', 'Rb'})]))
        self.assertEqual(
            Counter(self.dyadic_context.generators[self.dyadic_context.concepts[frozenset({'2', '5'})]]), Counter(
                [frozenset({'Rd'})]))
        self.assertEqual(
            Counter(self.dyadic_context.generators[self.dyadic_context.concepts[frozenset({'1', '5'})]]), Counter(
                [frozenset({'Na'})]))
        self.assertEqual(Counter(self.dyadic_context.generators[self.dyadic_context.concepts[frozenset({'5'})]]),
                         Counter(
                             [frozenset({'Kc'}), frozenset({'Rb', 'Na'}), frozenset({'Sa', 'Rd'}),
                              frozenset({'Na', 'Rd'}),
                              frozenset({'Kb', 'Rd'})]))
        self.assertEqual(Counter(self.dyadic_context.generators[self.dyadic_context.concepts[frozenset({'2'})]]),
                         Counter(
                             [frozenset({'Kd'}), frozenset({'Nc'}), frozenset({'Sd', 'Rd'}), frozenset({'Rd', 'Nb'})]))
        self.assertEqual(Counter(self.dyadic_context.generators[self.dyadic_context.concepts[frozenset({'1'})]]),
                         Counter(
                             [frozenset({'Rc'}), frozenset({'Pb', 'Na'}), frozenset({'Nb', 'Sa'}),
                              frozenset({'Nb', 'Na'})]))


if __name__ == '__main__':
    unittest.main()
