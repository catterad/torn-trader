#!/usr/bin/python3

import requests
import argparse
import os.path
from ast import literal_eval

api_key = "qPOHTchsOjtNSYDD"

wantedlist = {"Cannabis":7000, "Trout":17000, "Wolverine Plushie":9500, "Hockey Stick":4000, "Heather":40000, "Stingray Plushie":9000}

# api_key = os.environ['TORN']

def throw_an_error(code):
    if code == 1:
        print("Error 1: Are you online?")
    elif code == 20:
        print("Error 20: Item ID has to be an integer")
    elif code == 21:
        print("Error 21: Item name has to be a string")
    elif code == 100:
        print("Error 100: Item doesn't exist or there are no offers on the item market")
    exit(code)


def itemload():
    if os.path.exists("tornitems.kot"):
        cache = open("tornitems.kot", "r")
        data = literal_eval(cache.read())
        cache.close()
        return (data)
    else:
        itemupdate()
        print("Item list updated.")
        return (itemload())


def getprices(item_id):
    prices = market_api_call(item_id)
    all_prices = []
    for source in prices:
        for seller in prices[source]:
            all_prices.append(seller['cost'])
    return (all_prices)


def find_id(data, name):
    for itemid in data["items"]:
        if data["items"][str(itemid)]["name"] == name:
            return (itemid)


def sort_and_present(prices):
    prices.sort()
    i = 0
    while i < len(prices) and i <= 20:
        print(number_output(prices[i]))
        i += 1
    exit(0)


def itemupdate():
    r = requests.get("https://api.torn.com/torn/?selections=items&key=" + api_key)
    cache = open("tornitems.kot", "w+")
    cache.write(str(r.json()))
    cache.close()


def itemload():
    if os.path.exists("tornitems.kot"):
        cache = open("tornitems.kot", "r")
        data = literal_eval(cache.read())
        cache.close()
        return (data)
    else:
        itemupdate()
        print("Item list updated.")
        return (itemload())


def getprices(item_id):
    prices = market_api_call(item_id)
    all_prices = []
    for source in prices:
        for seller in prices[source]:
            all_prices.append(seller['cost'])
    return (all_prices)


def number_output(number):
    return ('{:,}'.format(number))


def market_api_call(item):
    try:
        p = requests.get("https://api.torn.com/market/" + str(item) + "?selections=bazaar,itemmarket&key=" + api_key)
        prices = p.json()
        if prices['bazaar'] is None and prices['itemmarket'] is None:
            throw_an_error(100)
        elif prices['bazaar'] is None:
            del prices['bazaar']
        elif prices['itemmarket'] is None:
            del prices['itemmarket']
        return (prices)
    except requests.exceptions.ConnectionError:
        throw_an_error(1)


parser = argparse.ArgumentParser(description="Torn-trader v1 by Catterad")
parser.add_argument("--name", help="Name of the item")

args = parser.parse_args()

data = itemload()
for item in wantedlist:
    print(item)
    prices_list = getprices(find_id(data, item))
    for price in prices_list:
        if(int(price) <= wantedlist[item]):
            print("Buy " + str(item) + " " + str(price))


if args.name:
    try:
        int(args.name)
    except:
        data = itemload()
        prices_list = getprices(find_id(data, args.name))
        sort_and_present(prices_list)
    throw_an_error(21)

