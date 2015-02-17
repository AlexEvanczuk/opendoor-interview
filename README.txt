README.txt

Author: Alex Evanczuk
Date: February 16, 2015
Purpose: Predict price for CA houses

Approach:
Prediction:
I use a variety of mathematical techniques to predict the house price.  I begin with straightforward multiple linear regression, using city, zip, state, and type as categorical variables, with beds, baths, and square feet as numerical variables.  I then check interaction effects, by seeing the effect that different house sizes have depending on location and type, by exploring the interactions of beds*city and beds*type.

Naive bayes and decision trees are employed as well to predict price.  Furthermore, I'm interested in the effect of geographical distribution independent of zip code, so I use k-means clustering on the coordinates of the houses to put them into de facto regions, which are then fed back into the original models.  I also give an option to use k-means clustering to categorize house types in three dimensions -- beds, baths, and square-feet. 

Lastly, I am interested in supplementing my data with data in public repositories.  I step back and consider what information can be decomposed in a way that adds more than the sum of its parts, and I fgure that I can create a seperate Django model for city and add several covariates.  City-data.com offers a number of interesting covariates for each US city, and the ones I can include that seem at least marginally interesting are population, median income, population density, demographics, median household value, and distance to nearest city with population > 1,000,000.  Several other measures may seem interesting (or variations of measures such as standard deviation instead of mean), but to avoid overfitting I leave these out.  Of these, I select median income, population density, and median household value.  The code should allow for additional covariates to be added in a very maintanable way.  The additional covariates are researched and loaded in manually using Django's administration page.

Future iterations could find a reliable API or page with a reliable structure and use web scraping techniques to pull additional information about cities to be put arbitrarily into a database, for procedural model generation.  For example, we might be interested in the location of a house to popular businesses, bars, restaurants, job listings, events, activities, etc.  A flexible web scraping framework would provide the infrastructure to create sophisticated housing pricing models.

In summary, the following model options are available:
Multiple Linear Regression
Multiple Linear Regression with interactions
Multiple Linear Regression with interactions and clustering
Multiple Linear Regression with interactions and city data
Naive Bayes 
Naive Bayes with clustering 
Naive Bayes with clustering and city data
Decision trees 
Decision trees with clustering
Decision trees with clustering and city data

Presentation:
This project is presented as a Django web app hosted on Heroku.  On the backend, I keep the default Django database, and create a model for each house with each field stored as a property with the respective data type.  These models are pulled into a Django view for the data analysis.  While it may be wise for larger data sets to store model results in server memory (or at least as a set of parameters for easy model recreation), in this case I recreate the model on every page load.  This ensures that the model always incorporates all data in the database.

The page is laid out with four views: about, models, visualization, and prediction.  The about page  outlines the purpose of the project.  The models page allows you to see the mathematical output of your model's parameters and visualize the model on graphs and charts.  The visualization page presents a map which uses D3 to display the results visually.  Every node is a house.  Nodes are placed based on longitude and latitude, sized according to (actual) price, darkened according to square feet, and colored according to type.  Each of these adjustments can be turned on or off.  Hover over nodes to display each property of a node, as well as its predicted price.  The prediction page is explained below.

Prediction:
Lastly, I offer the ability to predict the price of a new house.  In the input new house box, you can input the values of each property of the house, and it will output the predicted price of that house, as well as place the new house on the map.  Note that for the sake of presentation, the node color will be greyscale.  Also note that the input fields only allow for domain selection for previously predicted categories, or continuous values within one standard deviation of the domain.

Design:
I used the flat-ui user interface kit with user interactions designed manually to create this web-app.  I wanted the user experience to feel like a single interactive infographic where changed state data creates global change, rather than a "settings based" website (though the distinction is perhaps not clear).  Their is a clear division of functionality.  All visualizations and interactions post-model generations are displayed in the main page, and any changes to model creation are done in the sidebar.

Simple is good.

Technical notes:
Future iterations should migrate to a SQL database for more sophisticated and numerous database operations.

http://www.berriart.com/sidr/#
Sidr - A jQuery plugin for creating side menus

http://designmodo.github.io/Flat-UI/
FlatUI - Free User Interface Kit

http://www.city-data.com/city/Rio-Linda-California.html
CityData - Information about different cities

http://en.wikipedia.org/wiki/Sacramento,_California
Additional city information

http://datamaps.github.io/
DataMaps - Visual city data

Plots - http://scikit-learn.org/stable/auto_examples/cluster/plot_cluster_iris.html
Random Forest - http://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html
Clustering - http://scikit-learn.org/stable/modules/clustering.html#k-means
Decision Tree - http://scikit-learn.org/stable/modules/tree.html
Naive Bayes - http://scikit-learn.org/stable/modules/naive_bayes.html
Supervised Learning - http://scikit-learn.org/stable/supervised_learning.html#supervised-learning
Sci-Kit - Machine learning package for python

https://devcenter.heroku.com/articles/getting-started-with-django
Heroku - Hosting platform for webapps

https://docs.google.com/document/d/1jlOj_QNyyZjTlFm3DH-LEcf6eMVyjidmvl1zILGqXN0/edit
OpenDoor data science questions
