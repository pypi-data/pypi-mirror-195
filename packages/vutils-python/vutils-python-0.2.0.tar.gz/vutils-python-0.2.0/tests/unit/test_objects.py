#
# File:    ./tests/unit/test_objects.py
# Author:  Jiří Kučera <sanczes AT gmail.com>
# Date:    2022-06-28 12:39:49 +0200
# Project: vutils-python: Python language tools
#
# SPDX-License-Identifier: MIT
#
"""Test `vutils.python.objects` module."""

from vutils.testing.testcase import TestCase
from vutils.testing.utils import make_type

from vutils.python.objects import (
    ensure_key,
    ensure_no_key,
    flatten,
    merge_data,
)


class MergeDataTestCase(TestCase):
    """Test case for `merge_data`."""

    __slots__ = ()

    def test_merge_lists(self):
        """Test merging two lists."""
        src = [1, 2, "a"]
        dest = [1, "b"]

        merge_data(dest, src)
        self.assertEqual(dest, [1, "b", 1, 2, "a"])

    def test_merge_sets(self):
        """Test merging two sets."""
        src = {1, 2, 3}
        dest = {2, "a"}

        merge_data(dest, src)
        self.assertEqual(dest, {1, 2, 3, "a"})

    def test_merge_dicts(self):
        """Test merging two dicts."""
        src = {"a": 1, "b": 2}
        dest = {"c": 3, "a": "b", 4: "d"}

        merge_data(dest, src)
        self.assertEqual(dest, {"a": 1, "b": 2, "c": 3, 4: "d"})

    def test_merge_objects(self):
        """Test merging two objects."""
        dummy_type = make_type("Dummy", members={"a": 1, "b": 2})
        src = dummy_type()
        src.a = 3
        dest = dummy_type()

        merge_data(dest, src)
        self.assertEqual(dest.a, 3)
        self.assertEqual(dest.b, 2)

    def test_merge_different_objects(self):
        """Test merging two objects of different types."""
        a_type = make_type("A")
        b_type = make_type("B")

        with self.assertRaises(TypeError):
            merge_data([], {1, 2})

        with self.assertRaises(TypeError):
            merge_data(b_type(), a_type())


class EnsureKeyTestCase(TestCase):
    """Test case for `ensure_key`."""

    __slots__ = ()

    def test_key_desired_type(self):
        """Test that a key exists and the value has desired type."""
        mapping = {"a": 1}

        ensure_key(mapping, "a", 0)
        self.assertIn("a", mapping)
        self.assertIsInstance(mapping["a"], int)
        self.assertEqual(mapping["a"], 1)

    def test_key_convertible_type(self):
        """Test that a key exists and the value has convertible type."""
        mapping = {"a": 1}

        ensure_key(mapping, "a", False)
        self.assertIn("a", mapping)
        self.assertIsInstance(mapping["a"], bool)
        self.assertTrue(mapping["a"])

    def test_key_incomatible_type(self):
        """Test that a key exists and the value has incompatible type."""
        mapping = {"a": [1]}

        with self.assertRaises(TypeError):
            ensure_key(mapping, "a", 1)

    def test_key_missing(self):
        """Test that a key is defined when missing."""
        mapping = {"a": 1}

        ensure_key(mapping, "b", 2)
        self.assertEqual(mapping["b"], 2)


class EnsureNoKeyTestCase(TestCase):
    """Test case for `ensure_no_key`."""

    __slots__ = ()

    def test_ensure_no_key(self):
        """Test the key is removed."""
        mapping = {"a": 1}

        for key in ("a", "b"):
            ensure_no_key(mapping, key)
            self.assertNotIn(key, mapping)


class FlattenTestCase(TestCase):
    """Test case for `flatten`."""

    __slots__ = ()

    def test_flatten_simple_objects(self):
        """Test simple objects flattening."""
        self.assertEqual(list(flatten(1)), [1])
        self.assertEqual(list(flatten("abc")), ["abc"])

    def test_flatten_nested_structures(self):
        """Test flattening nested structures."""
        data = [
            1,
            2,
            [3, 4, (5, (6,), 7), 8],
            [9, (10, (11,)), (12,), ()],
            [],
            [([]), ([([], [])]), [(), (((((), 13), []), []), [[14]])]],
            15,
            {16, 17},
            {18: [19]},
        ]
        result = [
            1,
            2,
            3,
            4,
            5,
            6,
            7,
            8,
            9,
            10,
            11,
            12,
            13,
            14,
            15,
            {16, 17},
            {18: [19]},
        ]
        self.assertEqual(list(flatten(data)), result)
