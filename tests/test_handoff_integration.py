"""Fixture integration only; this does not claim to test a real game engine."""
import copy
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('verify_game_text', ROOT / 'scripts/verify_game_text.py')
verify = importlib.util.module_from_spec(spec)
spec.loader.exec_module(verify)

MAPPING = {
    'tower.need_stones': ('nodes', 'need_stones', 'text'),
    'tower.leave': ('nodes', 'leave', 'text'),
    'tower.goodbye': ('nodes', 'goodbye', 'text'),
    'ui.overwrite.title': ('ui', 'overwrite', 'title'),
    'ui.overwrite.body': ('ui', 'overwrite', 'body'),
    'ui.overwrite.confirm': ('ui', 'overwrite', 'confirm'),
    'ui.overwrite.cancel': ('ui', 'overwrite', 'cancel'),
    'ui.stones': ('ui', 'stones'),
}


def get_path(obj, path):
    for part in path:
        obj = obj[part]
    return obj


def integrate_fixture(output_dir):
    # Load reviewed text before writing any new game text.
    expected = verify.parse_source(ROOT / 'tests/fixtures/game-draft.md')
    before = json.loads((ROOT / 'tests/fixtures/game-before.json').read_text(encoding='utf-8'))
    after = copy.deepcopy(before)
    for key, path in MAPPING.items():
        parent = get_path(after, path[:-1])
        parent[path[-1]] = expected[key]
    output_dir.mkdir(parents=True, exist_ok=True)
    target = output_dir / 'game-after.json'
    target.write_text(json.dumps(after, ensure_ascii=True, indent=2) + '\n', encoding='utf-8')
    # Export from the serialized target, not from the source text or in-memory after.
    decoded_target = json.loads(target.read_text(encoding='utf-8'))
    exported = {key: get_path(decoded_target, path) for key, path in MAPPING.items()}
    (output_dir / 'decoded-export.json').write_text(
        json.dumps(exported, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    return expected, before, decoded_target, exported


class IntegrationTests(unittest.TestCase):
    def setUp(self):
        self.folder = tempfile.TemporaryDirectory()
        self.addCleanup(self.folder.cleanup)
        self.expected, self.before, self.after, self.exported = integrate_fixture(Path(self.folder.name))

    def test_actual_file_roundtrip_matches_all_eight_entries(self):
        self.assertEqual(8, len(self.expected))
        self.assertEqual([], verify.compare(self.expected, self.exported))

    def test_bindings_branches_and_unrelated_content_unchanged(self):
        restored = copy.deepcopy(self.after)
        for path in MAPPING.values():
            get_path(restored, path[:-1])[path[-1]] = get_path(self.before, path)
        self.assertEqual(self.before, restored)
        self.assertEqual('西洛', self.after['nodes']['need_stones']['speaker'])
        self.assertEqual('stones < 3', self.after['nodes']['need_stones']['condition'])
        self.assertEqual('leave', self.after['nodes']['need_stones']['next'])
        self.assertNotIn('action', self.after['nodes']['need_stones'])

    def test_missing_variable_and_swapped_nodes_are_detected(self):
        corrupted = dict(self.exported)
        corrupted['tower.need_stones'] = corrupted['tower.need_stones'].replace('{missing}', '3')
        self.assertEqual(['Text differs: tower.need_stones'], verify.compare(self.expected, corrupted))
        corrupted = dict(self.exported)
        corrupted['tower.leave'], corrupted['tower.goodbye'] = corrupted['tower.goodbye'], corrupted['tower.leave']
        self.assertEqual(2, len(verify.compare(self.expected, corrupted)))

    def test_ui_limits_and_required_consequence(self):
        ui = self.after['ui']['overwrite']
        self.assertLessEqual(len(ui['title']), 8)
        self.assertLessEqual(len(ui['confirm']), 4)
        self.assertLessEqual(len(ui['cancel']), 4)
        self.assertIn('手动存档将被替换', ui['body'])
        self.assertIn('自动存档不受影响', ui['body'])


if __name__ == '__main__':
    unittest.main()
