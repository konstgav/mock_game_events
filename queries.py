import psycopg2
import pandas as pd
import matplotlib.pyplot as plt

def make_query(sql, columns_names):
    with psycopg2.connect(dbname="test_db", user="student", password="student", host="127.0.0.1") as conn:
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
    sql = '''select event_date, count(distinct user_id) as users from test_schema.red_robot_game where event_name='login' group by event_date order by event_date;'''
    columns_names = ['event_date', 'count']
    df = make_query(sql, columns_names)
    plt.title('Количество игроков')
    plt.xlabel('дата')
    plt.ylabel('число игроков')
    plt.plot(df['event_date'], df['count'])
    plt.xticks(rotation=90)
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
get_monetization()

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
#get_retention