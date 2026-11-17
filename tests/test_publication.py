import subprocess
import json
import tempfile
import unittest
from pathlib import Path

from src.publication import stage_public_outputs, public_paths


class PublicationTests(unittest.TestCase):
    def test_inventory_and_state_are_published_without_unrelated_private_files(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            subprocess.run(['git', 'init', '-q', folder], check=True)
            output = root / 'output'
            output.mkdir()
            names = ('viet_lunar_latest.ics', 'viet_lunar_en_latest.ics')
            for name in (*names, 'personal.ics', 'credentials.json', '.build-state.json'):
                (output / name).write_text('test')
            (output / 'index.json').write_text(json.dumps([{'file': name} for name in names]))
            self.assertEqual(set(public_paths(root)), {
                'output/viet_lunar_latest.ics', 'output/viet_lunar_en_latest.ics',
                'output/index.json', 'output/.build-state.json',
            })
            (output / 'index.json').write_text(json.dumps([{'file': 'personal.ics'}]))
            with self.assertRaisesRegex(ValueError, 'keep custom feeds local'):
                stage_public_outputs(root)
            staged = subprocess.check_output(['git', 'diff', '--cached', '--name-only'], cwd=root)
            self.assertEqual(staged, b'')

    def test_only_standard_exports_are_staged_including_retired_files(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            subprocess.run(['git', 'init', '-q', folder], check=True)
            output = root / 'output'
            output.mkdir()
            retired = output / 'viet_lunar_2025.ics'
            retired.write_text('retired', encoding='utf-8')
            subprocess.run(['git', 'add', 'output/viet_lunar_2025.ics'], cwd=root, check=True)
            retired.unlink()
            for name in ('viet_lunar_latest.ics', 'viet_lunar_en_2026.ics',
                         'update-status.json', 'viet_lunar_custom_vi_latest.ics',
                         'personal.ics', '.env', 'credentials.json'):
                (output / name).write_text('test', encoding='utf-8')
            stage_public_outputs(root)
            paths = subprocess.check_output(
                ['git', 'diff', '--cached', '--name-only'], cwd=root, text=True,
            ).splitlines()
            self.assertEqual(set(paths), {
                'output/viet_lunar_latest.ics', 'output/viet_lunar_en_2026.ics',
                'output/update-status.json',
            })

    def test_personal_paths_are_ignored_by_git(self):
        result = subprocess.run(
            ['git', 'check-ignore', '--stdin'], input=(
                '.local/holidays.json\n.local/output/calendar.ics\n.env\n'
                'output/viet_lunar_custom_en_latest.ics\ncredentials.json\nbackup.bundle\n'
            ).encode('utf-8'), capture_output=True, check=True,
        )
        self.assertEqual(len(result.stdout.splitlines()), 6)
