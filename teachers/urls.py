from django.urls import path
from . import views
#For images:
from django.conf import settings
from django.conf.urls.static import static
#For authentication - Allauth
from django.urls import path, include

urlpatterns = [
    #path('', views.post_list, name='post_list'),
    path('teachers/', views.teacher_list, name='teacher_list'),

    #path('post/new/', views.post_new, name='post_new'),

    path('teachers/<slug:slug>/', views.teacher_detail, name='teacher_detail'),
    
    #path('post/<slug:slug>/edit/', views.post_edit, name='post_edit'),

    #path('comment/<int:pk>/approve/', views.comment_approve, name='comment_approve'),

	#path('comment/<int:pk>/remove/', views.comment_remove, name='comment_remove'),

	path('teachers_tags/<slug:slug>/', views.teacher_tags_list, name='teacher_tags_list'),

    #path('accounts/', include('allauth.urls')),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)