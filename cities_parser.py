import telebot

import re

from geo_time import get_coord

import os.path

import sqlite3

import random

token = '5872451119:AAFvgixrd41NzCW7Wi6a8Nh2BhnhN6zrTqU'
chat_saved_msg = 1226209785

DB_FILE_NAME = "cities.db"
QUERY_FOR_DB =        """ CREATE TABLE IF NOT EXISTS cities_info (
                          city VARCHAR(255),
                          popularity INT,
                          latitude REAL,
                          longitude REAL
                          ); """

QUERY_FOR_INSERT_DB = "INSERT INTO cities_info VALUES (?, ?, ?, ?);"

def get_text_cities():
    bot = telebot.TeleBot(token)
    chat = bot.get_chat(chat_saved_msg)
    pinned_mes = chat.pinned_message
    return pinned_mes.text

def get_res_cities():
    init_text = get_text_cities()
    names_cities = re.findall('. ([А-Я|а-я|\-|\s]+) - ', init_text)

    popularity_cities = init_text.split('\n')
    popularity_cities = [  re.findall('\\b[\\d]+\\b', elem)[1:] for elem in popularity_cities  ]
    popularity_cities = [  (int)( ''.join(elem) ) for elem in popularity_cities  ]

    result = []
    for i in range(0, len(names_cities)):
        coord_elem = get_coord(names_cities[i])
        result.append( (names_cities[i], popularity_cities[i], coord_elem[0], coord_elem[1] ) )

    return result

def create_sqlite():
    con = sqlite3.connect(DB_FILE_NAME)
    cur = con.cursor()
    cur.execute(QUERY_FOR_DB)

    results_from_internet = get_res_cities()
    con.executemany(QUERY_FOR_INSERT_DB, results_from_internet)

    con.commit()
    con.close()
    return results_from_internet

def get_cities():
    if not os.path.exists(DB_FILE_NAME):
        return create_sqlite()

    con = sqlite3.connect(DB_FILE_NAME)
    cur = con.cursor()
    cur.execute("SELECT * FROM cities_info")
    rows = cur.fetchall()
    return rows

def get2cities():
    source_list = get_cities()
    first_city, second_city = random.randint(0, len(source_list)), random.randint(0, len(source_list))
    while first_city == second_city:
        second_city = random.randint(0, len(source_list))

    return source_list[first_city], source_list[second_city]

def get_info_det_cities(city_from, city_to):
    source_list = get_cities()
    for elem in source_list:
        if elem[0] == city_from:
            res_from = elem
        elif elem[0] == city_to:
            res_to = elem

    return (res_from, res_to)
