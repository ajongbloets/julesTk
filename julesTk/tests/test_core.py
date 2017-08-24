
from __future__ import print_function
from julesTk import *
import unittest

value = 0


class JTkObjectExample(JTkObject):

    def __init__(self):
        super(JTkObjectExample, self).__init__()
        self._count = 0

    @property
    def count(self):
        return self._count

    @receives("update")
    def update_slot(self, event, source, data=None):
        if data is None:
            data = 0
        self._count -= data

    @triggers()
    def update(self):
        self._count += 1
        return self._count

    @receives("update_before")
    def update_before_slot(self, event, source, data=None):
        if data is None:
            data = 1
        self._count += data

    @triggers("update_before", before=True)
    def trigger_update_before(self):
        self._count = 4
        return self._count


class JTkObjectSubclassExample(JTkObjectExample):

    @receives("update")
    def update_slot(self, event, source, data=None):
        if data is None:
            data = 0
        self._count += data

    @receives("extra")
    def extra_slot(self, event, source, data=None):
        pass

class TestJTObject(unittest.TestCase):

    def test_event_slot_registration(self):
        subject = JTkObject()
        self.assertFalse("update" in subject.event_slots)
        subject = JTkObjectExample()
        self.assertIn("update", subject.event_slots)
        subject = JTkObjectSubclassExample()
        self.assertIn("update", subject.event_slots)

    def test_event_hook_registration(self):
        subject = JTkObjectExample()
        self.assertIn("update", subject.event_hooks)

    def test_hook_independence(self):
        self.assertListEqual(
            list(JTkObject.class_event_hooks), []
        )
        self.assertListEqual(
            sorted(list(JTkObjectExample.class_event_hooks)),
            sorted(["update", "update_before"])
        )
        self.assertListEqual(
            sorted(list(JTkObjectSubclassExample.class_event_hooks)),
            sorted(["update", "update_before"])
        )

    def test_slot_independence(self):
        self.assertListEqual(
            JTkObject.class_event_slots.keys(), []
        )
        self.assertListEqual(
            sorted(JTkObjectExample.class_event_slots.keys()),
            sorted(["update", "update_before"])
        )
        update_slot = JTkObjectExample.class_event_slots["update"]
        self.assertEqual(len(update_slot), 1)
        self.assertListEqual(
            sorted(JTkObjectSubclassExample.class_event_slots.keys()),
            sorted(["update", "update_before", "extra"])
        )
        update_slot = JTkObjectSubclassExample.class_event_slots["update"]
        self.assertEqual(len(update_slot), 1)

    def test_events(self):
        subject_a = JTkObjectExample()
        self.assertEqual(subject_a.count, 0)
        subject_a.receive_event("update", self, 1)
        self.assertEqual(subject_a.count, -1)
        subject_b = JTkObjectSubclassExample()
        subject_b.receive_event("update", self, 1)
        self.assertEqual(subject_b.count, 1)

    def test_trigger(self):
        subject_a = JTkObjectExample()
        subject_b = JTkObjectExample()
        subject_a.add_observer(subject_b)
        self.assertEqual(subject_a.count, 0)
        subject_a.update()
        self.assertEqual(subject_a.count, 1)
        self.assertEqual(subject_b.count, -1)

    def test_subclass(self):
        subject_a = JTkObjectExample()
        subject_b = JTkObjectSubclassExample()
        subject_a.add_observer(subject_b)
        self.assertEqual(subject_a.count, 0)
        subject_a.update()
        self.assertEqual(subject_a.count, 1)
        self.assertEqual(subject_b.count, 1)

    def test_nonclass_receive(self):
        global value
        value = 0

        def simple_handler(event, source, data=None):
            global value
            if data is None:
                data = 0
            value += data

        subject_a = JTkObjectExample()
        subject_a.add_event_slot("update", simple_handler)
        subject_a.add_observer(subject_a)
        subject_a.trigger_event("update", data=1)
        self.assertEqual(value, 1)
