from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.request import Request
import requests
import json
import datetime

with open('/Users/hckcksrl/Desktop/study/box_office/box_office/box/config.json', 'r') as f:
    config = json.load(f)

api_key = config['api_key']


class Daily_Box(APIView):

    def get_box_office(self):
        todey = datetime.datetime.now().strftime('%Y%m%d')
        date = str(int(todey) - 1)
        api = f'http://www.kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchDailyBoxOfficeList.json?key={api_key}&targetDt={date}'
        data = requests.get(api)
        return data.json()

    def get(self, request:Request):
        box = self.get_box_office()
        return Response(status=status.HTTP_200_OK)

class Weekly_Box(APIView):

    def post(self, request:Request):
        pass



# Create your views here.
