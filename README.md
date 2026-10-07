# binary_indexed_tree

A Binary Indexed Tree (Fenwick tree) for O(log n) point updates and prefix-sum queries on a fixed-size array.

## Usage

```python
from binary_indexed_tree import FenwickTree

t = FenwickTree.from_values([1, 2, 3, 4, 5])
print(t.prefix_sum(2))   # 6  -> 1 + 2 + 3
t.update(2, 10)          # add 10 at index 2
print(t.range_sum(1, 3)) # 19 -> 2 + 13 + 4
```

Exports:

- `FenwickTree` — the class.
- `BIT` — an alias for `FenwickTree`.
- `FenwickTree.from_values(values)` — build from an initial list.
- `FenwickTree(size)` — build empty for `size` positions.
- `.update(index, delta)` — add `delta` to position `index` (0-indexed).
- `.prefix_sum(index)` — sum of `[0, index]` inclusive; `-1` returns 0.
- `.range_sum(left, right)` — sum of `[left, right]` inclusive; empty if `left > right`.

## Why

The problem is simple: you have an array that changes one element at a time, and you repeatedly need sums over prefixes. A naive array gives O(1) updates and O(n) sums; a prefix-sum array gives O(n) updates and O(1) sums. A Fenwick tree sits between them at O(log n) for both, with constant extra space and very small constants. The trade-off is that the array size is fixed at construction — the index-to-node mapping depends on the size — so growing the structure means rebuilding.

The internal layout is the canonical 1-indexed Fenwick array; the public API translates to 0-indexed positions at the boundary so callers never deal with the offset.

## Edge cases

`prefix_sum(-1)` returns 0 so you can compute `range_sum(left, right)` as `prefix_sum(right) - prefix_sum(left - 1)` without special-casing `left == 0`. `range_sum` with `left > right` returns 0 rather than raising. Integer indices are type-checked; `bool` is rejected even though it is a subclass of `int`, because passing `True` as an index is almost always a bug.

## Design notes

The window stores values eagerly rather than keeping running aggregates. Running
sums drift with floating point over long streams, and recomputing from a small
buffer is cheap enough that the drift is not worth the speed.

