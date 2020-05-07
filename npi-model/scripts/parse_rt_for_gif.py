import numpy as np
import pandas as pd
import datetime as dt


def get_geo_startdate_data(geo_file, startdate_file):
    geos = pd.read_csv(geo_file)
    start_dates = pd.read_csv(startdate_file)

    fips_list = list(geos.values[0, 1:])
    start_dates = list(start_dates.values[0, 1:])

    return fips_list, start_dates


def parse_Rt_for_states(max_date_='05/07/20'):
    simulation_file_states = r'results\US_state_summary.csv'
    geo_file_states = r'results\US_state_geocode.csv'
    startdate_file_states = r'results\US_state_start_dates.csv'
    timeseries_file = r'data\us_data\infections_timeseries_w_states.csv'

    fips_list, start_dates = get_geo_startdate_data(geo_file_states, startdate_file_states)

    start_dates = [dt.datetime.strptime(x, '%m/%d/%y') for x in start_dates]

    min_date = min(start_dates)
    max_date = dt.datetime.strptime(max_date_, '%m/%d/%y')
    header = pd.date_range(start=min_date, end=max_date)
    header = [dt.datetime.strftime(x, '%m/%d/%y') for x in header]

    # model output indices start at 1
    county_numbers = np.arange(1, len(fips_list) + 1)

    simulation_data = pd.read_csv(simulation_file_states, delimiter=',', index_col=0)

    timeseries_data = pd.read_csv(timeseries_file, delimiter=',')
    timeseries_data = timeseries_data[timeseries_data['FIPS'] % 1000 == 0]
    timeseries_data = timeseries_data.reset_index()

    plotting_data = pd.DataFrame(columns=header)
    plotting_data.insert(loc=0, column='FIPS', value=timeseries_data['FIPS'].values)
    short_keys = pd.Series(['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'DC',
                            'FL', 'GA', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY',
                            'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT',
                            'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH',
                            'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT',
                            'VT', 'VA', 'WA', 'WV', 'WI', 'WY', 'PR'])

    plotting_data.insert(loc=1, column='Combined_Key', value=short_keys)

    for county_number, state, start_date in zip(county_numbers, fips_list, start_dates):
        time_data = list(pd.date_range(start=start_date, end=max_date_))
        time_data = [dt.datetime.strftime(x, '%m/%d/%y') for x in time_data]
        num_days = len(time_data)
        start = 'Rt[1,' + str(county_number) + ']'
        end = 'Rt[' + str(num_days) + ',' + str(county_number) + ']'
        Rt_data = simulation_data.loc[start:end]

        data = Rt_data['mean'][:num_days].values
        plotting_data.loc[plotting_data.index[plotting_data['FIPS'] == state], time_data] = data

    plotting_data.to_csv(r'data\us_data\Rt_data_states.csv', na_rep='NA', index=False)


def parse_Rt_for_counties(max_date_='05/07/20'):
    simulation_file_counties = r'results\US_county_summary.csv'
    geo_file_counties = r'results\US_county_geocode.csv'
    startdate_file_counties = r'results\US_county_start_dates.csv'
    timeseries_file = r'data\us_data\infections_timeseries_w_states.csv'

    fips_list, start_dates = get_geo_startdate_data(geo_file_counties, startdate_file_counties)

    start_dates = [dt.datetime.strptime(x, '%m/%d/%y') for x in start_dates]

    min_date = min(start_dates)
    max_date = dt.datetime.strptime(max_date_, '%m/%d/%y')
    header = pd.date_range(start=min_date, end=max_date)
    header = [dt.datetime.strftime(x, '%m/%d/%y') for x in header]

    # model output indices start at 1
    county_numbers = np.arange(1, len(fips_list) + 1)

    simulation_data = pd.read_csv(simulation_file_counties, delimiter=',', index_col=0)

    timeseries_data = pd.read_csv(timeseries_file, delimiter=',')
    timeseries_data = timeseries_data[timeseries_data['FIPS'] % 1000 != 0]
    timeseries_data = timeseries_data.reset_index()

    plotting_data = pd.DataFrame(columns=header)
    plotting_data.insert(loc=0, column='FIPS', value=timeseries_data['FIPS'].values)

    for county_number, state, start_date in zip(county_numbers, fips_list, start_dates):
        time_data = list(pd.date_range(start=start_date, end=max_date_))
        time_data = [dt.datetime.strftime(x, '%m/%d/%y') for x in time_data]
        num_days = len(time_data)
        start = 'Rt[1,' + str(county_number) + ']'
        end = 'Rt[' + str(num_days) + ',' + str(county_number) + ']'
        Rt_data = simulation_data.loc[start:end]

        data = Rt_data['mean'][:num_days].values
        plotting_data.loc[plotting_data.index[plotting_data['FIPS'] == state], time_data] = data

    plotting_data.to_csv(r'data\us_data\Rt_data_counties.csv', na_rep='NA', index=False)


if __name__ == '__main__':
    parse_Rt_for_states('05/04/20')
    parse_Rt_for_counties('05/04/20')

