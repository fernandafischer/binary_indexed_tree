class FenwickTree:
    """
    A Binary Indexed Tree (Fenwick Tree) for maintaining prefix sums
    of an array with point updates and prefix queries in O(log n).

    Implementation choice: 1-indexed internal tree array, which is the
    canonical Fenwick layout. The public API uses 0-indexed positions
    because Python sequences are 0-indexed and the caller should not need
    to think about the internal offset. Every public method translates
    once at the boundary.

    Handles negative values: no division is used anywhere (only bitwise
    operations and addition/subtraction), so negative integers behave
    correctly. Floats also work but are subject to normal floating-point
    accumulation error; the caller should not use == on prefix sums.
    """

    __slots__ = ("_size", "_tree")

    def __init__(self, size):
        """
        Initialize an empty tree for an array of `size` non-negative
        indexable positions (0 .. size-1).

        We pre-allocate rather than appending because Fenwick trees rely
        on a fixed index-to-node mapping determined by the maximum size.
        """
        if not isinstance(size, int) or isinstance(size, bool):
            raise TypeError("size must be an int")
        if size <= 0:
            raise ValueError("size must be positive")
        self._size = size
        # Internal tree is 1-indexed; index 0 is a dummy that is never read.
        self._tree = [0] * (size + 1)

    @classmethod
    def from_values(cls, values):
        """
        Build a FenwickTree pre-populated with `values`.

        Constructed in O(n) rather than n separate O(log n) updates: we
        first copy values into the 1-indexed tree, then propagate each
        node's sum to its parent (i & (i + lowbit) in 1-indexed terms).
        This is faster for large inputs and avoids an O(n log n) cold start.
        """
        n = len(values)
        if n == 0:
            raise ValueError("values must be non-empty")
        obj = cls(n)
        tree = obj._tree
        for i, v in enumerate(values, start=1):
            tree[i] = v
        for i in range(1, n + 1):
            j = i + (i & -i)
            if j <= n:
                tree[j] += tree[i]
        return obj

    def update(self, index, delta):
        """
        Add `delta` to position `index` (0-indexed).

        Uses `i & -i` to find the lowest set bit, which is the standard
        Fenwick traversal. Works for negative `delta`.
        """
        if not isinstance(index, int) or isinstance(index, bool):
            raise TypeError("index must be an int")
        if index < 0 or index >= self._size:
            raise IndexError(f"index {index} out of range [0, {self._size})")
        i = index + 1
        n = self._size
        tree = self._tree
        while i <= n:
            tree[i] += delta
            i += i & -i

    def prefix_sum(self, index):
        """
        Return the sum of positions [0 .. index] inclusive.

        `index` may be -1, which returns 0 (the empty prefix). This avoids
        forcing callers to special-case empty ranges when slicing.
        """
        if not isinstance(index, int) or isinstance(index, bool):
            raise TypeError("index must be an int")
        if index < -1 or index >= self._size:
            raise IndexError(f"index {index} out of range [-1, {self._size})")
        if index == -1:
            return 0
        i = index + 1
        tree = self._tree
        total = 0
        while i > 0:
            total += tree[i]
            i -= i & -i
        return total

    def range_sum(self, left, right):
        """
        Return the sum of positions [left .. right] inclusive.

        If left > right the result is 0 (empty range). This matches the
        natural convention that summing zero elements yields zero rather
        than raising.
        """
        if not isinstance(left, int) or isinstance(left, bool):
            raise TypeError("left must be an int")
        if not isinstance(right, int) or isinstance(right, bool):
            raise TypeError("right must be an int")
        if left < 0 or right >= self._size:
            raise IndexError("range endpoints out of bounds")
        if left > right:
            return 0
        return self.prefix_sum(right) - self.prefix_sum(left - 1)

    def __len__(self):
        return self._size


# Short alias for callers who prefer the acronym.
BIT = FenwickTree
