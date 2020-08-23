import unittest
from collections import Counter

from DyadicContext import DyadicContext
from TriadicContext import TriadicContext


class MyTestCase(unittest.TestCase):
    input_file = "inputs/example.data"
    dyadic_file = "miner_output/example.data.context"
    concepts_file = "miner_output/example.data.concepts"
    links_file = "miner_output/example.data.links"

    @classmethod
    def setUpClass(cls):
        triadic_context = TriadicContext.read_triadic_context(cls.input_file)

        context, objects_count, attributes_count = TriadicContext.to_dyadic(triadic_context)
        cls.dyadic_context = DyadicContext(context, objects_count, attributes_count)
        cls.dyadic_context.save_context(cls.dyadic_file)

        # dyadic_context.mine_concepts(configs.dyadic_file, configs.concepts_file)
        cls.dyadic_context.read_concepts_from_file(cls.concepts_file)

        cls.dyadic_context.iPred()
        cls.dyadic_context.save_links(cls.links_file)

        cls.dyadic_context.compute_feature_generators()

    @staticmethod
    def expected_test_link(set_list):
        return Counter([frozenset([str(i) for i in sub_list]) for sub_list in set_list])

    def actual_test_link(self, set_list, relation):
        if relation == 'children':
            return Counter([c.extent for c in
                            self.dyadic_context.concepts_lattice[frozenset([str(i) for i in set_list])].children])
        elif relation == 'parents':
            return Counter([c.extent for c in
                            self.dyadic_context.concepts_lattice[frozenset([str(i) for i in set_list])].parents])

    def test_links(self):
        self.assertEqual(self.expected_test_link([[1, 2, 4], [2, 3, 4, 5], [1, 3, 4, 5]]),
                         self.actual_test_link([1, 2, 3, 4, 5], 'children'))

        self.assertEqual(self.expected_test_link([]),
                         self.actual_test_link([1, 2, 3, 4, 5], 'parents'))

        self.assertEqual(self.expected_test_link([[2, 4], [1, 4]]),
                         self.actual_test_link([1, 2, 4], 'children'))

        self.assertEqual(self.expected_test_link([[1, 2, 3, 4, 5]]),
                         self.actual_test_link([1, 2, 4], 'parents'))

        self.assertEqual(self.expected_test_link([[2, 4], [2, 5], [3, 4, 5]]),
                         self.actual_test_link([2, 3, 4, 5], 'children'))

        self.assertEqual(self.expected_test_link([[1, 2, 3, 4, 5]]),
                         self.actual_test_link([2, 3, 4, 5], 'parents'))

        self.assertEqual(self.expected_test_link([[3, 4, 5], [1, 3, 4], [1, 3, 5]]),
                         self.actual_test_link([1, 3, 4, 5], 'children'))

        self.assertEqual(self.expected_test_link([[1, 2, 3, 4, 5]]),
                         self.actual_test_link([1, 3, 4, 5], 'parents'))

        self.assertEqual(self.expected_test_link([[2], [4]]),
                         self.actual_test_link([2, 4], 'children'))

        self.assertEqual(self.expected_test_link([[1, 2, 4], [2, 3, 4, 5]]),
                         self.actual_test_link([2, 4], 'parents'))

        self.assertEqual(self.expected_test_link([[2], [5]]),
                         self.actual_test_link([2, 5], 'children'))

        self.assertEqual(self.expected_test_link([[2, 3, 4, 5]]),
                         self.actual_test_link([2, 5], 'parents'))

        self.assertEqual(self.expected_test_link([[3, 4], [3, 5]]),
                         self.actual_test_link([3, 4, 5], 'children'))

        self.assertEqual(self.expected_test_link([[2, 3, 4, 5], [1, 3, 4, 5]]),
                         self.actual_test_link([3, 4, 5], 'parents'))

        self.assertEqual(self.expected_test_link([[3, 4], [1, 4], [1, 3]]),
                         self.actual_test_link([1, 3, 4], 'children'))

        self.assertEqual(self.expected_test_link([[1, 3, 4, 5]]),
                         self.actual_test_link([1, 3, 4], 'parents'))

        self.assertEqual(self.expected_test_link([[3, 5], [1, 3], [1, 5]]),
                         self.actual_test_link([1, 3, 5], 'children'))

        self.assertEqual(self.expected_test_link([[1, 3, 4, 5]]),
                         self.actual_test_link([1, 3, 5], 'parents'))

        self.assertEqual(self.expected_test_link([[4], [3]]),
                         self.actual_test_link([3, 4], 'children'))

        self.assertEqual(self.expected_test_link([[3, 4, 5], [1, 3, 4]]),
                         self.actual_test_link([3, 4], 'parents'))

        self.assertEqual(self.expected_test_link([[1], [4]]),
                         self.actual_test_link([1, 4], 'children'))

        self.assertEqual(self.expected_test_link([[1, 2, 4], [1, 3, 4]]),
                         self.actual_test_link([1, 4], 'parents'))

        self.assertEqual(self.expected_test_link([[3], [5]]),
                         self.actual_test_link([3, 5], 'children'))

        self.assertEqual(self.expected_test_link([[3, 4, 5], [1, 3, 5]]),
                         self.actual_test_link([3, 5], 'parents'))

        self.assertEqual(self.expected_test_link([[1], [3]]),
                         self.actual_test_link([1, 3], 'children'))

        self.assertEqual(self.expected_test_link([[1, 3, 4], [1, 3, 5]]),
                         self.actual_test_link([1, 3], 'parents'))

        self.assertEqual(self.expected_test_link([[1], [5]]),
                         self.actual_test_link([1, 5], 'children'))

        self.assertEqual(self.expected_test_link([[1, 3, 5]]),
                         self.actual_test_link([1, 5], 'parents'))

        self.assertEqual(self.expected_test_link([[2, 4], [2, 5]]),
                         self.actual_test_link([2], 'parents'))

        self.assertEqual(self.expected_test_link([[1, 4], [2, 4], [3, 4]]),
                         self.actual_test_link([4], 'parents'))

        self.assertEqual(self.expected_test_link([[1, 3], [1, 4], [1, 5]]),
                         self.actual_test_link([1], 'parents'))

        self.assertEqual(self.expected_test_link([[1, 3], [3, 4], [3, 5]]),
                         self.actual_test_link([3], 'parents'))

        self.assertEqual(self.expected_test_link([[2, 5], [3, 5], [1, 5]]),
                         self.actual_test_link([5], 'parents'))

        self.assertEqual(Counter([frozenset({'ø'})]),
                         self.actual_test_link([1], 'children'))

        self.assertEqual(Counter([frozenset({'ø'})]),
                         self.actual_test_link([2], 'children'))

        self.assertEqual(Counter([frozenset({'ø'})]),
                         self.actual_test_link([3], 'children'))

        self.assertEqual(Counter([frozenset({'ø'})]),
                         self.actual_test_link([4], 'children'))

        self.assertEqual(Counter([frozenset({'ø'})]),
                         self.actual_test_link([5], 'children'))

        self.assertEqual(
            Counter([frozenset({'1'}), frozenset({'2'}), frozenset({'3'}), frozenset({'4'}), frozenset({'5'})]),
            Counter([c.extent for c in
                     self.dyadic_context.concepts_lattice[frozenset({'ø'})].parents]))

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
