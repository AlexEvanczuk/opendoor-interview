import requests
data_csv = requests.get("https://s3.amazonaws.com/opendoor-problems/sacramento_txns.csv").text
data_rows = data_csv.splitlines()
for row in data_rows[1:]:
	#print(tuple(row.split(',')))
	street, city, zip_code, state, beds, baths, square_feet, house_type, sale_date, price, latitude, longitude = tuple(row.split(','))
	print(square_feet)