from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest, QueryDict

from predict_house_prices.models import House, City
import requests, json, math, numpy, re
from django.core import serializers
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import BayesianRidge
from sklearn.tree import DecisionTreeRegressor
from sklearn.feature_extraction import DictVectorizer
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
import sklearn
import locale

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
	locale.setlocale( locale.LC_ALL, '' )
	# Iterate over returned houses and provide the format needed
	# for the bubbles in datamaps
	bubbles = []
	for house in houses:
		house_dict = {'zip_code': house.zip_code,
			'fillKey': house.house_type,
			'house_type': house.house_type,
			# Use monotonic transformation to adjust price for radius
			'radius': math.sqrt(house.actual_price) / 100,
			'city': house.city.title(),
			'actual_price': locale.currency(house.actual_price, grouping=True),
			'beds': house.beds, 'baths': house.baths,
			'square_feet': house.square_feet,
			'predicted_price': locale.currency(house.predicted_price, grouping=True),
			'latitude': house.latitude,
			'longitude': house.longitude}
		bubbles += [house_dict]
	return HttpResponse(json.dumps(bubbles))

'''
Pass in JSON object of the form in a POST
request. House covariates is optional, used for prediction.

		['houseCovariates':[
			'zip': house.zip_code, 
			'state': house.state, 
			'city': house.city,
			'type': house.house_type,
			'beds': house.beds, 
			'baths': house.baths, 
			'sqfeet': house.square_feet
			],
		'modelType': ['linear', 'bayes', 'tree'],
		'interactions': ['true','false'],
		'clustering': ['true', 'false'],
		'supplementary: ['true', 'false']
		]
'''
def linear_model(request):
	print("Model settings ------------") 
	modelSettings = request.GET.dict()
	print(modelSettings)

	# Get houses and separate them into X and Y variables
	houses = House.objects.all()
	X = []
	Y = []

	#print("House covariates ------------") 
	for house in houses:
		houseCovariates = {
			'zip': house.zip_code, 
			'state': house.state, 
			'city': house.city, 
			'type': house.house_type,
			'beds': house.beds, 
			'baths': house.baths, 
			'sqfeet': house.square_feet
		}
		# Add beds * city and beds * type if interactions are on
		# Since we're interacting a categorical variable with a 
		# discrete numerical one, I simply concatenate the covariates
		# Note that we have to check string equality to 'true' here 
		# rather than a boolean value.  This is because we are passed in a 
		# string of 'true' or 'false' rather than a boolean.  This should be 
		# fixed to be made more intuitive.
		if modelSettings['interactions'] == 'true':
			print(True)
			houseCovariates['beds*city'] = str(house.beds) + "*" + house.city
			houseCovariates['beds*type'] = str(house.beds) + "*" + house.house_type
		
		print(houseCovariates)
		X += [houseCovariates]
		Y += [house.actual_price]
		#print("House Price: " + str(house.actual_price))
	
	# We need to turn our covariate matrix into a list of dictionary
	# to take care of the encoding of categorical data
	#print(enumerate(X[1]))
	#X = [dict(enumerate(covariate)) for covariate in X]
	#print("List of dicts ------------") 
	#for dictionary in X: print(dictionary)

	# Turn list of dicts into a numpy array
	vect = DictVectorizer(sparse=False)
	# This reorganizes our covariate array to represent first the continuous
	# variables (in alphabetical order), and then the categorical variables,
	# ordered first by key (alphabetical) then value (alphabetical)
	X = vect.fit_transform(X)
	
	print(vect.vocabulary_)
	print(vect.feature_names_)
	#print("Numpy Array ------------") 
	#for arr in X: print(numpy.array_str(arr, suppress_small = True))

	# Default model is linear
	clf = LinearRegression()
	if modelSettings['modelType'] == 'bayes':
		clf = BayesianRidge()
	elif modelSettings['modelType'] == 'tree':
		clf = DecisionTreeRegressor(max_depth=5)
	clf.fit(X, Y)

	# Train the model
	print("Model parameters ------------") 
	print(clf.get_params())

	# Model coefficients
	#print("Model coefficients ------------") 
	#print(clf.coef_, clf.intercept_)

	# Predict price based on covariates
	print("Predictions (actual, predicted) ------------") 
	
	# For each house, compare difference between predicted and actual price
	averageDiff = []
	predictedList = []
	actualList = []
	squaredDiff = 0

	print("Interactions ------------") 
	print("Interactions on: " + modelSettings['interactions'])

	for house in houses:
		houseCovariates = [house.zip_code, house.state, house.house_type,
			house.beds, house.baths, house.square_feet]
		houseCovariates = {
			'zip': house.zip_code, 
			'state': house.state, 
			'city': house.city,
			'type': house.house_type,
			'beds': house.beds, 
			'baths': house.baths, 
			'sqfeet': house.square_feet
		}		
		
		if modelSettings['interactions'] == 'true':
			houseCovariates['beds*city'] = str(house.beds) + "*" + house.city
			houseCovariates['beds*type'] = str(house.beds) + "*" + house.house_type

		covariates = vect.transform(houseCovariates)

		predicted_price = float(clf.predict(covariates[0]))
		house.predicted_price = predicted_price
		house.save()

		predictedList += [predicted_price]
		actualList += [house.actual_price]

		averageDiff += [predicted_price - house.actual_price]
		squaredDiff += (predicted_price - house.actual_price) ** 2
	
	print("Average Difference (actual, predicted) ------------") 
	averageDiff = numpy.mean(averageDiff)

	# Note that LSR and BRR use model coefficients but our decision tree
	# uses feature importances.  Both can output in a similar way
	# Build out a dictionary of model parameters to return
	prettyModelCoef = {}
	modelCoef = None
	if modelSettings['modelType'] == 'tree':
		modelCoef = clf.feature_importances_
	else:
		modelCoef = clf.coef_
	print(modelCoef)
	for index in range(0, len(modelCoef)):
		prettyModelCoef[vect.feature_names_[index]] = modelCoef[index]

	# Return a prediction only if houseCovariates is passed in
	housePrediction = None

	# Note that houseCovariates should be its own dictionary
	# but I was having issues with getting a dictionary from POST
	# so we have an unconventional key, value pairing that should be fixed
	# later.
	if modelSettings.has_key('houseCovariates[beds]'):
		houseCovariates = {'zip': modelSettings['houseCovariates[zip]'], 
			'state': modelSettings['houseCovariates[state]'], 
			'city': modelSettings['houseCovariates[city]'], 
			'type': modelSettings['houseCovariates[type]'],
			'beds': int(modelSettings['houseCovariates[beds]']), 
			'baths': int(modelSettings['houseCovariates[baths]']), 
			'sqfeet': int(modelSettings['houseCovariates[sqfeet]'])}

		if modelSettings['interactions'] == 'true':
			houseCovariates['beds*city'] = str(house.beds) + "*" + house.city
			houseCovariates['beds*type'] = str(house.beds) + "*" + house.house_type

		housePrediction = clf.predict(vect.transform(houseCovariates))[0]

	print("Metrics ------------") 
	print("r^2: " + str(r2_score(actualList, predictedList)))

	response = {'modelcoefficients': prettyModelCoef,
		'modelPrediction': housePrediction,
		'averageDiff': averageDiff,
		'ssDiff': squaredDiff,
		'predictedList': predictedList,
		'actualList': actualList,
		'metrics': {
				'rsquared': r2_score(actualList, predictedList),
				'mean_squared_error': mean_squared_error(actualList, predictedList),
				'mean_absolute_error': mean_absolute_error(actualList, predictedList)
			}
		}

	return HttpResponse(json.dumps(response))

# Scrape city data
def load_cities(request):
	houses = House.objects.all()
	cityStateSet = set([(house.city, house.state) for house in houses])
	stateAbbrevMap = {'CA': 'California'}

	# Keep track of features requested and found
	totalFeatures = 0
	foundFeatures = 0
	manualCities = []
	completedCities = []

	for city, state in cityStateSet:

		# Get density from wikipedia
		city = re.sub(" ", "_", city.title())
		stateAbbrev = stateAbbrevMap[state]
		url = "http://en.wikipedia.org/wiki/%s,_%s" % (city, stateAbbrev)
		page = requests.get(url)
		pageText = page.text
		pageText = re.sub(",","",pageText)
		density = re.findall("(\d+)/sq",pageText)

		# Get median income and value from city-data
		city = re.sub("_", "-", city)
		url = "http://www.city-data.com/city/%s-%s.html" % (city, stateAbbrev)
		page = requests.get(url)
		pageText = page.text
		pageText = re.sub(",","",pageText)
		medianIncome = re.findall("Estimated median household income in 2012.*?(\d+)",pageText)
		medianHouseholdValue = re.findall("Estimated median house or condo value in 2012.*?(\d+)",pageText)
		print(medianIncome)
		featureSet = [density, medianIncome, medianHouseholdValue]
		totalFeatures += len(featureSet)
		foundFeatures += len([feature for feature in featureSet if len(feature)>0])

		if len(medianIncome) > 0:
			medianIncome = int(medianIncome[0])
		else:
			medianIncome = 0
		
		if len(medianHouseholdValue) > 0:
			medianHouseholdValue = int(medianHouseholdValue[0])
		else:
			medianHouseholdValue = 0
		
		if len(density) > 0:
			density = density[0]
		else:
			density = 0

		if foundFeatures < totalFeatures: 
			manualCities += [city]
		else:
			completedCities += [city]

		City.objects.create(city = re.sub("-"," ",city.upper()),
			state = state, median_income = int(medianIncome), 
			population_density = int(density), median_household_value = int(medianHouseholdValue))

	return HttpResponse(json.dumps({'totalFeatures': totalFeatures,
		'foundFeatures': foundFeatures, 'Needs Manual': manualCities, 'Completed Cities': completedCities}))
