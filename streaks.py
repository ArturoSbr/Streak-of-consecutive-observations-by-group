import numpy as np
import pandas as pd
def counter(id_array, period_array, return_grouped=False):
    '''
    The purpose of this function is to count the streaks of consecutive numbers for each group in a given dataset.
    That is, to find the longest streak of consecutive observations for each group in the data, like the longest
    streak of daily purchases per client.
    Returns a `pandas.DataFrame` object that can either show the current streak of each row by group or the longest
    streak of consecutive numbers achieved by each group.

    Parameters
    ----------
            id_array : array_like
                Input array or object that can be converted to an array where the group identifiers are stored.
                This input will be the `groupby` argument.
            period_array : array_like
                Input array or object that can be converted to an array where the numeric order of each row is stored.
                The consecutive numbers of this array will be counted as the streak.
            return_grouped : bool, default `False`
                If `True` it will return the longest consecutive streak achieved by each group.
                If `False` it will return a dataframe with the current consecutive streak of each row.
    Returns
    -------
            `pandas.DataFrame` object
    Notes
    -----
            The user has to map the time stamps to numeric values that express their order
    GitHub
    ------
            https://github.com/ArturoSbr
    '''
    df = pd.DataFrame({'group':id_array, 'period':period_array})
    df = df.sort_values(['group','period'], ascending=True).reset_index(drop=True)
    df['lag'] = df.groupby('group')['period'].shift(periods=1, axis=0, fill_value=0)
    df['d'] = df['period'] - df['lag']
    df['streak'] = 1
    for group in np.unique(id_array):
        start = df.index[df['group'].eq(group)][1]
        x = 1
        for i in range(0, df['group'].eq(group).sum() - 1):
            if df.loc[start + i, 'd'] == 1:
                x = x + 1
                df.loc[start + i, 'streak'] = x
            else:
                x = 1
                df.loc[start + i, 'streak'] = x
    if return_grouped:
        df = df.groupby('group').agg({'streak':'max'}).reset_index()
        return df
    else:
        return df[['group','period','streak']]
