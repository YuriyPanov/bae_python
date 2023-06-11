from cities_parser import *

from geo_time import *

from pandas_data import *

from selenium_logic import TicketsGetter

import os.path

import matplotlib.pyplot as plt

def generate_csv(b_generate_city, city_from="Москва", city_to="Санкт-Петербург"):
    if b_generate_city:
        city_from, city_to = get2cities()
    else:
        city_from, city_to = get_info_det_cities(city_from, city_to)

    csv_name = city_from[0] + "_" + city_to[0] + ".csv"
    if os.path.exists(csv_name):
        plot_graph(csv_name)
        return

    ticket_manager = TicketsGetter(city_from[0], city_to[0])
    curr_date = get_random_date(get_today())

    for i in range(0, 45):
        ticket_manager.set_new_date(curr_date)
        curr_date = get_next_days(curr_date, 1)
        ticket_manager.first_load()
        count_tickets = ticket_manager.wait_load("card-class__quantity")
        if i == 0 and count_tickets == 0:
            ticket_manager.driver.quit()
            return generate_csv()

        ticket_manager.get_types_tickets()

    export_to_csv(ticket_manager.tickets, csv_name)

def plot_graph(csv_name):
    df = pd.read_csv(csv_name)

    x = df.loc[:, ['Купе']]
    df['Купе_norm'] = (x - x.mean())/x.std()
    df['colors'] = ['red' if x < 0 else 'green' for x in df['Купе_norm']]
    df.sort_values('Купе_norm', inplace=True)
    df.reset_index(inplace=True)

    tmp_cities = csv_name.split('_')

    city_from, city_to = get_info_det_cities(tmp_cities[0], tmp_cities[1].split('.')[0])

    plt.figure(figsize=(9,7), dpi= 80)
    plt.hlines(y=df.index, xmin=0, xmax=df['Купе_norm'], color=df.colors, alpha=0.4, linewidth=5)

    plt.gca().set(ylabel='$Дата$', xlabel='$Нормированная цена на купе$')
    plt.yticks(df.index, df['Дата'], fontsize=12)

    info_city_from = city_from[0] + " : Население - " + str(city_from[1]) + "; Координаты - (" + str(city_from[2]) + ", " + str(city_from[3]) + ")\n"
    info_city_to = city_to[0] + " : Население - " + str(city_to[1]) + "; Координаты - (" + str(city_to[2]) + ", " + str(city_to[3]) + ")\n"
    plt.title(info_city_from + "Едем в \n" + info_city_to, fontdict={'size':13})
    plt.grid(linestyle='--', alpha=0.5)
    #plt.show()
    plt.savefig(csv_name.split('.')[0] + ".png")
