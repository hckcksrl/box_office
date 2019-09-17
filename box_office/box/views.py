from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.request import Request
import requests
import json
import datetime
from urllib import parse,request

with open('/home/ubuntu/box_office/box_office/box/config.json', 'r') as f:
    config = json.load(f)

api_key = config['api_key']
client_id = config['client_id']
secret_key = config['secret_key']


def get_movie_content(movie_name):
    movie_name_encode = parse.quote_plus(movie_name)
    url = "https://openapi.naver.com/v1/search/movie.json?query=" + movie_name_encode
    search_request = request.Request(url)
    search_request.add_header("X-Naver-Client-Id", client_id)
    search_request.add_header("X-Naver-Client-Secret", secret_key)
    response = request.urlopen(search_request)
    rescode = response.getcode()
    if rescode == 200:
        response_body = response.read()
        return json.loads(response_body.decode('utf-8'))
    else:
        print("Error code:" + rescode)


def data_list(movies, time):
    movies_list = []
    for movie in movies:

        content = get_movie_content(movie_name=movie['movieNm'])
        movie_content = content["items"][0]
        image = movie_content["image"]
        link = movie_content["link"]
        open_dt = movie["openDt"].replace('-',',')
        audi_cnt = movie["audiCnt"]
        audi_acc = movie["audiAcc"]

        dicts = {
            "title": f'{movie["movieNm"]}\n개봉날짜 : {open_dt} 개봉',
            "description": f'{time.split()[0]} : {"{:,}".format(int(audi_cnt))}명\n누적 :{"{:,}".format(int(audi_acc))}명',
            "thumbnail": {
                "imageUrl": image,
                "fixedRatio": True,
                "width": 480,
                "height": 480,
            },
            "buttons": [
                {
                    "action": "webLink",
                    "label": "사이트 이동",
                    "webLinkUrl": link
                }
            ]
        }
        movies_list.append(dicts)
    return movies_list


class Daily_Box(APIView):

    def get_box_office(self):
        today = datetime.datetime.now()
        date = (today - datetime.timedelta(days=1)).strftime('%Y%m%d')
        api = f'http://www.kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchDailyBoxOfficeList.json?key={api_key}&targetDt={date}'
        data = requests.get(api).json()
        return data



    def post(self, request:Request):
        data = request.data
        block = data['userRequest']['block']['name']

        box = self.get_box_office()
        movies = box['boxOfficeResult']['dailyBoxOfficeList']
        movies_list = data_list(movies=movies,time=block)

        return Response(data={
            "version": "2.0",
            "template": {
                "outputs": [{
                    "carousel": {
                        "type": "basicCard",
                        "items": movies_list
                    }
                }]
            }}
        )


class Weekly_Box(APIView):

    def get_weekly_box(self, block):
        today = datetime.datetime.now()
        day = datetime.datetime.today().weekday()
        date = (today - datetime.timedelta(days=(day+1))).strftime('%Y%m%d')
        week = 0
        if block == '주말 박스오피스':
            week = 1
        api = f'http://www.kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchWeeklyBoxOfficeList.json?key={api_key}&targetDt={date}&weekGb={week}'
        data = requests.get(api).json()
        return data


    def post(self, request:Request):
        data = request.data
        block = data['userRequest']['block']['name']

        box = self.get_weekly_box(block=block)
        movies = box['boxOfficeResult']['weeklyBoxOfficeList']
        movies_list = data_list(movies=movies,time=block)

        return Response(data={
            "version": "2.0",
            "template": {
                "outputs": [{
                    "carousel": {
                        "type": "basicCard",
                        "items": movies_list
                    }
                }]
            }}
        )


class Weeked_Box(APIView):

    def post(self, request:Request):
        pass


class Movie_Search(APIView):

    def post(self, request:Request):
        data = request.data
        movie_name = data['action']['params']['movie_name']

        content = get_movie_content(movie_name=movie_name)
        movie_content = content["items"][0]
        title = movie_content["title"].replace('<b>', '').replace('</b>', '')
        director = movie_content["director"].replace("|", "")
        actor = movie_content["actor"].rstrip('|').replace("|", ",")
        rating = movie_content["userRating"]
        image = movie_content["image"]
        link = movie_content["link"]

        return Response(data={
            "version": "2.0",
            "template": {
                "outputs": [
                    {
                        "basicCard": {
                            "title": title,
                            "description": f'감독 : {director}\n배우 : {actor}\n평점 : {rating}',
                            "thumbnail": {
                                "imageUrl": image,
                                "fixedRatio": True,
                                "width" : 0,
                                "height" : 0
                            },
                            "buttons":[{
                                "action": "webLink",
                                "label": "사이트 이동",
                                "webLinkUrl": link

                            }]
                        }
                    }
                ]}
        }
        )

# Create your views here.
