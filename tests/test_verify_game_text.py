import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("verify_game_text", ROOT / "scripts/verify_game_text.py")
verify = importlib.util.module_from_spec(spec)
spec.loader.exec_module(verify)


class TextHandoffTests(unittest.TestCase):
    def setUp(self):
        self.folder = tempfile.TemporaryDirectory()
        self.addCleanup(self.folder.cleanup)
        self.path = Path(self.folder.name)

    def source(self, text):
        path = self.path / "draft.md"
        path.write_text(text, encoding="utf-8")
        return path

    def test_unicode_multiline_variables_tags_quotes_and_backslashes(self):
        body = '米露：还差 {count} 枚。\n<color=red>“返回”</color>  50%  C:\\save\\slot1'
        expected = verify.parse_source(self.source('## quest.need\n角色：米露\n~~~~text\n' + body + '\n~~~~\n'))
        target = self.path / "target.json"
        target.write_text(json.dumps(expected, ensure_ascii=True), encoding="utf-8")
        self.assertEqual([], verify.compare(expected, verify.load_actual(target)))
        self.assertEqual(body, expected['quest.need'])

    def test_missing_extra_and_changed_entries(self):
        self.assertEqual(['Missing: b', 'Unexpected: c', 'Text differs: a'],
                         verify.compare({'a': '{count}', 'b': '返回'}, {'a': '{amount}', 'c': '返回'}))

    def test_source_rejects_duplicate_id(self):
        with self.assertRaisesRegex(verify.VerificationError, 'Duplicate'):
            verify.parse_source(self.source('## a\n~~~~text\n甲\n~~~~\n## a\n~~~~text\n乙\n~~~~\n'))

    def test_export_rejects_duplicate_id(self):
        actual = self.path / 'actual.json'
        actual.write_text('{"a":"甲","a":"乙"}', encoding='utf-8')
        with self.assertRaisesRegex(verify.VerificationError, 'Duplicate'):
            verify.load_actual(actual)

    def test_rejects_unclosed_or_missing_text_block(self):
        for text in ['## a\n~~~~text\n甲', '## a\n角色：米露', '## a\n## b\n~~~~text\n乙\n~~~~']:
            with self.subTest(text=text), self.assertRaises(verify.VerificationError):
                verify.parse_source(self.source(text))

    def test_rejects_empty_document_and_multiple_blocks(self):
        for text in ['# 稿件\n无文本', '## a\n~~~~text\n甲\n~~~~\n~~~~text\n乙\n~~~~']:
            with self.subTest(text=text), self.assertRaises(verify.VerificationError):
                verify.parse_source(self.source(text))

    def test_preserves_spaces_and_blank_lines(self):
        expected = verify.parse_source(self.source('## a\n~~~~text\n  等等。\n\n还没结束。 \n~~~~\n'))
        self.assertEqual('  等等。\n\n还没结束。 ', expected['a'])
        self.assertTrue(verify.compare(expected, {'a': expected['a'].strip()}))

    def test_heading_like_text_inside_body_is_not_metadata(self):
        expected = verify.parse_source(self.source('## a\n~~~~text\n## b\n~~~~\n'))
        self.assertEqual({'a': '## b'}, expected)

    def test_unicode_separator_is_preserved_inside_text(self):
        body = '星灯🌙\u2028仍然亮着'
        expected = verify.parse_source(self.source('## a\n~~~~text\n' + body + '\n~~~~\n'))
        self.assertEqual(body, expected['a'])

    def test_rejects_non_string_export(self):
        actual = self.path / 'actual.json'
        for value in [[], {'a': 1}, {'a': None}]:
            actual.write_text(json.dumps(value), encoding='utf-8')
            with self.subTest(value=value), self.assertRaises(verify.VerificationError):
                verify.load_actual(actual)


if __name__ == '__main__':
    unittest.main()
