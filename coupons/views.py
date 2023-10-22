import sqlite3
import logging
import django.db.utils
from django.shortcuts import render
from main import parser, urls_market_dict
from coupons.models import Coupons

menu = ['Главная', 'Yum-yum']


def start_cite():
    get_data_title_db()


def get_data_title_db():
    try:
        all_coupons = Coupons.objects.in_bulk()
        title_in_db = [title for title in all_coupons.keys()]
        title_in_parser = [coup[0] for market_coupons in parser() for coup in market_coupons]
        data_for_del = list((set(title_in_db) - set(title_in_parser)))
        data_for_add = list((set(title_in_parser) - set(title_in_db)))
        add_coupons(data_for_add)
        del_coupons(data_for_del)
    except django.db.utils.IntegrityError:
        logging.basicConfig(level=logging.ERROR, filename="erors_log.log", filemode="a",
                            format="%(asctime)s %(levelname)s %(message)s")
        logging.error('django.db.utils.IntegrityError', exc_info=False)
    except TypeError:
        logging.basicConfig(level=logging.ERROR, filename="erors_log.log", filemode="a",
                            format="%(asctime)s %(levelname)s %(message)s")
        logging.error('TypeError', exc_info=False)


def add_coupons(data_for_add):
    for market in parser():
        for market_coupons in market:
            if market_coupons[0] in data_for_add and len(market_coupons) == 5:
                Coupons.objects.create(
                    title=market_coupons[0],
                    content=market_coupons[1],
                    price=market_coupons[2],
                    photo=market_coupons[3],
                    market_name=market_coupons[4],

                )
            elif market_coupons[0] in data_for_add and len(market_coupons) == 4:
                Coupons.objects.create(
                    title=market_coupons[0],
                    content=market_coupons[1],
                    photo=market_coupons[2],
                    market_name=market_coupons[3],
                )


def del_coupons(list_data_for_del):
    sqlite_connection = sqlite3.connect('db.sqlite3')
    cursor = sqlite_connection.cursor()
    for data in list_data_for_del:
        sql_del = "DELETE FROM coupons_coupons WHERE title = '%s'" % data
        cursor.execute(sql_del)
        sqlite_connection.commit()
    cursor.close()
    sqlite_connection.close()


def index(request):
    return render(request, 'coupons/index.html', {'menu': menu, 'title': menu[0]})


def coupons(request):
    all_coupons = Coupons.objects.all()
    return render(request, 'coupons/coupons.html',
                  {'all_coupons': all_coupons,
                   'urls_market_dict': urls_market_dict,
                   'title': menu[1]})


def coupons_filter_market(request, market_name):
    filter_coupons_market_name = Coupons.objects.filter(market_name=market_name)
    return render(request, 'coupons/coupons.html',
                  {'all_coupons': filter_coupons_market_name,
                   'urls_market_dict': urls_market_dict,
                   'title': menu[1]})


start_cite()
