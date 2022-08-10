from operator import concat, index
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


def duplicate_each_row_for_seven_times(week_data, order_by=['week', 'day'], daily_ratio=[17.57, 19.52, 20.04, 19.23, 18.97, 3.01, 1.66]):
    # duplicate each row for seven times
    week_data_origin = week_data.copy()
    # create a blank dataframe
    week_data_duplicate = pd.DataFrame(columns=week_data.columns)

    for i in range(7):
        week_data_origin['day'] = pd.Timedelta(days=i)
        week_data_origin['daily_ratio'] = daily_ratio[i] / 100
        # week_data_duplicate = week_data_duplicate.append(week_data_origin)
        week_data_duplicate = pd.concat(
            [week_data_duplicate, week_data_origin])
    # sort by week and day
    week_data_duplicate = week_data_duplicate.sort_values(
        by=order_by, ascending=True)

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
    # expand week to date and apply daily_ratio to qty_daily
    week_data['date'] = week_data['week'].apply(
        lambda x: pd.to_datetime(x, format='%V'))
    week_data['qty_daily'] = week_data['qty'] * week_data['daily_ratio']
    return week_data


def flow_convert_week_to_date(week_data):
    '''take un processed week data and convert it to date and qty_daily'''
    week_data = duplicate_each_row_for_seven_times(week_data)
    week_data = convert_week_to_date_and_split_weekly_quantity(week_data)
    week_data = add_date_to_each_row(week_data)
    return week_data


def convert_week_to_date_and_split_weekly_movement(week_data):
    # expand week to date and apply daily_ratio to net_movement
    week_data['date'] = week_data['week'].apply(
        lambda x: pd.to_datetime(x, format='%V'))
    week_data['daily_net_qty'] = week_data['net_movement'] * \
        week_data['daily_ratio']
    return week_data


def inventory_convert_week_to_day(week_data):
    '''take un processed week data and convert it to date and daily_net_qty'''
    week_data = duplicate_each_row_for_seven_times(
        week_data, order_by=['depot', 'week', 'day'])
    week_data = convert_week_to_date_and_split_weekly_movement(week_data)
    week_data = add_date_to_each_row(week_data)
    week_data = add_end_inventory_column(week_data)
    week_data = add_start_inventory_column(week_data)

    return week_data


def get_start_inventory(inventory_data):
    '''get start inventory of each depot'''
    start_inventory = inventory_data.groupby(['depot'])['starting inv'].first()
    return start_inventory


def get_date_by_depot(inventory_data, depot):
    '''get date by depot'''
    date = inventory_data[inventory_data['depot'] == depot]['date']
    return date


def get_daily_movenment_by_depot(inventory_data, depot):
    '''get daily movement by depot'''
    daily_movement = inventory_data[inventory_data['depot']
                                    == depot]['daily_net_qty']
    return daily_movement


def add_end_inventory_column(inventory_data):
    '''create list of end inventory by depot'''
    # get start inventory of each depot
    start_inventory = get_start_inventory(inventory_data)

    # get list of all depots
    depot_list = inventory_data['depot'].unique()
    # get list of dates by depot and get list of daily movement by depot
    date_list = []
    daily_movement_list = []
    for depot in depot_list:
        date_list.append(get_date_by_depot(inventory_data, depot))
        daily_movement_list.append(get_daily_movenment_by_depot(
            inventory_data, depot))

    # create list of end inventory by depot
    end_inventory_list = []
    for index, depot in enumerate(depot_list):
        current_inventory = start_inventory[depot]
        for i in daily_movement_list[index]:
            current_inventory += i
            end_inventory_list.append(current_inventory)

    # convert end inventory to dataframe
    end_inventory_list = pd.DataFrame(
        end_inventory_list, columns=['end inventory'])
    # reset index
    end_inventory_list = end_inventory_list.reset_index(drop=True)
    inventory_data = inventory_data.reset_index(drop=True)

    inventory_data = pd.concat([inventory_data, end_inventory_list], axis=1)
    return inventory_data


def add_start_inventory_column(inventory_data):
    '''add start inventory column to inventory_data'''

    # add start inventory column to inventory_data
    inventory_data['start inventory'] = inventory_data['end inventory'] - \
        inventory_data['daily_net_qty']
    return inventory_data


if __name__ == '__main__':
    print('This is a module. Do not run it directly.')
