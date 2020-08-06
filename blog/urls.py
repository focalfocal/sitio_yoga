from django.urls import path
from . import views
#For images:
from django.conf import settings
from django.conf.urls.static import static
#For authentication - Allauth
from django.urls import include

urlpatterns = [
	path('', views.home, name='home'),

    path('post/', views.post_list, name='post_list'),

    path('post/new/', views.post_new, name='post_new'),

    path('post/<slug:slug>/', views.post_detail, name='post_detail'),
    
    path('post/<slug:slug>/edit/', views.post_edit, name='post_edit'),

    path('comment/<int:pk>/approve/', views.comment_approve, name='comment_approve'),

	path('comment/<int:pk>/remove/', views.comment_remove, name='comment_remove'),

	path('tags/<slug:slug>/', views.tags_list, name='tags_list'),

    path('accounts/', include('allauth.urls')),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)