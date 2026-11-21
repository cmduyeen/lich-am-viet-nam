"""Stable feed names are independent of the rolling date range."""
import hashlib
import json
from .profiles import get_profile


def output_prefix(options):
    if options.feed_name is not None:
        return f"custom_{options.feed_name}"
    if options.legacy:
        prefix='viet_lunar' if options.language=='vi' else 'viet_lunar_en'
        if options.minimal:
            prefix+='_minimal'
        elif (options.lunar_days == frozenset({1, 15})
              and options.start_year is None and options.end_year is None
              and options.holiday_types == frozenset({'solar', 'lunar'})
              and options.calendar_color == '#E53935' and options.holiday_color is None
              and options.lunar_day_color == '#FB8C00' and options.ordinary_color == '#1E88E5'):
            return prefix + '_minimal'
    else:
        codes='-'.join(c.lower() for c in options.selected_countries)
        tradition=options.tradition or ('merged' if len(options.selected_countries)>1 else get_profile(options.selected_countries[0]).tradition)
        if options.residence:
            codes=options.residence.lower() + ('-' + codes if len(options.selected_countries)>1 else '')
        mode='minimal' if options.minimal else options.content
        prefix=f'lunar_{codes}_{tradition}_{options.language}_{mode}'
    if options.has_custom_filters:
        data=options.to_dict()
        if not data.get('countries'): data.pop('countries',None)
        digest=hashlib.sha256(json.dumps(data,sort_keys=True).encode()).hexdigest()[:8]
        prefix+=f'_custom_{digest}'
    return prefix
