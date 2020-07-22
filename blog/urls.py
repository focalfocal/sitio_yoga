from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'),

    path('post/new/', views.post_new, name='post_new'),
    #path('post/<#int:pk#>/', views.post_detail, name='post_detail'),
    path('post/<slug:slug>/', views.post_detail, name='post_detail'),
    
    #path('post/new/', views.post_new, name='post_new'),
    #path('post/<#int:pk#>/edit/', views.post_edit, name='post_edit'),
    path('post/<slug:slug>/edit/', views.post_edit, name='post_edit'),

    #Eliminar add_comment_to_post luego de unificar pagina
    #path('post/<#int:pk#>/comment/', views.add_comment_to_post, name='add_comment_to_post'),

    path('comment/<int:pk>/approve/', views.comment_approve, name='comment_approve'),
	path('comment/<int:pk>/remove/', views.comment_remove, name='comment_remove'),

	path('tags/<slug:slug>/', views.tags_list, name='tags_list'\
),
]