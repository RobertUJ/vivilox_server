from vivilox.apps.store.models import category, item, expedient_item, top_rated_cost,purchases,downloads,top_rated_text,license_text 
from django.contrib import admin

admin.site.register(category)
admin.site.register(item)
admin.site.register(top_rated_cost)
admin.site.register(expedient_item)
admin.site.register(purchases)
admin.site.register(downloads)
admin.site.register(top_rated_text)
admin.site.register(license_text)




