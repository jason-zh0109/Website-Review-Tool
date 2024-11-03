from django.urls import path
from search_link import views

urlpatterns = [
    path('', views.search_link, name='search_link'),  # Search page
    path('download/', views.download, name='download'),
    path('show_results/', views.show_results, name='show_results')
]