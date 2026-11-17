from contextlib import redirect_stdout, redirect_stderr
import io
import json
from pathlib import Path
import tempfile
import unittest

from generate_all import main
from src.ics import validate_bytes


class VietnamesePublicationTests(unittest.TestCase):
    def test_bilingual_build_retires_indexed_foreign_feed_and_preserves_private_file(self):
        with tempfile.TemporaryDirectory() as folder:
            output = Path(folder)
            foreign = output / 'lunar_cn_chinese_en_daily_latest.ics'
            foreign.write_bytes(b'old foreign feed')
            private = output / 'personal.ics'
            private.write_bytes(b'private data')
            (output / 'index.json').write_text(json.dumps([{'file': foreign.name}]))
            with redirect_stdout(io.StringIO()):
                main(['--start', '2026', '--end', '2026', '--output-dir', folder])
            self.assertFalse(foreign.exists())
            self.assertEqual(private.read_bytes(), b'private data')
            entries = json.loads((output / 'index.json').read_text())
            self.assertEqual(len(entries), 2)
            calendars = [validate_bytes((output / e['file']).read_bytes()) for e in entries]
            dates = [[e.decoded('dtstart') for e in c.walk('VEVENT')] for c in calendars]
            self.assertEqual(dates[0], dates[1])
            self.assertEqual(len(dates[0]), 365)

    def test_foreign_batch_customization_is_rejected_before_writing(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            config = root / 'config.json'
            config.write_text(json.dumps({'country': 'KR', 'language': 'en'}))
            output = root / 'output'
            with redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
                main(['--custom-config', str(config), '--output-dir', str(output)])
            self.assertFalse(output.exists())
