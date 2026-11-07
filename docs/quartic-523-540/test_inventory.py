"""Rejection checks for the added source/dependency inventory."""
import copy
import unittest
from unittest.mock import patch
import inventory

class InventoryRejectionTests(unittest.TestCase):
    def altered(self, edit):
        original=inventory.read
        def replacement(path):
            value=original(path)
            if path=='docs/quartic-523-540/new-applications.json':
                value=copy.deepcopy(value);edit(value)
            return value
        return patch.object(inventory,'read',side_effect=replacement)

    def test_valid_inventory(self):
        self.assertEqual(inventory.build()['coverage']['status'],'PASS_DOCUMENT_AND_DEPENDENCY_BINDING')

    def test_unknown_dependency_rejected(self):
        with self.altered(lambda r:r['new_derivations'][0]['dependencies'].append('missing:lemma')):
            with self.assertRaisesRegex(ValueError,'Dependency label absent'):inventory.build()

    def test_omitted_new_result_rejected(self):
        with self.altered(lambda r:r['new_derivations'].pop(0)):
            with self.assertRaisesRegex(ValueError,'New result omitted'):inventory.build()

    def test_changed_source_version_rejected(self):
        with self.altered(lambda r:r['source'].update(sha256='0'*64)):
            with self.assertRaisesRegex(ValueError,'Source edition mismatch'):inventory.build()

    def test_incomplete_conventions_rejected(self):
        with self.altered(lambda r:r['applications'][0].update(conventions='')):
            with self.assertRaisesRegex(ValueError,'Incomplete new application'):inventory.build()

    def test_new_assumption_rejected(self):
        with self.altered(lambda r:r['assumed_new_unpublished_results'].append('extra_prime_theorem')):
            with self.assertRaisesRegex(ValueError,'Unexpected new assumed result'):inventory.build()

if __name__=='__main__':unittest.main()
