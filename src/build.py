"""Build a validated set of files using one generated calendar."""
from pathlib import Path
from .ics import write_calendar, create_zip
from .ics_generator import LunarCalendarGenerator
from .naming import output_prefix


def build_files(options,start,end,staging,output,split=False,year_only=False,latest_only=False):
    staging,output=Path(staging),Path(output)
    generator=LunarCalendarGenerator()
    prefix=output_prefix(options)
    latest=f'{prefix}_latest.ics'
    # Reuse the previous rolling calendar for revisions even for --split.
    previous=output/latest
    calendar=generator.generate_range(start,end,options)
    from .ics import reconcile
    calendar=reconcile(calendar,previous)
    files=[]
    if split or year_only:
        yearly=[]
        for year in range(start,end+1):
            target=staging/f'{prefix}_{year}.ics'
            write_calendar(generator.split_year(calendar,year),target,reconciled=True)
            yearly.append(target)
        files.extend(yearly)
        if split and len(yearly)>1:
            archive=staging/f'{prefix}_yearly_{start}_{end}.zip'
            create_zip(yearly,archive)
            files.append(archive)
    if not year_only:
        suffix=str(start) if start==end else f'{start}_{end}'
        latest_file=staging/latest
        if latest_only:
            write_calendar(calendar,latest_file,reconciled=True)
            files.append(latest_file)
        else:
            ranged=staging/f'{prefix}_{suffix}.ics'
            write_calendar(calendar,ranged,reconciled=True)
            latest_file.write_bytes(ranged.read_bytes())
            files.extend([ranged,latest_file])
    return calendar,files
