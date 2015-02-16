README.txt

Author: Alex Evanczuk
Date: February 16, 2015
Purpose: Predict price for CA houses

Approach:
Prediction:
I use a variety of mathematical techniques to predict the house price.  I begin with straightforward multiple linear regression, using city, zip, state, and type as categorical variables, with beds, baths, and square feet as numerical variables.  I then check interaction effects, by seeing the effect that different house sizes have depending on location and type, by exploring the interactions of beds*city and beds*type.

Naive bayes and decision trees are employed as well to predict price.  Furthermore, I'm interested in the effect of geographical distribution independent of zip code, so I use k-means clustering on the coordinates of the houses to put them into de facto regions, which are then fed back into the original models.  I also give an option to use k-means clustering to categorize house types in three dimensions -- beds, baths, and square-feet. 

Lastly, I am interested in supplementing my data with data in public repositories.  I step back and consider what information can be decomposed in a way that adds more than the sum of its parts, and I fgure that I can create a seperate Django model for city and add several covariates.  City-data.com offers a number of interesting covariates for each US city, and the ones I can include that seem at least marginally interesting are population, median income, population density, demographics, median household value, and distance to nearest city with population > 1,000,000.  Several other measures may seem interesting (or variations of measures such as standard deviation instead of mean), but to avoid overfitting I leave these out.  Of these, I select median income, population density, and median household value.  The code should allow for additional covariates to be added in a very maintanable way.  The additional covariates are researched and loaded in manually using Django's administration page.  Future iterations could find a reliable API or page with a reliable structure and use web scraping techniques to pull additional information about cities to be put arbitrarily into a database, for procedural model generation.  For example, we might be interested in the location of a house to popular businesses, bars, restaurants, job listings, events, activities, etc.  A flexible web scraping framework would provide the infrastructure to create sophisticated housing pricing models.

Presentation:
This project is presented as a Django web app hosted on Heroku.  On the backend, I keep the default Django database, and create a model for each house with each field stored as a property with the respective data type.  These models are pulled into a Django view for the data analysis.  While it may be wise for larger data sets to store model results in server memory (or at least as a set of parameters for easy model recreation), in this case I recreate the model on every page load.  This ensures that the model always incorporates all data in the database.

The page is laid out with two views: about and models.  The about page  outlines the purpose of the project.  The models page allows you to select the statistical model of interest, see the mathematical output if its parameters, visualize the model on graphs and charts, and then a map which uses D3 to display the results visually.  Every node is a house.  Nodes are placed based on longitude and latitude, sized according to (actual) price, darkened according to square feet, and colored according to type.  Each of these adjustments can be turned on or off.  Hover over nodes to display each property of a node, as well as its predicted price.

Technical notes:
Future iterations should migrate to a SQL database for more sophisticated and numerous database operations.


