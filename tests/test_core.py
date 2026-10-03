import unittest
from binary_indexed_tree import FenwickTree, BIT


class TestConstruction(unittest.TestCase):

    def test_size_must_be_positive(self):
        with self.assertRaises(ValueError):
            FenwickTree(0)
        with self.assertRaises(ValueError):
            FenwickTree(-3)

    def test_size_must_be_int(self):
        with self.assertRaises(TypeError):
            FenwickTree(3.0)
        with self.assertRaises(TypeError):
            FenwickTree(True)

    def test_from_values_empty_raises(self):
        with self.assertRaises(ValueError):
            FenwickTree.from_values([])

    def test_from_values_single(self):
        t = FenwickTree.from_values([42])
        self.assertEqual(t.prefix_sum(0), 42)

    def test_from_values_matches_naive(self):
        values = [3, 1, 4, 1, 5, 9, 2, 6]
        t = FenwickTree.from_values(values)
        expected = 0
        for i, v in enumerate(values):
            expected += v
            self.assertEqual(t.prefix_sum(i), expected)

    def test_alias_is_same_class(self):
        self.assertIs(BIT, FenwickTree)


class TestUpdateAndQuery(unittest.TestCase):

    def setUp(self):
        self.t = FenwickTree.from_values([1, 2, 3, 4, 5])

    def test_prefix_sum_full(self):
        self.assertEqual(self.t.prefix_sum(4), 15)

    def test_prefix_sum_partial(self):
        self.assertEqual(self.t.prefix_sum(2), 6)

    def test_prefix_sum_empty(self):
        self.assertEqual(self.t.prefix_sum(-1), 0)

    def test_update_increases(self):
        self.t.update(2, 10)
        self.assertEqual(self.t.prefix_sum(2), 16)
        self.assertEqual(self.t.prefix_sum(4), 25)

    def test_update_decreases(self):
        self.t.update(0, -1)
        self.assertEqual(self.t.prefix_sum(0), 0)
        self.assertEqual(self.t.prefix_sum(4), 14)

    def test_range_sum_inclusive(self):
        self.assertEqual(self.t.range_sum(1, 3), 9)

    def test_range_sum_single(self):
        self.assertEqual(self.t.range_sum(2, 2), 3)

    def test_range_sum_empty(self):
        self.assertEqual(self.t.range_sum(3, 1), 0)

    def test_index_out_of_range(self):
        with self.assertRaises(IndexError):
            self.t.prefix_sum(5)
        with self.assertRaises(IndexError):
            self.t.update(-1, 1)
        with self.assertRaises(IndexError):
            self.t.update(5, 1)

    def test_index_type_checked(self):
        with self.assertRaises(TypeError):
            self.t.update(2.0, 1)
        with self.assertRaises(TypeError):
            self.t.prefix_sum("2")


class TestEdgeCases(unittest.TestCase):

    def test_negative_values(self):
        t = FenwickTree.from_values([-5, 3, -2, 7])
        self.assertEqual(t.prefix_sum(0), -5)
        self.assertEqual(t.prefix_sum(2), -4)
        self.assertEqual(t.range_sum(1, 3), 8)

    def test_single_element_tree(self):
        t = FenwickTree(1)
        t.update(0, 99)
        self.assertEqual(t.prefix_sum(0), 99)
        self.assertEqual(t.range_sum(0, 0), 99)

    def test_power_of_two_size(self):
        # Sizes that are powers of two exercise the boundary where the
        # highest node aggregates everything; a common off-by-one spot.
        n = 8
        t = FenwickTree(n)
        for i in range(n):
            t.update(i, 1)
        self.assertEqual(t.prefix_sum(n - 1), n)
        self.assertEqual(t.range_sum(0, n - 1), n)

    def test_large_index_propagation(self):
        # Updates at the last position must still propagate to every
        # covering node; verify the total changes correctly.
        t = FenwickTree.from_values([0, 0, 0, 0, 0, 0, 0, 0])
        t.update(7, 100)
        self.assertEqual(t.prefix_sum(7), 100)
        self.assertEqual(t.prefix_sum(6), 0)

    def test_len(self):
        t = FenwickTree(5)
        self.assertEqual(len(t), 5)


if __name__ == "__main__":
    unittest.main()
