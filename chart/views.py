# chart/views.py
from django.shortcuts import render
from .models import Passenger
from django.db.models import Count, Q
import json  # ***json 임포트 추가***
import pandas as pd
import numpy as np

def home(request):
    return render(request, 'home.html')

def covid(request):
    df = pd.read_csv('https://raw.githubusercontent.com/datasets/covid-19/master/data/countries-aggregated.csv', parse_dates=['Date'])
    countries = ['Korea, South', 'Germany', 'United Kingdom', 'US', 'France']
    df = df[df['Country'].isin(countries)]
    df = df.pivot(index='Date', columns='Country', values='Confirmed')

    countries = list(df.columns)
    covid = df.reset_index('Date')
    covid.set_index(['Date'], inplace=True)
    covid.columns = countries

    populations = {'Korea, South': 51269185, 'Germany': 83783942, 'United Kingdom': 67886011, 'US': 331002651,
                   'France': 65273511}
    percapita = df.copy()

    for country in list(percapita.columns):
        percapita[country] = percapita[country] / populations[country] * 1000000

    percapita.index = percapita.index.values.astype(np.int64) // 10**6

    date = list()
    for i in percapita.index:
        date.append(i)

    # Korea, South
    korea_confirmed = list()
    for k in percapita['Korea, South']:
        k = round(k, 1)
        korea_confirmed.append(k)

    # Germany
    germany_confirmed = list()
    for g in percapita['Germany']:
        g = round(g, 1)
        germany_confirmed.append(g)

    # UK
    uk_confirmed = list()
    for uk in percapita['United Kingdom']:
        uk = round(uk, 1)
        uk_confirmed.append(uk)

    # US
    us_confirmed = list()
    for us in percapita['US']:
        us = round(us, 1)
        us_confirmed.append(us)

    # France
    france_confirmed = list()
    for f in percapita['France']:
        f = round(f, 1)
        france_confirmed.append(f)

    korea = list()
    for i in range(len(date)):
        line = []
        line.append(date[i])
        line.append(korea_confirmed[i])
        korea.append(line)

    germany = list()
    for i in range(len(date)):
        line = []
        line.append(date[i])
        line.append(germany_confirmed[i])
        germany.append(line)

    uk = list()
    for i in range(len(date)):
        line = []
        line.append(date[i])
        line.append(uk_confirmed[i])
        uk.append(line)

    us = list()
    for i in range(len(date)):
        line = []
        line.append(date[i])
        line.append(us_confirmed[i])
        us.append(line)

    france = list()
    for i in range(len(date)):
        line = []
        line.append(date[i])
        line.append(france_confirmed[i])
        france.append(line)

    return render(request, 'covid.html', {
        'korea': json.dumps(korea),
        'germany': json.dumps(germany),
        'uk': json.dumps(uk),
        'us': json.dumps(us),
        'france': json.dumps(france)
    })

def covid19(request):
    df = pd.read_csv('https://raw.githubusercontent.com/datasets/covid-19/master/data/countries-aggregated.csv', parse_dates=['Date'])
    countries = ['Korea, South', 'Germany', 'United Kingdom', 'US', 'France']
    df = df[df['Country'].isin(countries)]
    df['Cases'] = df[['Confirmed', 'Recovered', 'Deaths']].sum(axis=1)
    df = df.pivot(index='Date', columns='Country', values='Cases')

    countries = list(df.columns)
    covid = df.reset_index('Date')
    covid.set_index(['Date'], inplace=True)
    covid.columns = countries

    populations = {'Korea, South': 51269185, 'Germany': 83783942, 'United Kingdom': 67886011, 'US': 331002651,
                   'France': 65273511}
    percapita = df.copy()

    for country in list(percapita.columns):
        percapita[country] = percapita[country] / populations[country] * 1000000

    percapita.index = percapita.index.values.astype(np.int64) // 10**6

    date = list()
    for i in percapita.index:
        date.append(i)

    # Korea, South
    korea_confirmed = list()
    for k in percapita['Korea, South']:
        k = round(k, 1)
        korea_confirmed.append(k)

    # Germany
    germany_confirmed = list()
    for g in percapita['Germany']:
        g = round(g, 1)
        germany_confirmed.append(g)

    # UK
    uk_confirmed = list()
    for uk in percapita['United Kingdom']:
        uk = round(uk, 1)
        uk_confirmed.append(uk)

    # US
    us_confirmed = list()
    for us in percapita['US']:
        us = round(us, 1)
        us_confirmed.append(us)

    # France
    france_confirmed = list()
    for f in percapita['France']:
        f = round(f, 1)
        france_confirmed.append(f)

    korea = list()
    for i in range(len(date)):
        line = []
        line.append(date[i])
        line.append(korea_confirmed[i])
        korea.append(line)

    germany = list()
    for i in range(len(date)):
        line = []
        line.append(date[i])
        line.append(germany_confirmed[i])
        germany.append(line)

    uk = list()
    for i in range(len(date)):
        line = []
        line.append(date[i])
        line.append(uk_confirmed[i])
        uk.append(line)

    us = list()
    for i in range(len(date)):
        line = []
        line.append(date[i])
        line.append(us_confirmed[i])
        us.append(line)

    france = list()
    for i in range(len(date)):
        line = []
        line.append(date[i])
        line.append(france_confirmed[i])
        france.append(line)

    return render(request, 'covid19.html', {
        'korea': json.dumps(korea),
        'germany': json.dumps(germany),
        'uk': json.dumps(uk),
        'us': json.dumps(us),
        'france': json.dumps(france)
    })

def ticket_class_view_1(request):  # 방법 1
    dataset = Passenger.objects \
        .values('ticket_class') \
        .annotate(
        survived_count=Count('ticket_class',
                             filter=Q(survived=True)),
        not_survived_count=Count('ticket_class',
                                 filter=Q(survived=False))) \
        .order_by('ticket_class')

    survived_rate = list()

    for entry in dataset:
        survived_rate_data = 1.0 * entry['survived_count'] \
               / (1.0 * entry['survived_count'] + 1.0 * entry['not_survived_count']) * 100.0
        survived_rate.append(survived_rate_data)

    return render(request, 'ticket_class_1.html', {'dataset': dataset,
                                                   'survived_rate': json.dumps(survived_rate)})

#  dataset = [
#    {'ticket_class': 1, 'survived_count': 200, 'not_survived_count': 123},
#    {'ticket_class': 2, 'survived_count': 119, 'not_survived_count': 158},
#    {'ticket_class': 3, 'survived_count': 181, 'not_survived_count': 528}
#  ]