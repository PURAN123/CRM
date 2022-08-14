
from django.contrib import admin
from leads.models import User, Agent, Lead, UserProfile
# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display =["username","email","id"]

@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display =["first_name","last_name","age","id"]

@admin.register(Agent)
class AgentAdmin(admin.ModelAdmin):
    list_display =["user","id"]
    
@admin.register(UserProfile)
class USerProfileAdmin(admin.ModelAdmin):
    list_display =["user","id"]