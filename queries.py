import psycopg2
import pandas as pd
import matplotlib.pyplot as plt

def make_query(sql, columns_names):
    with psycopg2.connect(dbname="game_events", user="student", password="student", host="127.0.0.1") as conn:
        with conn.cursor() as cursor:
            cursor.execute(sql)
            rerords = cursor.fetchall()
            return pd.DataFrame(rerords, columns=columns_names)

def get_all_records():
    sql = 'select * from test_schema.red_robot_game limit 10;'
    columns_names = ['user_id', 'event_date', 'event_name', 'event_param']
    df = make_query(sql, columns_names)
    print(df)

def get_dau():
    sql = '''select event_date, count(distinct user_id) as users from course.red_robot_game where event_name='login' group by event_date order by event_date;'''
    sql = '''select count(1) as users from course.red_robot_game where event_name='first_open';'''
    #columns_names = ['event_date', 'count']
    df = make_query(sql, ['count'])
    print(df)
    exit()
    plt.title('Количество игроков')
    plt.xlabel('дата')
    plt.ylabel('число игроков')
    plt.plot(df['event_date'], df['count'])
    plt.grid()
    plt.tight_layout()
    plt.show()
#get_dau()

def get_monetization():
    sql = '''select event_date, sum(event_param_int) as value from test_schema.red_robot_game where event_name='purchase' group by event_date order by event_date;'''
    columns_names = ['event_date', 'value']
    df = make_query(sql, columns_names)
    plt.title('Монетизация')
    plt.xlabel('дата')
    plt.ylabel('выкучка, $')
    plt.plot(df['event_date'], df['value'])
    plt.xticks(rotation=90)
    plt.grid()
    plt.tight_layout()
    plt.show()
#get_monetization()

def get_funnel():
    sql = '''select event_param_int as level, count(user_id) as count from test_schema.red_robot_game where event_name='start_level' group by event_param_int order by level;'''
    columns_names = ['level', 'count']
    df = make_query(sql, columns_names)
    plt.title('Воронка оттока игроков по уровням')
    plt.xlabel('уровень')
    plt.ylabel('число игроков')
    plt.plot(df['level'], df['count'])
    plt.xticks(rotation=90)
    plt.grid()
    plt.tight_layout()
    plt.show()
#get_funnel()

def get_retention():
    sql = '''
    with all_users as
    (select
        user_id,
        event_date as first_day
    from
        course.red_robot_game
    where
        event_name='first_open' and
        event_date >= to_timestamp('2022-01-01', 'YYYY-MM-DD') and
        event_date < to_timestamp('2022-11-01', 'YYYY-MM-DD')),
    
    logins as
    (select
        user_id,
        event_date
    from
        course.red_robot_game
    where
        event_name='login'),
    
    days_in_game as
    (select
        all_users.user_id,
        EXTRACT(DAY FROM logins.event_date - all_users.first_day) as days
    from
        all_users
    left join
        logins
    on
        all_users.user_id = logins.user_id)

    select
        days,
        COUNT(user_id)::decimal /(SELECT COUNT(1) from all_users)
    from
        days_in_game
    group by
        days
    order by
       days
    ;'''
    sql = '''
    with all_users as
    (select
        user_id,
        event_date as first_day
    from
        course.red_robot_game
    where
        event_name='first_open' and
        event_date >= to_timestamp('2022-01-01', 'YYYY-MM-DD') and
        event_date < to_timestamp('2022-11-01', 'YYYY-MM-DD')),
    
    logins as
    (select
        user_id,
        event_date
    from
        course.red_robot_game
    where
        event_name='login'),
    
    days_in_game as
    (select
        all_users.user_id,
        all_users.first_day, 
        EXTRACT(DAY FROM logins.event_date - all_users.first_day) as days
    from
        all_users
    left join
        logins
    on
        all_users.user_id = logins.user_id)

    select
        first_day,
        COUNT(user_id) as count 
    from
        days_in_game
    where
        days = 1
    group by
        first_day
    order by
       first_day
    ;'''    
    columns_names = ['days', 'count']
    df = make_query(sql, columns_names)
    print(df)
    #exit()
    plt.title('Возврат игроков на следующий день')
    plt.xlabel('день')
    plt.ylabel('доля игроков')
    plt.plot(df['days'], df['count'])
    #plt.xlim(0,30)
    plt.grid()
    plt.tight_layout()
    plt.show()
get_retention()