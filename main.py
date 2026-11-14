"""Generate a traditional lunar calendar, or preserve the original Vietnamese feed.

No arguments: original full Vietnamese calendar.
--country VN: new festival-only Vietnamese calendar.
--countries VN,CN,KR --language en: one semantically merged festival feed.
"""
import argparse
import json
from datetime import datetime
from pathlib import Path
import re
import sys
import tempfile
from zoneinfo import ZoneInfo
from src.user_config import CalendarOptions, parse_lunar_days, parse_holiday_types
from src.profiles import PROFILES, RESIDENCES, get_profile
from src.naming import output_prefix as _output_prefix
from src.ics import create_zip as create_zip_archive, publish_staged
from src.build import build_files
from src.output_lock import output_lock
from src.config import resolve_year_range

ROOT_DIR=Path(__file__).resolve().parent


def cleanup_past_files(output_path,current_year,output_prefix='viet_lunar'):
    """Compatibility helper, restricted to a single exact feed prefix."""
    folder=Path(output_path)
    removed=[]
    pattern=re.compile('^'+re.escape(output_prefix)+r'_(?:yearly_)?(\d{4})(?:_\d{4})?\.(?:ics|zip)$')
    for path in folder.iterdir() if folder.exists() else ():
        match=pattern.fullmatch(path.name)
        if path.is_file() and match and int(match.group(1))<current_year:
            path.unlink()
            removed.append(path.name)
    return removed


def count_events(filepath):
    return Path(filepath).read_bytes().count(b'BEGIN:VEVENT\r\n')


def main(argv=None):
    if hasattr(sys.stdout,'reconfigure'): sys.stdout.reconfigure(encoding='utf-8')
    parser=argparse.ArgumentParser(description=__doc__,formatter_class=argparse.RawDescriptionHelpFormatter,argument_default=argparse.SUPPRESS)
    group=parser.add_mutually_exclusive_group()
    group.add_argument('--country',type=str.upper)
    group.add_argument('--countries',help='Comma-separated country codes')
    parser.add_argument('--tradition')
    parser.add_argument('--residence',type=str.upper,help='Where you live, e.g. US; keeps source-calendar civil dates')
    parser.add_argument('--language',help='en, vi, zh-Hans, zh-Hant, ko, ms or native')
    parser.add_argument('--content',choices=('festivals','observances','daily'))
    parser.add_argument('--minimal',action='store_true',help='Legacy Full Moon and Lunar New Year mode; incompatible with --content')
    parser.add_argument('--feed-name',help='Stable custom subscription name, e.g. my-calendar')
    parser.add_argument('--config',type=Path)
    parser.add_argument('--start',type=int)
    parser.add_argument('--end',type=int)
    parser.add_argument('--year',type=int)
    parser.add_argument('--lunar-days',help='all, none, or comma-separated days 1-30')
    parser.add_argument('--holiday-types',help='all, none, solar, lunar or solar,lunar')
    for key in ('calendar','holiday','lunar-day','ordinary'):
        parser.add_argument(f'--{key}-color',metavar='#RRGGBB')
    parser.add_argument('--split',action='store_true')
    parser.add_argument('--output-dir',type=Path,default=ROOT_DIR/'output')
    parser.add_argument('--list-countries',action='store_true')
    args=vars(parser.parse_args(argv))
    if args.get('list_countries'):
        for p in PROFILES.values():
            print(f'{p.code} | {p.tradition} | {", ".join(p.languages)} | {p.first_year}-{p.last_year}')
        for host in RESIDENCES.values():
            print(f'{host.code} | residence | traditions: {", ".join(dict(host.traditions))}; language native=en')
        return 0
    try:
        data={}
        if 'config' in args:
            data=json.loads(args['config'].read_text(encoding='utf-8-sig'))
            if not isinstance(data,dict): raise ValueError('configuration root must be a JSON object')
        data=dict(data)
        # An explicit CLI profile replaces a JSON profile and its default language.
        if 'countries' in args or ('country' in args and ('countries' in data or args['country'] != data.get('country','VN'))):
            for key in ('country','countries','language','tradition'): data.pop(key,None)
        for key in ('feed_name','country','residence','tradition','language','content','minimal'):
            if key in args: data[key]=args[key]
        if 'countries' in args: data['countries']=[c.strip().upper() for c in args['countries'].split(',')]
        if 'start' in args: data['start_year']=args['start']
        if 'end' in args: data['end_year']=args['end']
        if 'year' in args: data.update(start_year=args['year'],end_year=args['year'])
        if 'lunar_days' in args:
            days=parse_lunar_days(args['lunar_days'])
            data['lunar_days']='all' if days is None else sorted(days)
        if 'holiday_types' in args: data['holiday_types']=sorted(parse_holiday_types(args['holiday_types']))
        colors=data.get('colors',{})
        if not isinstance(colors,dict): raise ValueError('colors must be an object')
        colors=dict(colors)
        for key in ('calendar','holiday','lunar_day','ordinary'):
            if key+'_color' in args: colors[key]=args[key+'_color']
        if colors: data['colors']=colors
        options=CalendarOptions.from_mapping(data)
        current=datetime.now(ZoneInfo(get_profile(options.selected_countries[0]).timezone)).year
        start,end=resolve_year_range(current,options.start_year,options.end_year,
                                    min(get_profile(c).last_year for c in options.selected_countries))
        output=args['output_dir']
        # All generation and wire-format checks finish before touching output.
        with output_lock(output), tempfile.TemporaryDirectory(prefix='lunar-build-') as temp:
            calendar,files=build_files(options,start,end,Path(temp),output,args.get('split',False),'year' in args,
                                       latest_only=not args.get('split',False) and 'year' not in args)
            changes=publish_staged(temp,output)
        print(f'{options.residence + " / " if options.residence else ""}{", ".join(options.selected_countries)} | {options.language} | {start}-{end} | {len(calendar.walk("VEVENT"))} events')
        for file in files: print(str(output/file.name))
        print(f'{len(changes)} files updated')
    except (ValueError,TypeError,KeyError,OSError,json.JSONDecodeError) as exc:
        parser.error(str(exc))
    return 0


if __name__=='__main__':
    raise SystemExit(main())
