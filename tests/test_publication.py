import subprocess
import tempfile
import unittest
from pathlib import Path

from src.publication import stage_public_outputs


class PublicationTests(unittest.TestCase):
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
