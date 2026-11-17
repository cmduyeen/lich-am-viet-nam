import hashlib
import json
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
BASE = 'https://raw.githubusercontent.com/cmduyeen/lich-am-viet-nam/main/output/'


class DocumentationTests(unittest.TestCase):
    def test_bilingual_readmes_have_valid_local_links_and_shared_cover(self):
        for name in ('README.md', 'README.en.md'):
            text = (ROOT / name).read_text(encoding='utf-8')
            self.assertIn('[Tiếng Việt](README.md)', text)
            self.assertIn('[English](README.en.md)', text)
            self.assertIn('](assets/lunar-calendar-cover.png)', text)
            self.assertNotIn('Global Lunar Calendars', text)
            for link in re.findall(r'\]\(([^)]+)\)', text):
                if '://' in link or link.startswith('#'):
                    continue
                target = (ROOT / link.split('#')[0]).resolve()
                self.assertTrue(target.is_relative_to(ROOT))
                self.assertTrue(target.is_file(), (name, link))

    def test_only_two_vietnamese_feeds_are_documented_and_published(self):
        entries = json.loads((ROOT / 'output/index.json').read_text(encoding='utf-8'))
        expected = {'viet_lunar_latest.ics', 'viet_lunar_en_latest.ics'}
        self.assertEqual({e['file'] for e in entries}, expected)
        self.assertEqual({e['language'] for e in entries}, {'vi', 'en'})
        for entry in entries:
            self.assertEqual(entry['countries'], ['VN'])
            raw = (ROOT / 'output' / entry['file']).read_bytes()
            self.assertEqual(hashlib.sha256(raw).hexdigest(), entry['sha256'])
        for name in ('README.md', 'README.en.md'):
            text = (ROOT / name).read_text(encoding='utf-8')
            urls = set(re.findall(re.escape(BASE) + r'([^\s)]+)', text))
            self.assertEqual(urls, expected)

    def test_foreign_public_guides_and_feeds_are_retired(self):
        for name in ('china', 'taiwan', 'hong-kong', 'macao', 'south-korea',
                     'singapore', 'malaysia', 'united-states'):
            self.assertFalse((ROOT / name).exists(), name)
        self.assertEqual({p.name for p in (ROOT / 'output').glob('*.ics')},
                         {'viet_lunar_latest.ics', 'viet_lunar_en_latest.ics'})
