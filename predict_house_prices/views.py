from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest, QueryDict

from predict_house_prices.models import House, City
import requests, json, math, numpy
from django.core import serializers
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import BayesianRidge
from sklearn.feature_extraction import DictVectorizer
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

'''
To predict, pass in JSON object of the form in a POST
request.

		['houseCovariates':[
			'zip': house.zip_code, 
			'state': house.state, 
			'type': house.house_type,
			'beds': house.beds, 
			'baths': house.baths, 
			'sqfeet': house.square_feet
		]
'''
def linear_model(request):

	# Get houses and separate them into X and Y variables
	houses = House.objects.all()
	X = []
	Y = []

	print("House covariates ------------") 
	for house in houses:
		houseCovariates = {
			'zip': house.zip_code, 
			'state': house.state, 
			'type': house.house_type,
			'beds': house.beds, 
			'baths': house.baths, 
			'sqfeet': house.square_feet
		}
		#print(houseCovariates)
		X += [houseCovariates]
		Y += [house.actual_price]
		#print("House Price: " + str(house.actual_price))
	
	# We need to turn our covariate matrix into a list of dictionary
	# to take care of the encoding of categorical data
	#print(enumerate(X[1]))
	#X = [dict(enumerate(covariate)) for covariate in X]
	print("List of dicts ------------") 
	#for dictionary in X: print(dictionary)

	# Turn list of dicts into a numpy array
	vect = DictVectorizer(sparse=False)
	# This reorganizes our covariate array to represent first the continuous
	# variables (in alphabetical order), and then the categorical variables,
	# ordered first by key (alphabetical) then value (alphabetical)
	X = vect.fit_transform(X)
	
	# 
	print(vect.vocabulary_)
	print(vect.feature_names_)
	print("Numpy Array ------------") 
	#for arr in X: print(numpy.array_str(arr, suppress_small = True))

	#clf = BayesianRidge()
	clf = LinearRegression()
	clf.fit(X, Y)

	# Train the model
	print("Model parameters ------------") 
	print(clf.get_params())

	# Model coefficients
	print("Model coefficients ------------") 
	print(clf.coef_, clf.intercept_)

	# Predict price based on covariates
	print("Predictions (actual, predicted) ------------") 
	
	# For each house, compare difference between predicted and actual price
	averageDiff = []
	predictedList = []
	actualList = []
	squaredDiff = 0

	for house in houses:
		houseCovariates = [house.zip_code, house.state, house.house_type,
			house.beds, house.baths, house.square_feet]
		houseCovariates = {
			'zip': house.zip_code, 
			'state': house.state, 
			'type': house.house_type,
			'beds': house.beds, 
			'baths': house.baths, 
			'sqfeet': house.square_feet
		}		

		covariates = vect.transform(houseCovariates)

		predictedList += [clf.predict(covariates[0])]
		actualList += [house.actual_price]

		averageDiff += [clf.predict(covariates[0]) - house.actual_price]
		squaredDiff += (clf.predict(covariates[0]) - house.actual_price) ** 2
	
	print("Average Difference (actual, predicted) ------------") 
	averageDiff = numpy.mean(averageDiff)

	if request.method == 'POST':
		predictionDict = request.POST.dict()['houseCovariates']
		houseCovariates = vect.transform(predictionDict)
	else:
		houseCovariates = covariates[0] 

	# Build out a dictionary of model parameters to return
	prettyModelCoef = {}
	for index in range(0, len(clf.coef_)):
		prettyModelCoef[vect.feature_names_[index]] = clf.coef_[index]

	response = {'modelcoefficients': prettyModelCoef,
		'modelPrediction': clf.predict(houseCovariates),
		'averageDiff': averageDiff,
		'ssDiff': squaredDiff,
		'predictedList': predictedList,
		'actualList': actualList}

	return HttpResponse(json.dumps(response))