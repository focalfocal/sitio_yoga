from django.urls import path
from . import views
#For images:
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('teachers/', views.teacher_list, name='teacher_list'),

    path('teachers/<slug:slug>/', views.teacher_detail, name='teacher_detail'),

	path('teachers_tags/<slug:slug>/', views.teacher_tags_list, name='teacher_tags_list'),
    
]
