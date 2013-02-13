from vivilox.apps.store.models import category, item, expedient_item, top_rated_cost,purchases,downloads 
from django.contrib import admin

admin.site.register(category)
admin.site.register(item)
admin.site.register(top_rated_cost)
admin.site.register(expedient_item)
admin.site.register(purchases)
admin.site.register(downloads)
