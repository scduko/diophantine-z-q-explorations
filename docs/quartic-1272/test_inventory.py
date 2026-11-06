"""Adversarial document-binding checks; these do not test mathematical truth."""
import copy
import unittest
from unittest.mock import patch

import inventory


class InventoryBindingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.repo = inventory.DEFAULT_REPO
        cls.path = 'quartic_1272.tex'
        cls.inputs = inventory.load(cls.repo, inventory.NEW + 'new-applications.json')
        cls.raw = inventory.read(cls.repo, cls.path)

    def collect_modified(self, replacement, inputs=None):
        real_read = inventory.read
        def read(repo, path):
            return replacement if path == self.path else real_read(repo, path)
        with patch.object(inventory, 'read', read):
            return inventory.collect(self.repo, self.path, inputs or self.inputs)['coverage.json']

    def append_before_bibliography(self, text):
        needle = b'\\begin{thebibliography}'
        self.assertEqual(self.raw.count(needle), 1)
        return self.raw.replace(needle, text.encode() + b'\n\n' + needle)

    def test_current_inventory_closes_document_checks(self):
        self.assertEqual(self.collect_modified(self.raw)['status'], 'PASS_DOCUMENT_BINDING')

    def test_reviewed_mathematics_cannot_be_rebuilt_without_review(self):
        replacement = self.raw.replace(b'\\label{lem:v5-three-witness-anchor}',
                                       b'\\label{lem:v5-three-witness-anchor} altered', 1)
        with self.assertRaisesRegex(ValueError, 'Reviewed fragment must occur exactly once'):
            self.collect_modified(replacement)

    def test_new_citation_needs_application_record(self):
        coverage = self.collect_modified(self.append_before_bibliography(r'An added unreviewed use of \cite{silverman}.'))
        self.assertTrue(coverage['unregistered_citations'])
        self.assertEqual(coverage['status'], 'REVIEW_ITEMS_REMAIN')

    def test_new_lemma_needs_review(self):
        coverage = self.collect_modified(self.append_before_bibliography(r'\begin{lemma}\label{test:unreviewed}1=1.\end{lemma}'))
        self.assertIn('test:unreviewed', coverage['new_results_without_review_record'])

    def test_broken_reference_is_reported(self):
        coverage = self.collect_modified(self.append_before_bibliography(r'\ref{test:missing}'))
        self.assertIn('test:missing', [x['label'] for x in coverage['unresolved_references']])

    def test_old_source_excerpt_change_breaks_bridge(self):
        old = inventory.Tex(inventory.read(self.repo, inventory.OLD_TEX), inventory.OLD_TEX)
        source = inventory.load(self.repo, inventory.V4 + 'baseline-bridge.json')['anchors'][0]['version4_location']
        start, end = source['start_character'], source['end_character']
        excerpt = old.text[start:end].encode()
        # Work in normalized text because manuscript line endings may differ.
        raw = inventory.tex_text(self.raw).encode()
        self.assertEqual(raw.count(excerpt), 1)
        self.assertIn(b' ', excerpt)
        coverage = self.collect_modified(raw.replace(excerpt, excerpt.replace(b' ', b' changed ', 1)))
        self.assertTrue(coverage['unresolved_application_bridges'])

    def test_pinned_review_evidence_cannot_change_silently(self):
        changed = copy.deepcopy(self.inputs)
        changed['evidence_pins'][0]['sha256'] = '0' * 64
        with self.assertRaisesRegex(ValueError, 'Review evidence changed'):
            self.collect_modified(self.raw, changed)

    def test_undeclared_dependency_is_reported(self):
        changed = copy.deepcopy(self.inputs)
        changed['current_consumption'][0]['depends_on'].append('test:missing-dependency')
        coverage = self.collect_modified(self.raw, changed)
        self.assertTrue(coverage['unresolved_declared_dependencies'])


if __name__ == '__main__':
    unittest.main()
