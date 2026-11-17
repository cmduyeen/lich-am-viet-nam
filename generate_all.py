"""Build every implemented profile, validate everything, then update output.

--custom-config may be repeated on a fork to publish personalized subscriptions.
No network calls are made while generating calendars.
"""
import argparse
import hashlib
import json
from datetime import datetime
from pathlib import Path
import sys
import tempfile
from zoneinfo import ZoneInfo
from src.build import build_files
from src.output_lock import output_lock
from src.release_state import fingerprint, is_current, write_state
from src.ics import publish_staged, obsolete_exports
from src.naming import output_prefix
from src.config import resolve_year_range
from src.profiles import PROFILES, RESIDENCES, residence_languages, FESTIVAL_SOURCES
from src.user_config import CalendarOptions, load_calendar_options

ROOT=Path(__file__).resolve().parent



def unique_jobs(jobs):
    """A fork can select a published default config without duplicating output."""
    seen = {}
    result = []
    for options, first, last, is_new in jobs:
        prefix = output_prefix(options)
        settings = options.to_dict()
        for field in ('country', 'countries', 'tradition'):
            settings.pop(field, None)
        settings['source_countries'] = list(options.selected_countries)
        signature = (first, last, settings)
        if prefix in seen:
            if seen[prefix] != signature:
                raise ValueError(f'Conflicting configurations for feed: {prefix}')
            print(f'Reusing existing feed: {prefix}_latest.ics')
            continue
        seen[prefix] = signature
        result.append((options, first, last, is_new))
    return result


def main(argv=None):
    if hasattr(sys.stdout,'reconfigure'): sys.stdout.reconfigure(encoding='utf-8')
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--start',type=int)
    parser.add_argument('--end',type=int)
    parser.add_argument('--split',action='store_true')
    parser.add_argument('--if-needed',action='store_true',help='Skip generation when inputs and output checksums are unchanged')
    parser.add_argument('--output-dir',type=Path,default=ROOT/'output')
    parser.add_argument('--custom-config',type=Path,action='append',default=[])
    args=parser.parse_args(argv)
    current=datetime.now(ZoneInfo('Asia/Ho_Chi_Minh')).year
    try:
        start,end=resolve_year_range(current,args.start,args.end)
    except ValueError as exc:
        parser.error(str(exc))
    try:
        manifest=[]
        jobs=[]
        for profile in PROFILES.values():
            for language in profile.languages:
                for content in ('festivals','observances','daily'):
                    options=CalendarOptions(country=profile.code,tradition=profile.tradition,language=language,content=content)
                    jobs.append((options,start,end if args.end is not None else min(end,profile.last_year),True))
        for host in RESIDENCES.values():
            for tradition, code in host.traditions:
                profile = PROFILES[code]
                for language in residence_languages(host.code, profile):
                    for content in ('festivals', 'observances', 'daily'):
                        options = CalendarOptions(country=host.code, tradition=tradition,
                                                  language=language, content=content)
                        last = end if args.end is not None else min(end, profile.last_year)
                        jobs.append((options, start, last, True))
        # Existing subscriptions keep their filenames, identities and full content.
        for language in ('vi','en'):
            for minimal in (False,True):
                jobs.append((CalendarOptions(language=language,minimal=minimal),start,end if args.end is not None else min(end,PROFILES['VN'].last_year),False))
        merged_end=end if args.end is not None else min(end,PROFILES['VN'].last_year,PROFILES['CN'].last_year,PROFILES['KR'].last_year)
        jobs.append((CalendarOptions(countries=('VN','CN','KR'),language='en',content='festivals'),start,merged_end,True))
        for config in args.custom_config:
            options=load_calendar_options(config)
            first,last=resolve_year_range(current,
                options.start_year if options.start_year is not None else args.start,
                options.end_year if options.end_year is not None else args.end,
                min(PROFILES[c].last_year for c in options.selected_countries))
            jobs.append((options,first,last,False))
        jobs = unique_jobs(jobs)
        expected=fingerprint(year=current,custom_configs=args.custom_config,start=args.start,end=args.end,split=args.split)
        with output_lock(args.output_dir), tempfile.TemporaryDirectory(prefix='lunar-release-') as temp:
            if args.if_needed and is_current(args.output_dir,expected):
                print('Up to date: 0 changed files; skipped generation')
                return 0
            staging=Path(temp)
            prefixes=set()
            for options,first,last,is_new in jobs:
                calendar,files=build_files(options,first,last,staging,args.output_dir,args.split,latest_only=not args.split)
                latest=next(p for p in files if p.name.endswith('_latest.ics'))
                if latest.name in prefixes: raise ValueError(f'Duplicate output feed: {latest.name}')
                prefixes.add(latest.name)
                raw=latest.read_bytes()
                entry=dict(countries=list(options.selected_countries),tradition=options.tradition,
                                     language=options.language,content=options.content or ('minimal' if options.minimal else 'legacy-daily'),
                                     legacy=options.legacy,start_year=first,end_year=last,
                                     supported_end_year=min(PROFILES[c].last_year for c in options.selected_countries),
                                     events=len(calendar.walk('VEVENT')),file=latest.name,
                                     sha256=hashlib.sha256(raw).hexdigest(),
                                     sources=sorted({url for c in options.selected_countries for url in (*PROFILES[c].sources, *FESTIVAL_SOURCES.get(c,{}).values())}),
                                     date_status='calculated-traditional-observance',
                                     app_subscription_tested=False)
                if options.residence:
                    entry['residence']=options.residence
                    entry['residence_sources']=list(RESIDENCES[options.residence].sources)
                    entry['date_policy']='source-calendar-civil-date'
                manifest.append(entry)
                print(f'{latest.name}: {manifest[-1]["events"]} events')
            (staging/'index.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
            write_state(staging,expected)
            stale=obsolete_exports(args.output_dir,staging,manifest)
            changes=publish_staged(staging,args.output_dir,obsolete=stale)
    except (ValueError,OSError) as exc:
        parser.error(str(exc))
    print(f'{len(manifest)} feeds; {len(changes)} changed files')
    return 0


if __name__=='__main__':
    raise SystemExit(main())
