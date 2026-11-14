"""One pipeline for country profiles, semantic merging and all languages."""
from .colors import add_event_color
from collections import defaultdict
from dataclasses import dataclass, replace
from functools import lru_cache
from types import MappingProxyType
from datetime import date, datetime, timedelta, timezone
from icalendar import Calendar, Event
from .engines import ENGINES
from .localization import LOCALES, lunar_label, title, validate_translations
from .profiles import get_profile, RULES, SOLAR_TERMS, SOLAR_RULES

# Initial revision is reproducible; the writer advances changed events using their
# existing UID/SEQUENCE, rather than changing all timestamps on every scheduled run.
INITIAL_REVISION = datetime(2026,11,14,tzinfo=timezone.utc)


@dataclass(frozen=True)
class Occurrence:
    country: str
    identity: str
    lunar: object
    category: str


def validate_range(start, end, options):
    if isinstance(start,bool) or isinstance(end,bool) or not isinstance(start,int) or not isinstance(end,int) or start>end:
        raise ValueError('start_year must be less than or equal to end_year')
    for code in options.selected_countries:
        profile=get_profile(code)
        if not profile.first_year <= start <= end <= profile.last_year:
            raise ValueError(f'{code} supports {profile.first_year}-{profile.last_year}; requested {start}-{end}')


def occurrences(start, end, options):
    """Cache semantics independently of display language, color and residence."""
    validate_range(start, end, options)
    codes = options.selected_countries
    traditions = {get_profile(c).tradition for c in codes}
    shared = replace(options, country=codes[0], countries=codes if len(codes)>1 else (),
        tradition=next(iter(traditions)) if len(traditions)==1 else None,
        language="en", residence=None, feed_name=None, start_year=None, end_year=None,
        calendar_color="#E53935", holiday_color=None, lunar_day_color="#FB8C00", ordinary_color="#1E88E5")
    return _collect_occurrences(start, end, shared)


@lru_cache(maxsize=64)
def _collect_occurrences(start, end, options):
    """Collect identities before translation. No matching by localized strings."""
    validate_range(start,end,options)
    grouped=defaultdict(list)
    first,last=date(start,1,1),date(end,12,31)
    for code in options.selected_countries:
        profile=get_profile(code)
        convert=ENGINES[profile.engine]
        rules=defaultdict(list)
        for month, lunar_day, identity in RULES[code]:
            rules[month,lunar_day].append(identity)
        solar={(m,d):identity for m,d,identity in SOLAR_RULES.get(code,())}
        for offset in range((last-first).days+1):
            day=first+timedelta(days=offset)
            lunar=convert(day)
            hits=[]
            if options.minimal:
                if lunar.day==15: hits.append(('full_moon','observance'))
                elif lunar.day==1 and lunar.month==1 and not lunar.leap: hits.append(('lunar_new_year','lunar'))
            else:
                if 'lunar' in options.holiday_types:
                    if not lunar.leap or profile.leap_festivals:
                        hits.extend((identity,'lunar') for identity in rules.get((lunar.month,lunar.day),()))
                        if lunar.month==12 and lunar.day>=29:
                            following=convert(day+timedelta(days=1))
                            if following.month==1 and following.day==1 and not following.leap:
                                hits.append(('new_year_eve','lunar'))
                if 'solar' in options.holiday_types:
                    if (day.month,day.day) in solar:
                        hits.append((solar[day.month,day.day],'solar'))
                    identity=SOLAR_TERMS.get(code,{}).get(lunar.solar_term)
                    if identity: hits.append((identity,'solar_term'))
                content=options.content or 'festivals'
                selected = options.lunar_days is not None and lunar.day in options.lunar_days
                if options.lunar_days is None:
                    selected=content=='daily' or (content=='observances' and lunar.day in (1,15))
                if selected:
                    # Daily labels are independent of festivals, but avoid a duplicate
                    # background event on days already represented by a festival.
                    if not hits:
                        identity='new_moon' if lunar.day==1 else 'full_moon' if lunar.day==15 else 'lunar_day'
                        hits.append((identity,'observance' if lunar.day in (1,15) else 'daily'))
            for identity,category in hits:
                # A daily label can only be merged when the actual lunar date agrees.
                key_identity=identity
                if identity=='lunar_day':
                    key_identity=f'lunar_day_{lunar.year}_{lunar.month}_{lunar.day}_{int(lunar.leap)}'
                grouped[(day,key_identity)].append(Occurrence(code,identity,lunar,category))
    return MappingProxyType({key:tuple(items) for key,items in grouped.items()})


def generate(start, end, options):
    validate_translations()
    grouped=occurrences(start,end,options)
    locale=LOCALES[options.language]
    codes=options.selected_countries
    calendar=Calendar()
    product='Global' if options.residence else 'Asian'
    calendar.add('prodid',f'-//cmduyeen//{product} Lunar Calendars//'+options.language)
    calendar.add('version','2.0')
    calendar.add('calscale','GREGORIAN')
    calendar.add('method','PUBLISH')
    mode='minimal' if options.minimal else options.content or 'festivals'
    label=locale['calendar'] if mode=='festivals' else locale[mode]
    names=' / '.join(locale['country_names'][code] for code in codes)
    if options.residence:
        names=locale['country_names'][options.residence]+' — '+names
        calendar.add('x-residence',options.residence)
        calendar.add('x-source-countries',','.join(codes))
    calendar.add('x-wr-calname',f'{names} — {label} {start}–{end}')
    if len(codes)==1 and not options.residence:
        calendar.add('x-wr-timezone',get_profile(codes[0]).timezone)
    residence_note=locale['residence_note'] if options.residence else ''
    calendar.add('x-wr-caldesc',locale['notice']+' '+locale['moon_note']+(' '+residence_note if residence_note else ''))
    calendar.add('x-apple-calendar-color',options.calendar_color)
    scope='-'.join(code.lower() for code in codes)
    if options.residence:
        scope=options.residence.lower()+'-'+scope
    for (day,key),items in sorted(grouped.items()):
        event=Event()
        titles=[]
        descriptions=[]
        applies=sorted({item.country for item in items})
        for item in items:
            name=lunar_label(item.lunar,options.language) if item.identity=='lunar_day' else title(item.country,options.language,item.identity)
            if name not in titles: titles.append(name)
            descriptions.append(locale['country_names'][item.country]+': '+name+'\n'+lunar_label(item.lunar,options.language))
        summary=' / '.join(titles)
        if len(codes)>1: summary+=' ['+', '.join(applies)+']'
        # A corrected festival date must update the existing occurrence, not
        # create a second event. Membership distinguishes split country dates.
        category=items[0].category
        if category in ('solar','solar_term'):
            occurrence=str(day.year)
        elif category=='lunar':
            occurrence='-'.join(str(y) for y in sorted({i.lunar.year for i in items}))
        else:
            occurrence='-'.join(sorted({f'{i.lunar.year:04d}{i.lunar.month:02d}{i.lunar.day:02d}{int(i.lunar.leap)}' for i in items}))
        membership='-'.join(c.lower() for c in applies)
        event.add('uid',f'lunar-{scope}-{mode}-{key}-{membership}-{occurrence}@cmduyeen')
        event.add('summary',summary)
        event.add('description','\n\n'.join(descriptions)+'\n\n'+locale['notice']+
                  ('\n'+locale['moon_note'] if any(i.identity=='full_moon' for i in items) else '')+
                  ('\n'+residence_note if residence_note else ''))
        event.add('dtstart',day)
        event.add('dtend',day+timedelta(days=1))
        event.add('dtstamp',INITIAL_REVISION)
        event.add('sequence',0)
        event.add('transp','TRANSPARENT')
        event.add('x-lunar-event-id',items[0].identity)
        event.add('x-countries',','.join(applies))
        if options.residence:
            event.add('x-residence',options.residence)
        event.add('x-event-category',items[0].category)
        holiday=any(i.category in ('lunar','solar','solar_term') for i in items)
        add_event_color(event,(options.holiday_color or '#E53935') if holiday else options.lunar_day_color if items[0].category=='observance' else options.ordinary_color)
        calendar.add_component(event)
    return calendar
