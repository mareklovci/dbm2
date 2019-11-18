from textwrap import wrap

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from lifelines import KaplanMeierFitter
from lifelines.plotting import plot_lifetimes
from lifelines.utils import datetimes_to_durations

from utils import start_end_for_diagnosis, image_sequence

diagnosis_list = {
    0: 'I63.0: Cerebral infarct, large vessel disease with significant carotid stenosis',
    3: 'I63.3: Cerebral infarct, other large vessel disease',
    4: 'I63.4: Cerebral infarct, cardic emboli',
    5: 'I63.5: Cerebral infarct, small vessel / lacunar',
    8: 'I63.8: Cerebral infarct, other / unusual cause',
    9: 'I63.9: Cerebral infarct, multiple / unknown cause'
}


GEN = image_sequence()


def kaplan_meier_analysis(df, rows=2, columns=3):
    """
    Kaplan-Meier estimates for individual diagnoses

    :param df: Pandas dataframe with data
    :param rows: number of rows for subplots
    :param columns: number of columns for subplots
    :return: Plots the data
    """
    fig, axes = plt.subplots(rows, columns, figsize=[10, 6])

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
        ax: plt.Axes = axes[pos % rows, pos % columns]

        # plot Kaplan-Meier
        kmf.plot(ax=ax)

        # format plot
        ax.set_ylim(0.45, 1)
        ax.set_title('\n'.join(wrap(diagnosis_list[diagnosis], 30)))
        ax.get_legend().remove()
        ax.margins(y=50)

    # show plot
    fig.show()
    fig.savefig(f'paper/img/image_{next(GEN)}.pdf', format='pdf')


def plot_lifetimes_for_diagnosis(df, diagnosis, current_time=50, subset_size=80):
    df = df.loc[df['diagnosis'] == diagnosis]

    # create figure and axes
    fig, ax = plt.subplots()

    # specify type for PyCharm help
    fig: plt.Figure = fig
    ax: plt.Axes = ax

    if df.shape[0] >= subset_size:
        df = df.sample(n=subset_size, random_state=1)

    start_times, end_times = df['start_date'], df['end_date']

    actual_lifetimes, death_observed = datetimes_to_durations(start_times, end_times, freq='M')

    plot_lifetimes(durations=actual_lifetimes, event_observed=death_observed, ax=ax)

    ax.set_title(diagnosis_list[diagnosis])
    ax.set_xlabel('Čas od začátku sledování po vznik události v měsících')
    ax.set_ylabel('Sledovaná osoba')

    # show and save plot
    fig.show()
    fig.savefig(f'paper/img/image_{next(GEN)}.pdf', format='pdf')


def plot_hist(df: pd.DataFrame, column, x_label, y_label, title='', x_lim=0, x_ticks: np.ndarray = None):
    # create figure and axes
    fig, ax = plt.subplots()

    # specify type for PyCharm help
    fig: plt.Figure = fig
    ax: plt.Axes = ax

    # plot histogram
    labels, counts = np.unique(df[column], return_counts=True)
    plt.bar(labels, counts, align='center')
    plt.gca().set_xticks(labels)

    # set properties
    if x_ticks is not None:
        ax.set_xticks(x_ticks)

    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.set_title(title)
    ax.set_xlim(x_lim - 0.5)

    # show and save plot
    fig.show()
    fig.savefig(f'paper/img/image_{next(GEN)}.pdf', format='pdf')


def plot_comparison(df, x, x_label, y_label, title=''):
    fig, ax = plt.subplots()
    data = {'x': x, 'y': df['mrs_1y'] == 6}
    sns.regplot(x='x', y='y', data=data, logistic=True, n_boot=100, ax=ax)

    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.set_title(title)

    # show and save plot
    fig.show()
    fig.savefig(f'paper/img/image_{next(GEN)}.pdf', format='pdf')


def main():
    # read cleaned data
    df = pd.read_csv('data.csv')

    plot_hist(df, 'age', 'Věk', 'Počet pacientů', x_lim=25, x_ticks=np.arange(25, 95, 5))

    plot_hist(df, 'mrs_1y', 'mRS - 1Y', 'Počet pacientů')

    plot_hist(df, 'diagnosis', 'Diagnóza', 'Počet pacientů')

    # Age to mRS comparison
    plot_comparison(df, df['age'], 'Věk', 'mRS - 1Y')

    # TSS to mRS comparison
    plot_comparison(df, df['tss_in'], 'Vstupní TSS', 'mRS - 1Y')

    # TSS difference to mRS comparison
    plot_comparison(df, df['tss_in'] - df['tss_out'], 'Rozdíl vstupního a výstupního TSS', 'mRS - 1Y')

    # Sex to mRS comparison
    fig, ax = plt.subplots()

    fig: plt.Figure = fig
    ax: plt.Axes = ax

    data = {'x': np.asarray([0 if i is 'f' else 1 for i in df['sex']]),
            'y': df['mrs_1y'] == 6}
    sns.regplot(x='x', y='y', data=data, logistic=True, n_boot=100, ax=ax)

    ax.set_xticks(np.arange(0, 1 + 0.1, 1))
    ax.set_xticklabels(['Žena', 'Muž'])

    ax.set_ylabel('mRS - 1Y')
    ax.set_xlabel('Pohlaví')

    fig.show()
    fig.savefig(f'paper/img/image_{next(GEN)}.pdf', format='pdf')

    # plot lifetimes graph
    plot_lifetimes_for_diagnosis(df, diagnosis=3)

    # plot kaplan-meier curves
    kaplan_meier_analysis(df)


if __name__ == '__main__':
    main()
