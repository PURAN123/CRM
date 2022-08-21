from django.urls import path
from leads.views import ( list_leads,lead_detail, create_lead,lead_update,lead_delete,
                        LeadListView, LeadDetailView, LeadCreateView, LeadUpdateView, LeadDeleteView, AssignAgentView, CategoryListView, CategoryDetailView, CategoryUpdateView, CategoryCreateView, CategoryUpdateViewCategory,CategoryDeleteViewCategory
)

app_name = "leads"

urlpatterns = [
    path("", LeadListView.as_view(), name= "lead-list"),
    path("create/", LeadCreateView.as_view(), name="lead-create"),
    path("<int:pk>/details/", LeadDetailView.as_view(), name="lead-detail"),
    path("<int:pk>/update/", LeadUpdateView.as_view(), name="lead-update"),
    path("<int:pk>/delete/", LeadDeleteView.as_view(), name="lead-delete"),
    path("<int:pk>/assign-agent/", AssignAgentView.as_view(), name= "assign-agent"),
    path("categories/", CategoryListView.as_view(), name= "category-list"),
    path("category/<int:pk>/details/", CategoryDetailView.as_view(), name= "category-detail"),
    path("lead-category/<int:pk>/update/", CategoryUpdateView.as_view(), name= "category-update"),
    path("category/create/", CategoryCreateView.as_view(), name= "category-create"),
    path("category/<int:pk>/update/", CategoryUpdateViewCategory.as_view(), name= "category-update-category"),
    path("category/<int:pk>/delete/", CategoryDeleteViewCategory.as_view(), name= "category-delete-category")
]
