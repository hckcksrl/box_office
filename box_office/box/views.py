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


class Daily_Box(APIView):

    def get_box_office(self):
        todey = datetime.datetime.now().strftime('%Y%m%d')
        date = str(int(todey) - 1)
        api = f'http://www.kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchDailyBoxOfficeList.json?key={api_key}&targetDt={date}'
        data = requests.get(api).json()
        return data

    def data_list(self, movies):
        movies_list = []
        for movie in movies:

            content = get_movie_content(movie['movieNm'])
            movie_content = content["items"][0]
            director = movie_content["director"].replace("|", "")
            actor = movie_content["actor"].rstrip('|').replace("|", ",")
            rating = movie_content["userRating"]
            image = movie_content["image"]
            link = movie_content["link"]

            dicts = {
                "title": f'{movie["movieNm"]}\n감독 : {director}',
                "description": f'출연 : {actor}\n평점 : {rating}',
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


    def post(self, request:Request):
        box = self.get_box_office()
        movies = box['boxOfficeResult']['dailyBoxOfficeList']
        movies_list = self.data_list(movies)

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

    def post(self, request:Request):
        pass


class Weeked_Box(APIView):

    def post(self, request:Request):
        pass


class Movie_Search(APIView):

    def post(self, request:Request):
        data = request.data
        movie_name = data['action']['params']['movie_name']

        content = get_movie_content(movie_name)
        movie_content = content["items"][0]
        title = movie_content["title"].replace('<p>', '').replace('</p>', '')
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
                                "imageUrl": image
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
