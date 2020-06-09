# chart/views.py
from django.shortcuts import render
from .models import Passenger
from django.db.models import Count, Q
import json  # ***json 임포트 추가***
from django.http import JsonResponse  # for chart_data()

def home(request):
    return render(request, 'home.html')

def world_population(request):
    return render(request, 'world_population.html')

def ticket_class_view_1(request):  # 방법 1
    dataset = Passenger.objects \
        .values('ticket_class') \
        .annotate(
        survived_count=Count('ticket_class',
                             filter=Q(survived=True)),
        not_survived_count=Count('ticket_class',
                                 filter=Q(survived=False))) \
        .order_by('ticket_class')
    return render(request, 'ticket_class_1.html', {'dataset': dataset})


#  dataset = [
#    {'ticket_class': 1, 'survived_count': 200, 'not_survived_count': 123},
#    {'ticket_class': 2, 'survived_count': 119, 'not_survived_count': 158},
#    {'ticket_class': 3, 'survived_count': 181, 'not_survived_count': 528}
#  ]

def ticket_class_view_2(request):  # 방법 2
    dataset = Passenger.objects \
        .values('ticket_class') \
        .annotate(survived_count=Count('ticket_class', filter=Q(survived=True)),
                  not_survived_count=Count('ticket_class', filter=Q(survived=False))) \
        .order_by('ticket_class')

    # 빈 리스트 3종 준비
    categories = list()  # for xAxis
    survived_series = list()  # for series named 'Survived'
    not_survived_series = list()  # for series named 'Not survived'

    # 리스트 3종에 형식화된 값을 등록
    for entry in dataset:
        categories.append('%s Class' % entry['ticket_class'])  # for xAxis
        survived_series.append(entry['survived_count'])  # for series named 'Survived'
        not_survived_series.append(entry['not_survived_count'])  # for series named 'Not survived'

    # json.dumps() 함수로 리스트 3종을 JSON 데이터 형식으로 반환
    return render(request, 'ticket_class_2.html', {
        'categories': json.dumps(categories),
        'survived_series': json.dumps(survived_series),
        'not_survived_series': json.dumps(not_survived_series)
    })

def ticket_class_view_3(request):  # 방법 3
    dataset = Passenger.objects \
        .values('ticket_class') \
        .annotate(survived_count=Count('ticket_class', filter=Q(survived=True)),
                  not_survived_count=Count('ticket_class', filter=Q(survived=False))) \
        .order_by('ticket_class')

    # 빈 리스트 3종 준비 (series 이름 뒤에 '_data' 추가)
    categories = list()  # for xAxis
    survived_series_data = list()  # for series named 'Survived'
    not_survived_series_data = list()  # for series named 'Not survived'

    # 리스트 3종에 형식화된 값을 등록
    for entry in dataset:
        categories.append('%s Class' % entry['ticket_class'])  # for xAxis
        survived_series_data.append(entry['survived_count'])  # for series named 'Survived'
        not_survived_series_data.append(entry['not_survived_count'])  # for series named 'Not survived'

    survived_series = {
        'name': 'Survived',
        'data': survived_series_data,
        'color': 'green'
    }
    not_survived_series = {
        'name': 'Not Survived',
        'data': not_survived_series_data,
        'color': 'red'
    }

    chart = {
        'chart': {'type': 'column'},
        'title': {'text': 'Titanic Survivors by Ticket Class'},
        'xAxis': {'categories': categories},
        'series': [survived_series, not_survived_series]
    }
    dump = json.dumps(chart)

    return render(request, 'ticket_class_3.html', {'chart': dump})

def json_example(request):  # 접속 경로 'json-example/'에 대응하는 뷰
    return render(request, 'json_example.html')


def chart_data(request):  # 접속 경로 'json-example/data/'에 대응하는 뷰
    dataset = Passenger.objects \
        .values('embarked') \
        .exclude(embarked='') \
        .annotate(total=Count('id')) \
        .order_by('-total')
    #  [
    #    {'embarked': 'S', 'total': 914}
    #    {'embarked': 'C', 'total': 270},
    #    {'embarked': 'Q', 'total': 123},
    #  ]

    # # 탑승_항구 상수 정의
    # CHERBOURG = 'C'
    # QUEENSTOWN = 'Q'
    # SOUTHAMPTON = 'S'
    # PORT_CHOICES = (
    #     (CHERBOURG, 'Cherbourg'),
    #     (QUEENSTOWN, 'Queenstown'),
    #     (SOUTHAMPTON, 'Southampton'),
    # )
    port_display_name = dict()
    for port_tuple in Passenger.PORT_CHOICES:
        port_display_name[port_tuple[0]] = port_tuple[1]
    # port_display_name = {'C': 'Cherbourg', 'Q': 'Queenstown', 'S': 'Southampton'}

    chart = {
        'chart': {'type': 'pie'},
        'title': {'text': 'Number of Titanic Passengers by Embarkation Port'},
        'series': [{
            'name': 'Embarkation Port',
            'data': list(map(
                lambda row: {'name': port_display_name[row['embarked']], 'y': row['total']},
                dataset))
            # 'data': [ {'name': 'Southampton', 'y': 914},
            #           {'name': 'Cherbourg', 'y': 270},
            #           {'name': 'Queenstown', 'y': 123}]
        }]
    }
    # [list(map(lambda))](https://wikidocs.net/64)

    return JsonResponse(chart)