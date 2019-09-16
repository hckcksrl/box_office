from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.request import Request
import requests
import json
import datetime
from urllib import parse,request

with open('/Users/hckcksrl/Desktop/study/box_office/box_office/box/config.json', 'r') as f:
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
        data = requests.get(api)
        return data.json()

    def data_list(self,movies):
        movies_list=[]
        for movie in movies :
            movie_content = get_movie_content(movie['movieNm'])
            dicts ={
                "title": movie['movieNm'],
                "description": f'감독 : {movie_content["items"][0]["director"].replace("|","")}\n출연 : {movie_content["items"][0]["actor"]}\n평점 : {movie_content["items"][0]["userRating"]}',
                "thumbnail": {
                    "imageUrl": movie_content["items"][0]["image"],
                    "link": movie_content["items"][0]["link"]
                },
                "buttons": [
                    {
                        "action": "webLink",
                        "label": "사이트 이동",
                        "webLinkUrl": movie_content["items"][0]["link"]
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



# Create your views here.
