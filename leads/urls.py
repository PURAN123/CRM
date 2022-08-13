from django.urls import path
from leads.views import list_leads,lead_detail, create_lead,lead_update,lead_delete

app_name = "leads"

urlpatterns = [
    path("", list_leads, name= "lead-list"),
    path("create/", create_lead, name="lead-create"),
    path("<int:pk>/details/", lead_detail, name="lead-detail"),
    path("<int:pk>/update/", lead_update, name="lead-update"),
    path("<int:pk>/delete/", lead_delete, name="lead-delete"),
]
