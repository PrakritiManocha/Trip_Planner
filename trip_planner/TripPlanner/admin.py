from django.contrib import admin
from .models import Plan,Location,TripPlan,Participant,Event,PlanSelection,Expenditure,ExpenditureSplit

admin.site.register(Location)
admin.site.register(TripPlan)
admin.site.register(Participant)
admin.site.register(Event)
admin.site.register(PlanSelection)
admin.site.register(Expenditure)
admin.site.register(ExpenditureSplit)


class PlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'trip_plan')  
admin.site.register(Plan, PlanAdmin)
