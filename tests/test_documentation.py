import json
from pathlib import Path
import re
import unittest
from src.documentation import GUIDES, LANGUAGE_NAMES
from src.naming import output_prefix
from src.user_config import CalendarOptions

ROOT = Path(__file__).resolve().parents[1]
BASE = 'https://raw.githubusercontent.com/cmduyeen/lich-am-viet-nam/main/output/'


class DocumentationTests(unittest.TestCase):
    def test_country_language_pairs_and_local_links(self):
        pages = [ROOT/'README.md', ROOT/'united-states/README.md']
        for guide in GUIDES:
            folder = ROOT/guide.folder
            native = f'README.{guide.native}.md'
            self.assertEqual({p.name for p in folder.glob('README*.md')}, {'README.md', native})
            self.assertTrue((folder/'calendar.config.json').is_file())
            for name in ('README.md', native):
                page = folder/name
                text = page.read_text(encoding='utf-8')
                first = text.splitlines()[0]
                self.assertIn('[English](README.md)', first)
                self.assertIn(f'[{LANGUAGE_NAMES[guide.native]}]({native})', first)
                pages.append(page)
        self.assertFalse((ROOT/'docs/i18n').exists())
        for page in pages:
            text = page.read_text(encoding='utf-8')
            for link in re.findall(r'\]\(([^)]+)\)', text):
                if '://' in link or link.startswith('#'):
                    continue
                target = (page.parent/link.split('#')[0]).resolve()
                self.assertTrue(target.exists(), (page, link))
                self.assertTrue(target.is_relative_to(ROOT), (page, link))

    def test_copyable_urls_cover_the_published_inventory(self):
        inventory = json.loads((ROOT/'output/index.json').read_text(encoding='utf-8'))
        expected = {entry['file'] for entry in inventory if not entry['legacy'] and len(entry['countries']) == 1}
        combined = set()
        for guide in GUIDES:
            for language, name in [('en', 'README.md'), (guide.native, f'README.{guide.native}.md')]:
                path = ROOT/guide.folder/name
                text = path.read_text(encoding='utf-8')
                files = set(re.findall(re.escape(BASE)+r'([^\s)]+)', text))
                scoped = set()
                for content in ('festivals', 'observances', 'daily'):
                    options = CalendarOptions.from_mapping({**guide.settings(language), 'content': content})
                    scoped.add(output_prefix(options)+'_latest.ics')
                if guide.source == 'MY' and language == 'en':
                    for content in ('festivals', 'observances', 'daily'):
                        options = CalendarOptions(country='MY', tradition='chinese', language='zh-Hans', content=content)
                        scoped.add(output_prefix(options)+'_latest.ics')
                self.assertEqual(files, scoped, path)
                blocks = re.findall(r'```text\n(https://[^\n]+)\n```', text)
                self.assertEqual(len(blocks), len(files), path)
                for filename in files:
                    self.assertTrue((ROOT/'output'/filename).exists(), filename)
                combined.update(files)
        self.assertEqual(combined, expected)

    def test_configs_and_code_examples_select_the_right_profile(self):
        for guide in GUIDES:
            folder = ROOT/guide.folder
            config = CalendarOptions.from_mapping(json.loads((folder/'calendar.config.json').read_text(encoding='utf-8')))
            self.assertEqual(config.country, guide.source)
            self.assertEqual(config.residence, guide.residence)
            self.assertEqual(config.language, guide.native)
            for name in ('README.md', f'README.{guide.native}.md'):
                text = (folder/name).read_text(encoding='utf-8')
                sample, = re.findall(r'```json\n(.*?)\n```', text, re.S)
                parsed = CalendarOptions.from_mapping(json.loads(sample))
                self.assertEqual(parsed.country, guide.source)
                self.assertEqual(parsed.residence, guide.residence)
                for flag in ('--config', '--language', '--split', '--countries'):
                    self.assertIn(flag, text)
                self.assertIn('CUSTOM_CONFIG', text)
                self.assertIn(f'{guide.folder}/calendar.config.json', text)
