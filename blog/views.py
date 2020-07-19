from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Post, Comment
from .forms import PostForm, CommentForm
import json
import urllib
from django.conf import settings
from django.contrib import messages

# Create your views here.
def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)

    # Si se envio el formulario con el boton submit, procesar formulario:
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            #Begin reCAPTCHA validation
            recaptcha_response = request.POST.get('g-recaptcha-response')
            url = 'https://www.google.com/recaptcha/api/siteverify'
            values = {
                'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
                'response': recaptcha_response
            }
            data = urllib.parse.urlencode(values).encode()
            req =  urllib.request.Request(url, data=data)
            response = urllib.request.urlopen(req)
            result = json.loads(response.read().decode())
            #End reCAPTCHA validation

            if result['success']:

                comment = form.save(commit=False)
                comment.post = post
                comment.save()
                messages.success(request, '¡Se envió exitosamente el comentario para aprobación!')
            else:
                messages.error(request, 'reCAPTCHA inválido. Por favor intente nuevamente.')

            return redirect('post_detail', pk=post.pk)

    #Si se pidio la pagina por GET: cargar formulario en blanco        
    else:
        form = CommentForm()
        
    #return render(request, 'blog/add_comment_to_post.html', {'form': form})

    return render(request, 'blog/post_detail.html', {'post': post, 'form': form})

def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
            
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})

def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})



# def add_comment_to_post(request, pk):
#     post = get_object_or_404(Post, pk=pk)

#     # Si se envio el formulario con el boton submit, procesar formulario:
#     if request.method == "POST":
#         form = CommentForm(request.POST)
#         if form.is_valid():
#             #Begin reCAPTCHA validation
#             recaptcha_response = request.POST.get('g-recaptcha-response')
#             url = 'https://www.google.com/recaptcha/api/siteverify'
#             values = {
#                 'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
#                 'response': recaptcha_response
#             }
#             data = urllib.parse.urlencode(values).encode()
#             req =  urllib.request.Request(url, data=data)
#             response = urllib.request.urlopen(req)
#             result = json.loads(response.read().decode())
#             #End reCAPTCHA validation

#             if result['success']:

#                 comment = form.save(commit=False)
#                 comment.post = post
#                 comment.save()
#                 messages.success(request, '¡Se agregó exitosamente el comentario!')
#             else:
#                 messages.error(request, 'reCAPTCHA inválido. Por favor intente nuevamente.')

#             return redirect('post_detail', pk=post.pk)

#     #Si se pidio la pagina por GET: cargar formulario en blanco        
#     else:
#         form = CommentForm()

#     return render(request, 'blog/add_comment_to_post.html', {'form': form})

#@login_required
#Pendiente tener esquema de seguridad. @login_required es un decorator que viene de "from django.contrib.auth.decorators import login_required"
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('post_detail', pk=comment.post.pk)

#@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return redirect('post_detail', pk=comment.post.pk)