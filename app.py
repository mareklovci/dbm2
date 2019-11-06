from textwrap import wrap

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from lifelines import KaplanMeierFitter
from lifelines.utils import datetimes_to_durations

from utils import start_end_for_diagnosis

cols = [
    'Pohlaví', 'Věk', 'Zařazen od', 'Datum vzniku příznaku', 'Datum 1. hosp.', 'Datum zahájení trombolýzy',
    'Datum zahájení trombektomie', 'Lokalizace tr.', 'Etiolog. klas.', 'TSS příjem', 'TSS prop.', 'MRS Před', 'MRS',
    'MRS 3M', 'mRS-out-3M', 'mRS - 1Y', 'zpracování 0/1/2 ', 'mRS-out', 'BI 1 rok', 'ADL 1 rok', 'datum +',
    'Unnamed: 25', 'událost', 'Diag. hypertenze', 'Diag. diabetes', 'Diag. hyperlip.', 'Akt. kuřák', 'Bývalý kuřák',
    'Ischem. příhoda před > 3M', 'Ischem. příhoda před < 3M', 'Předchozí TIA', 'Fibrilace síní',
    'Městnavé srdeční selhání', 'Cévní onem.'
]

diagnosis_list = [
    'I63.0: Cerebral infarct, large vessel disease with significant carotid stenosis',
    'I63.3: Cerebral infarct, other large vessel disease',
    'I63.4: Cerebral infarct, cardic emboli',
    'I63.5: Cerebral infarct, small vessel / lacunar',
    'I63.8: Cerebral infarct, other / unusual cause',
    'I63.9: Cerebral infarct, multiple / unknown cause'
]


def kaplan_meier_analysis(df, rows=2, columns=3):
    """
    Kaplan-Meier estimates for individual diagnoses

    :param df: Pandas dataframe with data
    :param rows: number of rows for subplots
    :param columns: number of columns for subplots
    :return: Plots the data
    """
    fig, axes = plt.subplots(columns, rows, figsize=[6, 10])

    for pos, diagnosis in enumerate(diagnosis_list):
        timeline = np.linspace(0, 21)

        # initialize start and end times
        start_times, end_times = start_end_for_diagnosis(df, diagnosis)

        # get data in the right format - t is time_span, e is event (1 is death)
        t, e = datetimes_to_durations(start_times, end_times, freq='M')  # M - months, D - days

        # initialize Kaplan-Meier fitters
        kmf = KaplanMeierFitter()

        # fit the data
        kmf.fit(t, event_observed=e, timeline=timeline)

        # get the plot position
        ax: plt.Axes = axes[pos % columns, pos % rows]

        # plot Kaplan-Meier
        kmf.plot(ax=ax)

        # format plot
        ax.set_ylim(0.45, 1)
        ax.set_title('\n'.join(wrap(diagnosis, 30)))
        ax.get_legend().remove()
        ax.margins(y=50)

    # show plot
    fig.show()


def plot_logistic_regression(data_x, data_y):
    data = {'x': data_x, 'y': data_y}
    sns.regplot(x='x', y='y', data=data, logistic=True, n_boot=100)
    plt.show()


def main():
    # read excel sheet
    df = pd.read_excel('data.xlsx')

    # drop rows without valid data
    df.dropna(subset=['Zařazen od'], inplace=True)  # rows with null values
    df.drop(df[df['ID3'] == 258].index, inplace=True)  # strange one, dead before admission
    df.drop(df[df['ID3'] == 563].index, inplace=True)  # strange one, the only string value in column 'TSS příjem'
    df.drop(df[df['mRS-out'] == 7].index, inplace=True)  # those are not relevant according to the assignment

    # drop columns
    df.drop(columns=['ID1', 'ID3'], inplace=True)  # drop ID columns
    df.drop(columns=['Obec', 'Okres'], inplace=True)  # drop location columns
    df.drop(columns=['datum kontroly', 'pobyt', 'pobyt 1'], inplace=True)  # drop additional information columns

    # modify columns
    df['TSS příjem'] = df['TSS příjem'].astype(int)  # make this column's values numerical
    df['TSS prop.'] = df['TSS prop.'].fillna(0)  # replace NaN with 0
    df['TSS prop.'] = df['TSS prop.'].astype(int)  # make this column's values numerical

    # Age to mRS comparison
    plot_logistic_regression(df['Věk'], df['mRS-out'])

    # TSS to mRS comparison
    plot_logistic_regression(df['TSS příjem'], df['mRS-out'])

    # TSS difference to mRS comparison
    difference = abs(df['TSS příjem'] - df['TSS prop.'])
    plot_logistic_regression(difference, df['mRS-out'])

    # Sex to mRS comparison
    sex = [0 if i is 'F' else 1 for i in df['Pohlaví']]
    plot_logistic_regression(np.asarray(sex), df['mRS-out'])

    # plot kaplan-meier curves
    kaplan_meier_analysis(df)


if __name__ == '__main__':
    main()
