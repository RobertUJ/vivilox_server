from vivilox.apps.contests.models import category, industry, top_rated_cost, contest, duration , cost, resource, proposal, private_cost,proposal_feedback
from django.contrib import admin
from django.contrib.admin import ModelAdmin

admin.site.register(category)
admin.site.register(industry)
admin.site.register(top_rated_cost)
admin.site.register(contest)
admin.site.register(duration)

admin.site.register(resource)
admin.site.register(proposal)
admin.site.register(private_cost)
admin.site.register(proposal_feedback)

# Registro en el administrador del modelo costos y su administrador
class costAdmin(admin.ModelAdmin):
	list_display       = ('category','cost','order','status')
	list_display_links = ('cost','order','category')
	list_filter        = ('category','status','cost',)
	ordering           = ('-status','order','cost')
	search_fields      = ('cost',)

admin.site.register(cost,costAdmin)