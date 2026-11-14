"""Only implemented lunar profiles appear here; roadmapped countries stay separate."""
from dataclasses import dataclass
import json
from pathlib import Path

FESTIVAL_SOURCES = json.loads(Path(__file__).with_name("festival_sources.json").read_text(encoding="utf-8"))


@dataclass(frozen=True)
class Profile:
    code: str
    name: str
    timezone: str
    engine: str
    languages: tuple[str, ...]
    native: str
    tradition: str
    first_year: int
    last_year: int
    sources: tuple[str, ...]
    leap_festivals: bool = False


HKO = 'https://www.hko.gov.hk/en/gts/time/conversion.htm'
KASI = 'https://astro.kasi.re.kr/'
VN = 'https://tienphong.vn/nam-2007-viet-nam-an-tet-som-hon-trung-quoc-mot-ngay-post52582.tpo'
PROFILES = {
    'VN': Profile('VN', 'Vietnam', 'Asia/Ho_Chi_Minh', 'vietnamese', ('vi','en'), 'vi', 'vietnamese', 1901, 2099, (VN,)),
    'CN': Profile('CN', 'China', 'Asia/Shanghai', 'chinese', ('zh-Hans','en'), 'zh-Hans', 'chinese', 1901, 2099, (HKO,)),
    'TW': Profile('TW', 'Taiwan', 'Asia/Taipei', 'chinese', ('zh-Hant','en'), 'zh-Hant', 'chinese', 1901, 2099, (HKO,'https://www.dgpa.gov.tw/')),
    'HK': Profile('HK', 'Hong Kong', 'Asia/Hong_Kong', 'chinese', ('zh-Hant','en'), 'zh-Hant', 'chinese', 1901, 2099, (HKO,'https://www.gov.hk/en/about/abouthk/holiday/')),
    'MO': Profile('MO', 'Macao', 'Asia/Macau', 'chinese', ('zh-Hant','en'), 'zh-Hant', 'chinese', 1901, 2099, (HKO,'https://www.gov.mo/en/public-holidays/')),
    'KR': Profile('KR', 'South Korea', 'Asia/Seoul', 'korean', ('ko','en'), 'ko', 'korean', 1901, 2050, (KASI,)),
    'SG': Profile('SG', 'Singapore', 'Asia/Singapore', 'chinese', ('en','zh-Hans'), 'en', 'chinese', 1901, 2099, (HKO,'https://www.mom.gov.sg/employment-practices/public-holidays')),
    'MY': Profile('MY', 'Malaysia', 'Asia/Kuala_Lumpur', 'chinese', ('ms','en','zh-Hans'), 'ms', 'chinese', 1901, 2099, (HKO,'https://www.kabinet.gov.my/')),
}
ROADMAP = {'TH':'Thai Buddhist', 'KH':'Khmer Buddhist', 'LA':'Lao Buddhist', 'MM':'Myanmar Buddhist', 'LK':'Sri Lankan Buddhist'}


def get_profile(code):
    if not isinstance(code,str) or code.upper() not in PROFILES:
        raise ValueError(f'Unsupported lunar profile: {code}. Use --list-countries.')
    return PROFILES[code.upper()]


def resolve_language(profile, language, residence=None):
    language = ('en' if residence else profile.native) if language in (None,'native') else language
    supported = residence_languages(residence, profile) if residence else profile.languages
    if language not in supported:
        raise ValueError(f'{residence or profile.code} / {profile.tradition} supports languages: {", ".join(supported)}')
    return language

"""Festival identities are independent of translated names and public holidays."""
# (month, day, identity). Leap months are excluded unless a profile says otherwise.
COMMON = ((1,1,'lunar_new_year'), (1,15,'lantern'), (5,5,'dragon_boat'), (8,15,'mid_autumn'))
RULES = {
    'VN': ((1,1,'lunar_new_year'), (1,2,'tet_day_2'), (1,3,'tet_day_3'), (1,7,'khai_ha'), (1,10,'wealth'), (3,3,'han_thuc'), (1,15,'lantern'), (3,10,'hung_kings'), (4,15,'buddha_vn'), (5,5,'dragon_boat'), (7,15,'vu_lan'), (7,15,'ghost'), (8,15,'mid_autumn'), (12,23,'kitchen_gods')),
    'CN': COMMON + ((1,2,'cny_day_2'),(1,3,'cny_day_3'),(2,2,'dragon_heads'), (7,7,'qixi'), (7,15,'ghost'), (9,9,'double_ninth'), (12,8,'laba'), (12,23,'xiaonian_north'), (12,24,'xiaonian_south')),
    'TW': COMMON + ((1,2,'cny_day_2'), (3,23,'mazu'), (7,7,'qixi'), (7,15,'ghost'), (9,9,'double_ninth'), (12,24,'kitchen_gods')),
    'HK': COMMON + ((1,2,'cny_day_2'), (1,3,'cny_day_3'), (3,23,'mazu'), (4,8,'tam_kung'), (4,8,'buddha_east'), (7,15,'ghost'), (9,9,'double_ninth')),
    'MO': COMMON + ((1,2,'cny_day_2'), (3,23,'mazu'), (5,18,'na_tcha'), (4,8,'buddha_east'), (7,15,'ghost'), (9,9,'double_ninth')),
    'KR': ((1,1,'lunar_new_year'), (1,2,'seollal_day_2'), (8,14,'chuseok_eve'), (8,16,'chuseok_day_2'), (1,15,'daeboreum'), (4,8,'buddha_east'), (5,5,'dano'), (8,15,'chuseok')),
    'SG': COMMON + ((1,2,'cny_day_2'), (7,15,'ghost'),),
    'MY': COMMON + ((1,2,'cny_day_2'), (7,15,'ghost'),),
}
# Solar-term festivals must not be mislabelled as fixed lunar-day festivals.
SOLAR_TERMS = {'CN': {'清明':'qingming'}, 'TW': {'清明':'qingming'}, 'HK': {'清明':'qingming'}, 'MO': {'清明':'qingming'}}
SOLAR_RULES = {'VN': ((1,1,'solar_new_year'),(4,30,'reunification'),(5,1,'labour'),(9,2,'national_vn'))}


@dataclass(frozen=True)
class Residence:
    """Where a community lives; never an astronomical calendar engine."""
    code: str
    name: str
    traditions: tuple[tuple[str, str], ...]
    sources: tuple[str, ...] = ()


RESIDENCES = {
    'US': Residence('US', 'United States',
                    (('vietnamese', 'VN'), ('chinese', 'CN'), ('korean', 'KR')),
                    ('https://www.census.gov/library/stories/2023/09/2020-census-dhc-a-asian-population.html',)),
}
# Later markets are intentionally not enabled as working lunar profiles.
GLOBAL_ROADMAP = {
    'NG': 'Nigeria: independently verified Islamic calendar and local announcements required',
    'EG': 'Egypt: independently verified Islamic calendar and local announcements required',
    'BR': 'Brazil: Portuguese and national-holiday scope required',
    'MX': 'Mexico: Spanish and national-holiday scope required',
}


def get_residence(code):
    if not isinstance(code, str) or code.upper() not in RESIDENCES:
        raise ValueError(f'Unsupported residence: {code}. Use --list-countries.')
    return RESIDENCES[code.upper()]


def residence_languages(residence, profile):
    host = get_residence(residence)
    if profile.code not in dict(host.traditions).values():
        raise ValueError(f'{host.code} does not support the {profile.code} profile')
    if profile.tradition == 'chinese':
        return ('en', 'zh-Hans', 'zh-Hant')
    return ('en',) + tuple(lang for lang in profile.languages if lang != 'en')
