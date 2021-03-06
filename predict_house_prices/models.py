from django.db import models

class House(models.Model):

	street = models.CharField(max_length=1000)
	city = models.CharField(max_length=1000)
	zip_code = models.CharField(max_length=1000)
	state = models.CharField(max_length=1000)
	house_type = models.CharField(max_length=1000)
	sale_date = models.CharField(max_length=1000)
	beds = models.IntegerField()
	baths = models.IntegerField()
	# Some fields have zero in square feet data, which should be 
	# converted to null rather than kept as zero.
	square_feet = models.IntegerField(null = True)
	actual_price = models.FloatField()
	predicted_price = models.FloatField(null = True)
	latitude = models.FloatField()
	longitude = models.FloatField()
	cluster = models.CharField(max_length = 10, blank=True)

	def __unicode__(self):
		return u'%s %s' % (self.zip_code, self.house_type)

class City(models.Model):
	city = models.CharField(max_length=1000)
	state = models.CharField(max_length=1000)
	median_income = models.FloatField(blank=True, null=True)
	population_density = models.FloatField(blank=True, null=True)
	median_household_value = models.FloatField(blank=True, null=True)

	def __unicode__(self):
		return self.city

	class Meta:
		verbose_name_plural = "Cities"

class Cluster(models.Model):
	index = models.CharField(max_length = 10, primary_key=True)
	latitude = models.FloatField()
	longitude = models.FloatField()