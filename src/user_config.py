"""Validated immutable options shared by CLI, JSON configuration and generators."""
from __future__ import annotations
import json
import re
from dataclasses import dataclass
from pathlib import Path
from .profiles import get_profile, resolve_language, get_residence, RESIDENCES

_HOLIDAY_TYPES = frozenset({'solar','lunar'})
_COLOR_PATTERN = re.compile(r'^#[0-9a-fA-F]{6}$')


def _validate_year(value, field):
    if value is not None and (isinstance(value,bool) or not isinstance(value,int) or not 1 <= value <= 9998):
        raise ValueError(f'{field} must be an integer between 1 and 9998')
    return value


def _validate_color(value, field):
    if not isinstance(value,str) or not _COLOR_PATTERN.fullmatch(value):
        raise ValueError(f'{field} must be a six-digit hex color such as #E53935')
    return value.upper()


@dataclass(frozen=True)
class CalendarOptions:
    feed_name: str | None = None
    country: str = 'VN'
    residence: str | None = None
    countries: tuple[str,...] = ()
    tradition: str | None = None
    language: str | None = None
    content: str | None = None
    minimal: bool = False
    subdivision: str | None = None
    start_year: int | None = None
    end_year: int | None = None
    lunar_days: frozenset[int] | None = None
    holiday_types: frozenset[str] | None = None
    calendar_color: str = '#E53935'
    holiday_color: str | None = None
    lunar_day_color: str = '#FB8C00'
    ordinary_color: str = '#1E88E5'

    def __post_init__(self):
        if self.feed_name is not None and (not isinstance(self.feed_name, str) or not re.fullmatch(r"[a-z0-9][a-z0-9-]{0,63}", self.feed_name)):
            raise ValueError("feed_name must be 1-64 lowercase letters, digits or hyphens")
        if self.tradition is not None and not isinstance(self.tradition,str):
            raise ValueError('tradition must be a string')
        if not isinstance(self.countries,(tuple,list)):
            raise ValueError('countries must be a list of country codes')
        requested = self.country.upper() if isinstance(self.country, str) else self.country
        if requested in RESIDENCES:
            host = get_residence(requested)
            if self.residence is not None and get_residence(self.residence).code != host.code:
                raise ValueError('country and residence identify different places')
            if self.countries:
                raise ValueError('Use --residence with --countries to select source calendars')
            sources = dict(host.traditions)
            if self.tradition not in sources:
                raise ValueError(f'{host.code} requires --tradition: {", ".join(sources)}')
            object.__setattr__(self, 'country', sources[self.tradition])
            object.__setattr__(self, 'residence', host.code)
        if self.residence is not None:
            object.__setattr__(self, 'residence', get_residence(self.residence).code)
        if not isinstance(self.minimal,bool):
            raise ValueError('minimal must be a boolean')
        if self.subdivision is not None:
            raise ValueError('Subdivisions are not part of the published traditional-festival profiles')
        if isinstance(self.countries,str):
            raise ValueError('countries must be a list of country codes')
        selected = tuple(sorted({get_profile(c).code for c in self.countries}))
        profile = get_profile(self.country)
        object.__setattr__(self,'country',profile.code)
        object.__setattr__(self,'countries',selected)
        profiles = [get_profile(c) for c in self.selected_countries]
        if self.residence and len(profiles)==1 and self.tradition is None:
            object.__setattr__(self,'tradition',profiles[0].tradition)
        if len(profiles)==1 and profiles[0].code in ('SG','MY') and self.tradition != 'chinese':
            raise ValueError('SG and MY require --tradition chinese; other traditions are not implemented')
        if self.tradition is not None and any(p.tradition != self.tradition for p in profiles):
            raise ValueError('tradition does not match the selected country profiles')
        language = 'en' if self.residence and self.language == 'native' else self.language
        if len(profiles)>1:
            if language == 'native':
                raise ValueError('A merged feed needs one shared language; use --language en')
            language = language or 'en'
        for p in profiles:
            resolved = resolve_language(p,language,self.residence)
            if language in (None,'native'):
                language = resolved
        object.__setattr__(self,'language',language)
        if self.content is not None and self.content not in ('festivals','observances','daily'):
            raise ValueError('content must be festivals, observances or daily')
        if self.content is None and not self.minimal and (self.country != 'VN' or selected or self.residence):
            object.__setattr__(self,'content','festivals')
        if self.minimal and (self.selected_countries != ('VN',) or self.residence):
            raise ValueError('--minimal is a legacy Vietnamese mode; use --content observances for other profiles')
        if self.minimal and self.content is not None:
            raise ValueError('--minimal is a legacy mode; do not combine it with --content')
        for field in ('start_year','end_year'):
            _validate_year(getattr(self,field),field)
        if self.start_year is not None and self.end_year is not None and self.start_year>self.end_year:
            raise ValueError('start_year must be less than or equal to end_year')
        if self.lunar_days is not None:
            days=frozenset(self.lunar_days)
            if any(isinstance(d,bool) or not isinstance(d,int) or not 1<=d<=30 for d in days):
                raise ValueError('lunar_days must contain integers between 1 and 30')
            object.__setattr__(self,'lunar_days',days)
        types=frozenset(self.holiday_types) if self.holiday_types is not None else (_HOLIDAY_TYPES if self.legacy else frozenset({'lunar'}))
        if not types <= _HOLIDAY_TYPES:
            raise ValueError("holiday_types may only contain 'solar' and 'lunar'")
        object.__setattr__(self,'holiday_types',types)
        for field in ('calendar_color','holiday_color','lunar_day_color','ordinary_color'):
            value=getattr(self,field)
            if value is not None or field!='holiday_color':
                object.__setattr__(self,field,_validate_color(value,field))

    @property
    def selected_countries(self):
        return self.countries or (self.country,)

    @property
    def legacy(self):
        return self.content is None and not self.countries and not self.residence and self.country=='VN'

    @property
    def has_custom_filters(self):
        return (self.start_year is not None or self.end_year is not None or self.lunar_days is not None
                or self.holiday_types!=(_HOLIDAY_TYPES if self.legacy else frozenset({'lunar'})) or self.calendar_color!='#E53935'
                or self.holiday_color is not None or self.lunar_day_color!='#FB8C00'
                or self.ordinary_color!='#1E88E5')

    def to_dict(self):
        result = dict(country=self.country,countries=list(self.countries),tradition=self.tradition,
                    language=self.language,content=self.content,minimal=self.minimal,
                    start_year=self.start_year,end_year=self.end_year,
                    lunar_days='all' if self.lunar_days is None else sorted(self.lunar_days),
                    holiday_types=sorted(self.holiday_types),
                    colors=dict(calendar=self.calendar_color,holiday=self.holiday_color,
                                lunar_day=self.lunar_day_color,ordinary=self.ordinary_color))
        result.pop('country' if self.countries else 'countries')
        if self.residence is not None:
            result['residence'] = self.residence
        if self.feed_name is not None:
            result['feed_name'] = self.feed_name
        return result

    @classmethod
    def from_mapping(cls,data):
        if not isinstance(data,dict):
            raise ValueError('configuration root must be a JSON object')
        allowed={'feed_name','country','countries','residence','tradition','language','content','minimal','subdivision',
                 'start_year','end_year','lunar_days','holiday_types','colors'}
        if set(data)-allowed:
            raise ValueError('unknown configuration key(s): '+', '.join(sorted(set(data)-allowed)))
        kwargs={k:v for k,v in data.items() if k not in ('lunar_days','holiday_types','colors')}
        if 'country' in data and 'countries' in data and data['countries']:
            raise ValueError('Choose country or countries, not both')
        if 'countries' in data:
            if not isinstance(data['countries'],list) or not data['countries']:
                raise ValueError('countries must be a nonempty list')
            kwargs['countries']=tuple(data['countries'])
        if ('country' in data or 'countries' in data or data.get('residence')) and 'content' not in data and not data.get('minimal'):
            kwargs['content']='festivals'
        value=data.get('lunar_days','all')
        if value=='all':
            kwargs['lunar_days']=None
        elif isinstance(value,list):
            if any(isinstance(day,bool) or not isinstance(day,int) for day in value):
                raise ValueError('lunar_days must contain integers between 1 and 30')
            kwargs['lunar_days']=frozenset(value)
        else:
            raise ValueError("lunar_days must be 'all' or a list of day numbers")
        is_new = ('country' in data or 'countries' in data or data.get('residence') or data.get('content') is not None)
        types=data.get('holiday_types',['lunar'] if is_new and not data.get('minimal') else sorted(_HOLIDAY_TYPES))
        if not isinstance(types,list) or any(not isinstance(t,str) for t in types):
            raise ValueError('holiday_types must be a list of strings')
        kwargs['holiday_types']=frozenset(types)
        colors=data.get('colors',{})
        if not isinstance(colors,dict) or set(colors)-{'calendar','holiday','lunar_day','ordinary'}:
            raise ValueError('unknown color key(s) or invalid colors object')
        kwargs.update({k+'_color':v for k,v in colors.items()})
        return cls(**kwargs)


def load_calendar_options(filepath):
    with Path(filepath).open(encoding='utf-8-sig') as file:
        return CalendarOptions.from_mapping(json.load(file))


def parse_lunar_days(value):
    if value.lower()=='all': return None
    if value.lower()=='none': return frozenset()
    try: days=frozenset(int(d.strip()) for d in value.split(','))
    except ValueError as exc: raise ValueError('use all, none or comma-separated day numbers') from exc
    if not days or any(not 1<=d<=30 for d in days): raise ValueError('lunar days must be between 1 and 30')
    return days


def parse_holiday_types(value):
    if value.lower()=='all': return _HOLIDAY_TYPES
    if value.lower()=='none': return frozenset()
    result=frozenset(t.strip().lower() for t in value.split(','))
    if not result or not result<=_HOLIDAY_TYPES: raise ValueError('use all, none, solar, lunar or solar,lunar')
    return result
