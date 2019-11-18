def start_end_for_diagnosis(df, diagnosis=None):
    """

    Return Tuple (start_times, end_times) where:
        start_times is a vector or list of datetime objects or datetime strings\n
        end_times is a vector or list of (possibly missing) datetime objects or datetime strings

    :param df: Pandas dataframe
    :param diagnosis:
    :return: (start_times, end_times)
    """
    if not diagnosis:
        return df['start_date'], df['end_date']
    else:
        df = df.loc[df['diagnosis'] == diagnosis]
        return df['start_date'], df['end_date']


def image_sequence():
    num = 0
    while True:
        yield num
        num += 1


if __name__ == '__main__':
    pass
