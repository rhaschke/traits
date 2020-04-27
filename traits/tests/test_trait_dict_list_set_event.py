# (C) Copyright 2005-2020 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

""" Test cases for TraitListEvent, TraitDictEvent, TraitSetEvent. """

import unittest

from traits.api import (
    Dict, HasTraits, List, on_trait_change, Set,
    TraitListEvent, TraitDictEvent, TraitSetEvent
)


class Foo(HasTraits):

    alist = List([1, 2, 3])
    adict = Dict({'red': 255, 'blue': 0, 'green': 127})
    aset = Set({1, 2, 3})

    @on_trait_change(["alist_items", "adict_items", "aset_items"])
    def _receive_events(self, event):
        self.event = event


class TestTraitEvent(unittest.TestCase):

    foo = Foo()

    def test_list_repr(self):
        self.foo.alist[::2] = [4, 5]
        event = self.foo.event
        event_str = ("TraitListEvent(index=slice(0, 3, 2), "
                     "removed=[1, 3], added=[4, 5])")
        self.assertEqual(event.__repr__(), event_str)
        self.assertIsInstance(eval(event.__repr__()), TraitListEvent)

    def test_dict_event_repr(self):
        self.foo.adict.update({'blue': 10, 'black': 0})
        event = self.foo.event
        event_str = ("TraitDictEvent(removed={}, added={'black': 0}, "
                     "changed={'blue': 0})")
        self.assertEqual(event.__repr__(), event_str)
        self.assertIsInstance(eval(event.__repr__()), TraitDictEvent)

    def test_set_event_repr(self):
        self.foo.aset.symmetric_difference_update({3, 4})
        event = self.foo.event
        event_str = "TraitSetEvent(removed={3}, added={4})"
        self.assertEqual(event.__repr__(), event_str)
        self.assertIsInstance(eval(event.__repr__()), TraitSetEvent)