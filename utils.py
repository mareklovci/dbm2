import calendar
import datetime as dt
import re
from typing import List


def add_months(source_date, months) -> dt.date:
    month = source_date.month - 1 + months
    year = source_date.year + month // 12
    month = month % 12 + 1
    day = min(source_date.day, calendar.monthrange(year, month)[1])
    return dt.date(year, month, day)


def try_parsing_date(text):
    if not text:
        return ''
    for fmt in ('%Y-%m-%d', '%d.%m.%Y', '%m.%Y', '%d.%m.%y', '%Y-%m-%d %H:%M:%S', '%Y-%m-%d%H:%M:%S', '%d/%m/%Y'):
        try:
            date = dt.datetime.strptime(text, fmt)
            if date and fmt != '%m.%Y':
                return dt.datetime.strptime(text, fmt).date()
            else:
                return add_months(date, 1)
        except ValueError:
            pass
    raise ValueError(f'no valid date format found: {text}')


def clean_date_string(text):
    if text == 'nan':
        return ''
    if text is '0' or text is '1':
        return ''
    if '(' in text:
        s = re.sub(r'\(.*\)', '', text)
        return ''.join(s.split())
    return ''.join(text.split())


def clean_dates(list_of_strings) -> List:
    dates = list()
    for item in list_of_strings:
        date = clean_date_string(item)
        dates.append(date)
    return dates


def _get_dates(data_frame):
    start_times = [dt.datetime.strptime(date, '%d.%m.%Y').date() for date in data_frame['Zařazen od']]

    dates = clean_dates(data_frame['datum +'].astype(str).values.tolist())
    end_times = [try_parsing_date(date) for date in dates]

    return start_times, end_times


def start_end_for_diagnosis(data_frame, diagnosis: str = None):
    """

    Return Tuple (start_times, end_times) where:
        start_times is a vector or list of datetime objects or datetime strings\n
        end_times is a vector or list of (possibly missing) datetime objects or datetime strings

    :param data_frame:
    :param diagnosis:
    :return: (start_times, end_times)
    """
    if not diagnosis:
        return _get_dates(data_frame)
    else:
        df = data_frame.loc[data_frame['Etiolog. klas.'] == diagnosis]
        return _get_dates(df)
