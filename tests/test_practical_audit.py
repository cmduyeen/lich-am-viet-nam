from dataclasses import replace
from contextlib import redirect_stderr
import io
import tempfile
from pathlib import Path
import unittest
from icalendar import Event
from src.colors import add_event_color, PALETTE
from src.user_config import CalendarOptions
from src.naming import output_prefix
from src.ics import obsolete_exports
from generate_all import main, unique_jobs

class PracticalAuditTests(unittest.TestCase):
    def test_custom_subscription_name_survives_settings_changes(self):
        a=CalendarOptions(country='VN',content='festivals',feed_name='family')
        b=replace(a,holiday_color='#123ABC',start_year=2027,content='daily')
        self.assertEqual(output_prefix(a),'custom_family')
        self.assertEqual(output_prefix(a),output_prefix(b))
        self.assertEqual(CalendarOptions.from_mapping(b.to_dict()),b)
        with self.assertRaisesRegex(ValueError,'Conflicting'):
            unique_jobs([(a,2026,2027,False),(b,2026,2027,False)])

    def test_unsafe_names_are_rejected(self):
        for name in ('../x','A','',True,'a/b','a'*65):
            with self.subTest(name=name), self.assertRaises(ValueError):
                CalendarOptions(feed_name=name)

    def test_invalid_batch_config_has_no_traceback_or_output(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp); out=root/'output'
            bad=root/'bad.json';bad.write_text('{',encoding='utf-8')
            for config in (bad,root/'missing.json'):
                error=io.StringIO()
                with redirect_stderr(error), self.assertRaises(SystemExit) as result:
                    main(['--custom-config',str(config),'--output-dir',str(out)])
                self.assertEqual(result.exception.code,2)
                self.assertNotIn('Traceback',error.getvalue())
                self.assertFalse(out.exists())

    def test_event_color_is_named_and_preserves_exact_rgb(self):
        for color in ('#123ABC','#E53935','#000000','#FFFFFF'):
            e=Event();add_event_color(e,color)
            self.assertIn(str(e['color']),PALETTE)
            self.assertEqual(str(e['x-lunar-color']),color)

    def test_named_custom_snapshots_are_not_pruned(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);out=root/'out';stage=root/'stage'
            out.mkdir();stage.mkdir();(out/'custom_family_2026.ics').touch()
            self.assertEqual(obsolete_exports(out,stage,[{'file':'custom_family_latest.ics'}]),[])
