import pandas as pd


def insert_date_between_week(week_data):
    # insert date between week
    week_data['date'] = week_data['date'].apply(
        lambda x: pd.to_datetime(x, format='%Y-%m-%d'))
    week_data['date'] = week_data['date'].apply(
        lambda x: x + pd.Timedelta(days=1))
    week_data['date'] = week_data['date'].apply(
        lambda x: x.strftime('%Y-%m-%d'))
    return week_data

def duplicate_each_row_for_seven_times(week_data):
    # duplicate each row for seven times
    week_data_origin = week_data.copy()
    # create a blank dataframe
    week_data_duplicate = pd.DataFrame(columns=week_data.columns)

    for i in range(7):
        week_data_origin['day'] = pd.Timedelta(days=i)
        # week_data_duplicate = week_data_duplicate.append(week_data_origin)
        week_data_duplicate = pd.concat(
            [week_data_duplicate, week_data_origin])
    # sort by week and day
    week_data_duplicate = week_data_duplicate.sort_values(
        by=['week', 'day'], ascending=True)

    return week_data_duplicate


def add_date_to_each_row(week_data):
    # add date to each row
    week_data['date'] = week_data['date'].apply(
        lambda x: pd.to_datetime(x, format='%Y-%m-%d'))
    week_data['date'] = week_data['date'] + week_data['day']
    week_data['date'] = week_data['date'].apply(
        lambda x: x.strftime('%Y-%m-%d'))
    return week_data


def convert_week_to_date_and_split_weekly_quantity(week_data):
    # expand week to date and split qty to qty_daily
    week_data['date'] = week_data['week'].apply(
        lambda x: pd.to_datetime(x, format='%V'))
    week_data['qty_daily'] = week_data['qty'].apply(
        lambda x: x / 7)
    return week_data


def convert_week_to_date(week_data):
    '''take un processed week data and convert it to date and qty_daily'''
    week_data = duplicate_each_row_for_seven_times(week_data)
    week_data = convert_week_to_date_and_split_weekly_quantity(week_data)
    week_data = add_date_to_each_row(week_data)
    return week_data