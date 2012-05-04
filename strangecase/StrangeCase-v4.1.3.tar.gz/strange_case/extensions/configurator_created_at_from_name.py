import re
import datetime

from strange_case.configurators import provides


CREATED_AT_RE = re.compile(r'''
    (?P<created_at>
        (?P<year>[1-9]\d{3})
        (?:
            [-_](?P<month>\d{2})
            (?:
                [-_](?P<day>\d{2})
            )?
        )?
        [-_]
    )
    (?P<name>.*)''', re.VERBOSE)

STRIP_CREATED_AT_RE = re.compile(r'''
    (?P<created_at>
        (?P<year>[1-9]\d{3})
        (?:
            [-_](?P<month>\d{2})
            (?:
                [-_](?P<day>\d{2})
            )?
        )?
        [-_]
    )
    ''', re.VERBOSE)


def strip_created_at_from(created_at, name):
    match = STRIP_CREATED_AT_RE.match(name)
    if match:
        return name[len(match.group(0)):]
    return name


@provides('created_at')
def created_at_from_name(source_file, config):
    """
    Matches a date in the name or target_name.  Makes it easy to sort a blog
    and you don't have to add `date: ...` using YAML, plus you get a
    python date object.
    """
    matches = CREATED_AT_RE.match(config['name'])
    if not matches:
        matches = CREATED_AT_RE.match(config['target_name'])

    if matches:
        created_at = matches.group('created_at')
        year = int(matches.group('year'))
        if matches.group('month') is not None:
            month = int(matches.group('month'))
        else:
            month = 1

        if matches.group('day') is not None:
            day = int(matches.group('day'))
        else:
            day = 1

        date = datetime.date(
            year=year,
            month=month,
            day=day,
            )
        config['created_at'] = date

        if config['strip_metadata_from_name']:
            config['name'] = strip_created_at_from(created_at, config['name'])

        if config['strip_metadata_from_target_name']:
            config['target_name'] = strip_created_at_from(created_at, config['target_name'])
    return config

created_at_from_name.defaults = {
    'strip_metadata_from_name': True,
    'strip_metadata_from_target_name': False,
}
