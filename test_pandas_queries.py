import pandas as pd
from generate_dataset import get_day_by_level
import matplotlib.pyplot as plt
from sqlalchemy import create_engine

def get_purches():
    df = pd.read_csv('events.csv', parse_dates=['event_date'])
    df = df[df['event_name']=='purchase']
    print(df['event_param_int'].value_counts())
    df = df.set_index('event_date')
    res = df.groupby(pd.Grouper(freq='M')).sum()
    print(res)
#get_purches()

def plot_game_time():
    for sample in range(100):
        cur_date = 0
        res = []
        res.append(cur_date)
        for level in range(100):
            cur_date += get_day_by_level(level)
            res.append(cur_date)
        plt.plot(res)
    plt.show()

def plot_events_game_time():
    df = pd.read_csv('events.csv', parse_dates=['event_date'])
    df = df[(df['event_name']=='start_level')&(df['user_id']=='45875cea-eefd-4181-8dcf-9c8fca2e844a')]
    plt.plot(df['event_param_int'], df['event_date'])
    plt.show()

def insert_data():
    df = pd.read_csv('events.csv', parse_dates=['event_date'])
    engine = create_engine('postgresql://student:student@localhost:5432/game_events')
    df.to_sql('course.mad_robots_game', engine)
insert_data()    