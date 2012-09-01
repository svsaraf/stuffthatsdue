from django.contrib import admin
from app.models import UserProfile, PatelActivity, LeungActivity, StropleActivity, SchaeferActivity

admin.site.register(UserProfile)
admin.site.register(PatelActivity)
admin.site.register(LeungActivity)
admin.site.register(StropleActivity)
admin.site.register(SchaeferActivity)