from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest, QueryDict

from predict_house_prices.models import House, City
import requests, json, math
from django.core import serializers
from sklearn import linear_model
import sklearn



# Create your views here.
def main_page(request):
	return HttpResponse("test")

def load_data(request):
	import requests
	data_csv = requests.get("https://s3.amazonaws.com/opendoor-problems/sacramento_txns.csv").text
	data_rows = data_csv.splitlines()
	count = 0
	for row in data_rows[1:]:
		count += 1 
		street, city, zip_code, state, beds, baths, square_feet, house_type, sale_date, price, latitude, longitude = tuple(row.split(','))
		House.objects.create(street = street, city = city, zip_code = zip_code,
			state = state, beds = beds, baths = baths, square_feet = square_feet,
			house_type = house_type, sale_date = sale_date, actual_price = price,
			latitude = latitude, longitude = longitude)

	return HttpResponse("Saved %d houses to the database" % count)

def return_houses(request):
	houses = House.objects.all()
	return HttpResponse(serializers.serialize("json", houses), content_type='application/json')

def return_house_bubbles(request):
	houses = House.objects.all()
	# Iterate over returned houses and provide the format needed
	# for the bubbles in datamaps
	bubbles = []
	for house in houses:
		house_dict = {'zip_code': house.zip_code,
			'fillKey': house.house_type,
			# Use monotonic transformation to adjust price for radius
			'radius': math.sqrt(house.actual_price) / 100,
			'actual_price': house.actual_price,
			'beds': house.beds, 'baths': house.baths,
			'square_feet': house.square_feet,
			'predicted_price': house.predicted_price,
			'latitude': house.latitude,
			'longitude': house.longitude}
		bubbles += [house_dict]
	return HttpResponse(json.dumps(bubbles))

def linear_model(request):
	# Create linear regression object
	regr = linear_model.LinearRegression()

	# Get houses and separate them into X and Y variables
	houses = House.objects.all()
	X_matrix = []
	Y_matrix = []

	for house in houses:
		houseCovariates = [house.zip_code, house.state, house.house_type,
			house.beds, house.baths, house.square_feet]
		X_matrix += houseCovariates
		Y_matrix += [house.actual_price]


	# Train the model
	regr.fit(X_matrix, Y_matrix)

	# The coefficients
	print('Coefficients: \n', regr.coef_)