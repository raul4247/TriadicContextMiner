import unittest
from collections import Counter

import configs
from DyadicContext import DyadicContext
from TriadicContext import TriadicContext


class MyTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        triadic_context = TriadicContext.read_triadic_context(configs.input_file)

        context, objects_count, attributes_count = TriadicContext.to_dyadic(triadic_context)
        cls.dyadic_context = DyadicContext(context, objects_count, attributes_count)
        cls.dyadic_context.save(configs.dyadic_file)

        # dyadic_context.mine_concepts(configs.dyadic_file, configs.concepts_file)
        cls.dyadic_context.read_concepts_from_file(configs.concepts_file)

        cls.dyadic_context.iPred()
        cls.dyadic_context.save_links(configs.links_file)

        cls.dyadic_context.compute_feature_generators()

    def test_generators(self):
        self.assertEqual(Counter(
            [frozenset({'Ra'}), frozenset({'Nd'}), frozenset({'Pd'}), frozenset({'Ka'}), frozenset({'Pa'})]),
            Counter(self.dyadic_context.generators[self.dyadic_context.concepts[frozenset({'4', '3', '5', '2', '1'})]]))

        self.assertEqual(Counter([frozenset({'Rb'})]), Counter(
            self.dyadic_context.generators[self.dyadic_context.concepts[frozenset({'4', '2', '3', '5'})]]))

        self.assertEqual(Counter([frozenset({'Kb'})]), Counter(
            self.dyadic_context.generators[self.dyadic_context.concepts[frozenset({'4', '1', '3', '5'})]]))

        self.assertEqual(Counter([frozenset({'Rb', 'Kb'})]), Counter(
            self.dyadic_context.generators[self.dyadic_context.concepts[frozenset({'4', '3', '5'})]]))

        self.assertEqual(Counter([frozenset({'Pb'})]), Counter(
            self.dyadic_context.generators[self.dyadic_context.concepts[frozenset({'4', '1', '3'})]]))

        self.assertEqual(Counter([frozenset({'Pb', 'Rb'})]),
                         Counter(self.dyadic_context.generators[self.dyadic_context.concepts[frozenset({'4', '3'})]]))

        self.assertEqual(Counter([frozenset({'Sa'})]), Counter(
            self.dyadic_context.generators[self.dyadic_context.concepts[frozenset({'1', '3', '5'})]]))

        self.assertEqual(Counter([frozenset({'Rb', 'Sa'})]),
                         Counter(self.dyadic_context.generators[self.dyadic_context.concepts[frozenset({'3', '5'})]]))

        self.assertEqual(Counter([frozenset({'Pb', 'Sa'})]),
                         Counter(self.dyadic_context.generators[self.dyadic_context.concepts[frozenset({'1', '3'})]]))

        self.assertEqual(Counter([frozenset({'Pb', 'Rb', 'Sa'})]),
                         Counter(self.dyadic_context.generators[self.dyadic_context.concepts[frozenset({'3'})]]))

        self.assertEqual(Counter([frozenset({'Nb'})]), Counter(
            self.dyadic_context.generators[self.dyadic_context.concepts[frozenset({'4', '2', '1'})]]))

        self.assertEqual(Counter([frozenset({'Sd'}), frozenset({'Nb', 'Rb'})]),
                         Counter(self.dyadic_context.generators[self.dyadic_context.concepts[frozenset({'4', '2'})]]))

        self.assertEqual(Counter([frozenset({'Kb', 'Nb'}), frozenset({'Nb', 'Pb'})]),
                         Counter(self.dyadic_context.generators[self.dyadic_context.concepts[frozenset({'1', '4'})]]))

        self.assertEqual(Counter([frozenset({'Pb', 'Sd'}), frozenset({'Sd', 'Kb'}), frozenset({'Pb', 'Nb', 'Rb'}),
                                  frozenset({'Kb', 'Nb', 'Rb'})]),
                         Counter(self.dyadic_context.generators[self.dyadic_context.concepts[frozenset({'4'})]]))

        self.assertEqual(Counter([frozenset({'Rd'})]),
                         Counter(self.dyadic_context.generators[self.dyadic_context.concepts[frozenset({'2', '5'})]]))

        self.assertEqual(Counter([frozenset({'Na'})]), Counter(
            self.dyadic_context.generators[self.dyadic_context.concepts[frozenset({'1', '5'})]]))

        self.assertEqual(Counter(
            [frozenset({'Kc'}), frozenset({'Rb', 'Na'}), frozenset({'Sa', 'Rd'}), frozenset({'Na', 'Rd'}),
             frozenset({'Kb', 'Rd'})]),
                         Counter(self.dyadic_context.generators[self.dyadic_context.concepts[frozenset({'5'})]]))

        self.assertEqual(
            Counter([frozenset({'Kd'}), frozenset({'Nc'}), frozenset({'Sd', 'Rd'}), frozenset({'Rd', 'Nb'})]),
            Counter(self.dyadic_context.generators[self.dyadic_context.concepts[frozenset({'2'})]]))

        self.assertEqual(
            Counter([frozenset({'Rc'}), frozenset({'Pb', 'Na'}), frozenset({'Nb', 'Sa'}), frozenset({'Nb', 'Na'})]),
            Counter(self.dyadic_context.generators[self.dyadic_context.concepts[frozenset({'1'})]]), )

    if __name__ == '__main__':
        unittest.main()
