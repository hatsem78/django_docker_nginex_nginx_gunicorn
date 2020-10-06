from rest_framework.authentication import TokenAuthentication, SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
import requests
import json
from rest_framework import status
from datetime import datetime
from app.settings import KEY_API_WEATHER
from  urllib.request import urlopen


class CheckWeatherView(APIView):
    """
        Retrieve:
            Return List Check Weather  forecast 16th

        **Example request**:

        .. code-block:: http

            GET  api/check_weather/list/
            :parameter
                city is required

    """

    authentication_classes = [
        SessionAuthentication,
        BasicAuthentication,
        TokenAuthentication,
    ]
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=json):
        city = self.request.GET.get('city', None)

        if city is None:
            with urlopen("https://geolocation-db.com/json") as url:
                data = json.loads(url.read().decode())
                city = f"{data['city']}&{data['country_code'].lower()}"
        else:
            city = city.replace(',', '&')

        url = f"https://community-open-weather-map.p.rapidapi.com/forecast/daily?q={city}&units=metric&cnt=16"

        headers = {
            'x-rapidapi-host': "community-open-weather-map.p.rapidapi.com",
            'x-rapidapi-key': "b72f915c95msh1546f213cf7a63ep17e18djsn97b2093b3687"
        }

        response = requests.request("GET", url, headers=headers)

        if response.status_code == 404:
            return Response(json.loads(response.text), status=status.HTTP_200_OK)

        list_weather = []

        for element in json.loads(response.text)['list']:
            list_weather.append({
                'date_day': datetime.fromtimestamp(element['dt']).strftime('%A  %Y-%m-%d'),
                'date': datetime.fromtimestamp(element['dt']).strftime('%Y-%m-%d'),
                'temp': element['temp']['day'],
                'weather_description': element['weather'][0]['description']
            })

        return Response(list_weather)




