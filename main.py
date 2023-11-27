import pandas as pd
import streamlit as st
from fake_data import generate_dataset, generate_dataset_plan

countries = pd.read_csv('countries.csv')

df_size = st.number_input('Dataset size', step=1, value=100)

# expected_revenue = generate_dataset_plan()
expected_revenue = pd.read_csv('local_dataset_plan.csv')

# sales_report = generate_dataset(df_size)
sales_report = pd.read_csv('local_dataset.csv')


revenue_by_country = sales_report.groupby(
    ['country'], as_index=False).sum(numeric_only=True)

revenue_by_country = revenue_by_country.rename(
    columns={'price': 'real revenue'})


# st.table(revenue_by_country)

joined_expected_and_real_revenue_by_country = expected_revenue.merge(
    revenue_by_country, how='left')

# st.table(joined_expected_and_real_revenue_by_country)


joined_expected_and_real_revenue_by_country['diff_expected_and_real_revenue'] = joined_expected_and_real_revenue_by_country['real revenue'] / \
    joined_expected_and_real_revenue_by_country['expected revenue']

# st.table(joined_expected_and_real_revenue_by_country)


def determine_country_color(country):
    colors = {
        'yellow': '#FFDC00',
        'green': '#00FF13',
        'red': '#FF0000'
    }

    # match True:
    #     case _ if country.diff_expected_and_real_revenue > 2:
    #         return colors['green']
    #     case _ if country.diff_expected_and_real_revenue < 0.5:
    #         return colors['red']

    # return colors['yellow']


    if country['diff_expected_and_real_revenue'] > 2:
        return colors['green']
    elif country['diff_expected_and_real_revenue'] < 0.5:
        return colors['red']
    else:
        return colors['yellow']


joined_expected_and_real_revenue_by_country['color'] = joined_expected_and_real_revenue_by_country.apply(
    determine_country_color, axis=1)

# st.table(joined_expected_and_real_revenue_by_country)
full_table = joined_expected_and_real_revenue_by_country.merge(countries)
st.table(full_table)

# CONFIGURATION

show_configurations = st.checkbox('Configurable map?', value=False)
if show_configurations:
    points_size = st.number_input('Points size:', value=100000)
else: # default configuration
    points_size = 100000
    # other configurations (expected revenue range, dataset size etc.)

st.map(
    full_table,
    size=points_size,
    color='color',
    zoom=2
)
