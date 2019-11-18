import pandas as pd
import re
import calendar
import datetime as dt


def add_months(source_date, months) -> dt.date:
    month = source_date.month - 1 + months
    year = source_date.year + month // 12
    month = month % 12 + 1
    day = min(source_date.day, calendar.monthrange(year, month)[1])
    return dt.date(year, month, day)


def parse_date(date):
    def clean_date(date_string):
        if date_string == 'nan':
            return ''
        if date_string is '0' or date_string is '1':
            return ''
        if '(' in date_string:
            s = re.sub(r'\(.*\)', '', date_string)
            return ''.join(s.split())
        return ''.join(date_string.split())

    def try_parsing_date(text):
        if not text:
            return ''
        for fmt in ('%Y-%m-%d', '%d.%m.%Y', '%m.%Y', '%d.%m.%y', '%Y-%m-%d %H:%M:%S', '%Y-%m-%d%H:%M:%S', '%d/%m/%Y'):
            try:
                actual_date = dt.datetime.strptime(text, fmt)
                if actual_date and fmt != '%m.%Y':
                    return dt.datetime.strptime(text, fmt).date()
                else:
                    return add_months(actual_date, 1)
            except ValueError:
                pass
        raise ValueError(f'No valid date format found: {text}')

    date = clean_date(date)
    date = try_parsing_date(date)
    return date


def main():
    # read excel sheet
    df = pd.read_excel('data.xlsx')

    # drop rows without valid data
    df.dropna(subset=['Zařazen od'], inplace=True)  # rows with null values
    df.drop(df[df['ID3'] == 258].index, inplace=True)  # strange one, dead before admission
    df.drop(df[df['ID3'] == 563].index, inplace=True)  # strange one, the only string value in column 'TSS příjem'
    df.drop(df[df['mRS-out'] == 7].index, inplace=True)  # those are not relevant according to the assignment

    # censoring

    # drop columns
    df.drop(columns=['ID1', 'ID3'], inplace=True)  # drop ID columns
    df.drop(columns=['Obec', 'Okres'], inplace=True)  # drop location columns
    df.drop(columns=['datum kontroly', 'pobyt', 'pobyt 1'], inplace=True)  # drop additional information columns
    df.drop(columns=['Diag. hypertenze', 'Diag. diabetes', 'Diag. hyperlip.', 'Akt. kuřák', 'Bývalý kuřák',
                     'Ischem. příhoda před > 3M', 'Ischem. příhoda před < 3M', 'Předchozí TIA', 'Fibrilace síní',
                     'Městnavé srdeční selhání', 'Cévní onem.'],
            inplace=True)  # drop columns with risk factors (irrelevant for the task)
    df.drop(columns=['událost', 'ADL 1 rok', 'BI 1 rok'], inplace=True)  # no information about meaning of the column
    df.drop(columns=['Datum zahájení trombolýzy', 'Datum zahájení trombektomie', 'Lokalizace tr.', 'zpracování 0/1/2 '],
            inplace=True)  # irrelevant for the task
    df.drop(columns=['Unnamed: 25'], inplace=True)  # column without values should not be there
    df.drop(columns=['Zařazen od', 'Datum 1. hosp.'], inplace=True)  # observation start is taken from another column
    df.drop(columns=['mRS-out-3M', 'MRS Před', 'MRS', 'MRS 3M'], inplace=True)  # irrelevant for the task

    # modify columns
    df['TSS příjem'] = df['TSS příjem'].astype(int)  # make this column's values numerical
    df['TSS prop.'] = df['TSS prop.'].fillna(0)  # replace NaN with 0
    df['TSS prop.'] = df['TSS prop.'].astype(int)  # make this column's values numerical

    # clean column data
    df['Etiolog. klas.'] = df['Etiolog. klas.'].apply(lambda x: int(x[4]))  # replace diagnosis with it's numerical code
    df['datum +'] = df['datum +'].apply(lambda x: parse_date(str(x)))  # transform end_date to correct format
    df['Datum vzniku příznaku'] = df['Datum vzniku příznaku'].apply(
        lambda x: dt.datetime.strptime(x, '%d.%m.%Y %H:%M:%S').date())  # transform start
    df['mRS-out'] = df['mRS-out'].apply(lambda x: int(x))
    df['mRS - 1Y'] = df['mRS - 1Y'].apply(lambda x: int(x))
    df['Věk'] = df['Věk'].apply(lambda x: int(x))
    df['Pohlaví'] = df['Pohlaví'].apply(lambda x: str.lower(x))

    # rename columns
    df.rename(columns={'Datum vzniku příznaku': 'start_date',
                       'Etiolog. klas.': 'diagnosis',
                       'TSS příjem': 'tss_in',
                       'TSS prop.': 'tss_out',
                       'datum +': 'end_date',
                       'mRS - 1Y': 'mrs_1y',
                       'mRS-out': 'mrs_out',
                       'Pohlaví': 'sex',
                       'Věk': 'age'},
              inplace=True)

    # save to csv
    df.to_csv('data.csv', index=None)


if __name__ == '__main__':
    main()
