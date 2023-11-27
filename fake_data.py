import pandas as pd
import numpy as np
from faker import Faker
from faker_vehicle import VehicleProvider
from faker.providers import date_time
import datetime


countries = ['Ukraine', 'England', 'France', 'Germany',
             'Norway', 'Spain', 'Portugal', 'Italy', 'USA', 'China']

date_range = (datetime.date(2022, 1, 1), datetime.date(2022, 12, 31))

car_price_range = (1, 100)

expected_revenue_range = (100, 1000)


fake = Faker()
fake.add_provider(VehicleProvider)
fake.add_provider(date_time)


def generate_dataset(size):
    cars = [fake.vehicle_make() for _ in range(size)]
    dates = [fake.date_between_dates(*date_range) for _ in range(size)]

    data = {
        'car': cars,
        'price': np.random.randint(*car_price_range, size=size),
        'country': np.random.choice(countries, size=size),
        'date': dates
    }

    df = pd.DataFrame(data)

    return df


def generate_dataset_plan():
    revenue = np.random.randint(*expected_revenue_range, size=len(countries))

    data = {
        'expected revenue': revenue,
        'country': countries
    }

    df = pd.DataFrame(data)

    return df