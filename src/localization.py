"""Strict, explicit locale lookup; errors expose incomplete translations."""
import json
from pathlib import Path
from .profiles import PROFILES, RESIDENCES, residence_languages, RULES, SOLAR_RULES, SOLAR_TERMS

LOCALES = json.loads(Path(__file__).with_name('locales.json').read_text(encoding='utf-8'))


def title(code, language, identity):
    locale=LOCALES[language]
    overrides=locale.get('overrides',{}).get(code,{})
    return overrides[identity] if identity in overrides else locale['festivals'][identity]


def lunar_label(lunar, language):
    locale=LOCALES[language]
    return locale['lunar_date'].format(day=lunar.day,month=lunar.month,year=lunar.year,
                                      leap=locale['leap'] if lunar.leap else '')


def validate_translations():
    required={'calendar','daily','observances','minimal','lunar_date','leap','countries','notice','moon_note','country_names','festivals'}
    for profile in PROFILES.values():
        ids={rule[2] for rule in RULES[profile.code]} | {'new_year_eve','new_moon','full_moon'}
        ids.update(SOLAR_TERMS.get(profile.code,{}).values())
        ids.update(rule[2] for rule in SOLAR_RULES.get(profile.code,()))
        for language in profile.languages:
            locale=LOCALES[language]
            if required-set(locale): raise ValueError(f'Incomplete metadata: {language}')
            for identity in ids:
                if not title(profile.code,language,identity): raise ValueError(f'Missing translation: {language}/{identity}')
            if not locale['country_names'].get(profile.code): raise ValueError('Missing localized country name')

    for host in RESIDENCES.values():
        for _, code in host.traditions:
            profile = PROFILES[code]
            identities = {r[2] for r in RULES[code]} | {'new_year_eve','new_moon','full_moon'}
            identities.update(SOLAR_TERMS.get(code, {}).values())
            identities.update(r[2] for r in SOLAR_RULES.get(code, ()))
            for language in residence_languages(host.code, profile):
                locale = LOCALES[language]
                if not locale.get('residence_note') or not locale['country_names'].get(host.code):
                    raise ValueError(f'Missing residence translation: {host.code}/{language}')
                for identity in identities:
                    if not title(code, language, identity):
                        raise ValueError(f'Missing translation: {language}/{identity}')
