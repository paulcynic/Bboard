from django.urls import path
from .views import index, by_rubric, BbCreateView, add_and_save

urlpatterns = [
    path('<int:rubric_id>/', by_rubric, name='by_rubric'),
    path('', index, name='index'),
    #path('add/', BbCreateView.as_view(), name='add'),
    path('add/', add_and_save, name='add'),
]
