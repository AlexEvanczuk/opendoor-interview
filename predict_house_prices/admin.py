from django.contrib import admin
from predict_house_prices.models import House, City,Cluster
# Register your models here.
admin.site.register(House)
admin.site.register(City)
admin.site.register(Cluster)
