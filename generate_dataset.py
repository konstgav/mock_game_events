import pandas as pd
from datetime import datetime, date, timedelta
import uuid
import random 
import numpy as np

def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)


def churn_func(level):
    a = 0.5
    b = 0.5
    threshold = 1. - a*np.exp(-b*level)
    rnd_num = random.random()
    return rnd_num > threshold*user['country_retention_factor']


def pursh_func(level, user):
    min_proba = 0.1
    max_proba = 0.3
    threshold = min_proba - (max_proba-min_proba)*level/100
    rnd_num = random.random()
    return rnd_num < threshold*user['country_monetization_factor']


def get_day_by_level(level):
    mu = 0.3*level**0.5
    sigma = 0.02*level
    return int(abs(random.gauss(mu, sigma)))


def get_dataset_params():
    dataset_params = {}
    dataset_params['old_users_num'] = 1000
    dataset_params['start_date'] = datetime(year=2022, month=1, day=1)
    dataset_params['finish_date'] = datetime(year=2023, month=1, day=1)
    dataset_params['new_daily_users_avg'] = 100
    dataset_params['new_daily_users_std'] = 20
    dataset_params['filename'] = 'events.csv'
    dataset_params['random_seed'] = 42
    dataset_params['max_level'] = 100
    dataset_params['payer_types_thresh'] = [0.04, 0.03, 0.02, 0.01, 0.9]
    dataset_params['prices'] = [2,5,10,20,30,50,100]
    dataset_params['payer_types_probas'] = [[0.6,0.3,0.1,0,0,0,0], [0.2,0.3,0.3,0.2,0,0,0], [0,0.1,0.2,0.3,0.3,0.1,0], [0,0,0,0,0.3,0.4,0.3]]
    dataset_params['country_monetization_factor'] = {'USA': 1.15, 'France': 1.02, 'India': 0.98}
    dataset_params['country_retention_factor'] = {'USA': 1.1, 'France': 1.05, 'India': 1.0}    
    dataset_params['country_user_probas'] = {'USA': 0.4, 'France': 0.3, 'India': 0.3}
    return dataset_params


def get_varian_by_probas(probas):
    rnd_number = random.random()
    proba_thresh = 0
    for i in range(len(probas)):
        proba_thresh += probas[i]
        if rnd_number < proba_thresh:
            return i
    return len(probas)-1


def spawn_user(dataset_params, is_new_user, date):
    user = {}
    user['dataset_params'] = dataset_params
    user['id'] = str(uuid.uuid4())
    user['start_date'] = date
    if is_new_user:
        user['level'] = 0
    payer_types_index = get_varian_by_probas(dataset_params['payer_types_thresh'])
    user['payer_types_index'] = payer_types_index
    if payer_types_index < len(dataset_params['payer_types_thresh'])-1:        
        user['price_probas'] = dataset_params['payer_types_probas'][payer_types_index]
    country_probas = list(dataset_params['country_user_probas'].values())
    country_index = get_varian_by_probas(country_probas)
    country = list(dataset_params['country_user_probas'].keys())[country_index]
    user['country'] = country
    user['country_monetization_factor'] = dataset_params['country_monetization_factor'][country]
    user['country_retention_factor'] = dataset_params['country_retention_factor'][country]
    return user


def create_event(user, event_name, event_date, event_param_int, event_param_str):
    event = {}
    event['user_id'] = user['id']
    event['event_date'] = event_date
    event['event_name'] = event_name
    if event_param_int is not None:
        event['event_param_int'] = event_param_int
    if event_param_str is not None:
        event['event_param_str'] = event_param_str
    event['country'] = user['country']
    #event['user_first_date'] = user['start_date']
    #event['user_total_levels'] = user['level']
    return event


def generate_user_history(user):
    user_events = []
    first_open_event = create_event(user, 'first_open', user['start_date'], None, None)
    user_events.append(first_open_event)
    login_event = create_event(user, 'login', user['start_date'], None, None)
    user_events.append(login_event)    
    max_level = user['dataset_params']['max_level']
    current_date = user['start_date']
    for level in range(user['level'], max_level):    
        if churn_func(level):
            return user_events
        delta_days = get_day_by_level(level)
        current_date += timedelta(delta_days)
        if current_date > dataset_params['finish_date']:
            break
        if delta_days > 0:
            login_event = create_event(user, 'login', current_date, None, None)        
        start_level = create_event(user, 'start_level', current_date, level, None)
        user_events.append(start_level)
        if (user['payer_types_index']< 4) and pursh_func(level, user):
            index = get_varian_by_probas(user['price_probas'])
            price = dataset_params['prices'][index]
            purchase = create_event(user, 'purchase', current_date, price, None)
            user_events.append(purchase)            
    return user_events
        

def generate_user_events(user):
    user_events = generate_user_history(user)
    df_user_events = pd.DataFrame(user_events)
    if 'event_param_int' in df_user_events:
        df_user_events['event_param_int'] = pd.array(df_user_events['event_param_int'], dtype="Int64")
    return df_user_events


if __name__ == '__main__':
    dataset_params = get_dataset_params()
    random.seed(dataset_params['random_seed'])
    events_data = []
    # spawn old users
    # for i in range(dataset_params['old_users_num']):
    #     user = spawn_user(dataset_params, False, dataset_params['start_date'])
    #     user_data = generate_user_events(user)
    #     events_data.append(user_data)

    for single_date in daterange(dataset_params['start_date'], dataset_params['finish_date']):
        num_new_users = int(random.gauss(dataset_params['new_daily_users_avg'], dataset_params['new_daily_users_std']))
        for i in range(num_new_users):
            user = spawn_user(dataset_params, True, single_date)
            user_data = generate_user_events(user)
            events_data.append(user_data)
        print(single_date)
    df = pd.concat(events_data)
    print(df)
    df.to_csv(dataset_params['filename'], index=False)