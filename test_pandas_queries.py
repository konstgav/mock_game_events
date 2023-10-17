import pandas as pd
from generate_dataset import get_day_by_level
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
from scipy import stats

def get_purches():
    df = pd.read_csv('events.csv', parse_dates=['event_date'])
    df = df[df['event_name']=='purchase']
    print(df['event_param_int'].value_counts())
    df = df.set_index('event_date')
    res = df.groupby(pd.Grouper(freq='M')).sum()
    print(res)
#get_purches()

def get_contry_purches():
    df = pd.read_csv('events.csv', parse_dates=['event_date'])
    #country = 'India'
    df_purch = df[(df['event_name']=='purchase')] #&(df['country']==country)]
    df_purch = df_purch.groupby(['country', 'user_id']).agg(value=('event_param_int','sum')).reset_index()    
    df_purch.to_csv('purches.csv', index=False)
    data_india = df_purch[df_purch['country']=='India']['value']
    data_usa = df_purch[df_purch['country']=='USA']['value']
    res = stats.ttest_ind(data_usa, data_india, alternative='greater')
    print(res)
#get_contry_purches()

def get_arpu():
    df = pd.read_csv('events.csv', parse_dates=['event_date'])
    df_purch = df[df['event_name']=='purchase']
    total_value = sum(df_purch['event_param_int'])
    total_users = len(df['user_id'].unique())
    print(total_value, total_users, total_value/ total_users)
#get_arpu()

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
#insert_data() 

def count_countries():
    df = pd.read_csv('events.csv', parse_dates=['event_date'])
    df = df[df['event_name']=='first_open']
    df_gr = df.groupby('country').agg(count=('user_id','count'))
    print(df_gr)
#count_countries()

def logins():
    df = pd.read_csv('events.csv', parse_dates=['event_date'])
    df = df[df['event_name']=='login']
    df_gr = df.groupby('event_date').agg(count=('user_id','count'))
    print(df_gr)
    plt.plot(df_gr['count'])
    plt.show()
#logins()

def count_start_level():
    df = pd.read_csv('events.csv', parse_dates=['event_date'])
    df = df[df['event_name']=='start_level']
    df_gr = df.groupby('event_param_int').agg(count=('user_id','count'))
    plt.plot(df_gr)
    plt.show()
count_start_level()

