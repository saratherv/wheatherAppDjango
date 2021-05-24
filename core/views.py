from rest_framework.decorators import APIView
from rest_framework.response import Response
# from rest_framework.permissions import AllowAny
from django.shortcuts import render
import json
import requests


def fetchWeatherReport(latitude, longitude):

    url = f"https://api.met.no/weatherapi/locationforecast/2.0/compact?lat={latitude}&lon=-{longitude}"
    response = requests.get(url)
    return response


class WeatherView(APIView):

    def post(self, request):
        if "lat" not in request.data or "long" not in request.data:
            return Response({"sucess" : False, "code": 500, "message" : "Please input values for latitude and longitude"})
        response = fetchWeatherReport(request.data["lat"], request.data["long"])
        if response.status_code == 200:
            response_content = json.loads(response.content)
            return Response({"sucess" : True, "code": response.status_code, "data" : response_content})
        else:
            return Response({"sucess" : False, "code": response.status_code, "message" : "Invalid request"})


class HomeView(APIView):

    def get(self, request):
        return render(request, "index.html")

    def post(self, request):
        latitude = request.POST['latitude']
        longitude = request.POST["longitude"]
        if latitude == None or longitude == None:
            return render(request, "index.html", {"error" : "enter valid data"})
        
        response = fetchWeatherReport(latitude, longitude)
        if response.status_code == 200:
            response_content = json.loads(response.content)
            print(response_content)
            return render(request, "index.html", {"data" : response_content["properties"]})
        return render(request, "index.html", {"error" : "enter valid data"})