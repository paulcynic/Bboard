from django.urls import path
from .views import index, BbByRubricView, BbDetailView, BbAddView, edit, BbDeleteView, BbRedirectView, pass_form


urlpatterns = [
    #path('<int:rubric_id>/', by_rubric, name='by_rubric'),
    path('<int:rubric_id>/', BbByRubricView.as_view(), name='by_rubric'),
    # path('detail/<int:pk>/', BbDetailView.as_view(), name='detail'),
    path('detail/<int:pk>/', BbDetailView.as_view(), name='detail'),
    path('detail/<int:pk>/', BbRedirectView.as_view(), name='old_detail'),
    path('', index, name='index'),
    #path('add/', BbCreateView.as_view(), name='add'),
    path('add/', BbAddView.as_view(), name='add'),
    path('edit/<int:pk>/', edit, name='edit'),
    path('delete/<int:pk>/', BbDeleteView.as_view(), name='delete'),
    path('login/', pass_form, name='login'),
    #path('set_form/<int:rubric_id>/', bbs, name='setform'),
]
