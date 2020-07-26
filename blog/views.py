from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Post, Comment, Tag
from .forms import PostForm, CommentForm
import json
import urllib
from django.conf import settings
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def paginate_post_list(request, object_list, tag_title):
    #No cambiar el nombre a object_list porque falla
    paginator = Paginator(object_list, 2) # 2 posts in each page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
    # If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
    # If page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)
    return render(request,
        'blog/post_list.html',
        {'page': page,
        'posts': posts,
        'tag_title' : tag_title})

def post_list(request):
     #No cambiar el nombre a object_list porque falla paginator
    object_list = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    # paginator = Paginator(object_list, 2) # 2 posts in each page
    # page = request.GET.get('page')
    # try:
    #     posts = paginator.page(page)
    # except PageNotAnInteger:
    # # If page is not an integer deliver the first page
    #     posts = paginator.page(1)
    # except EmptyPage:
    # # If page is out of range deliver last page of results
    #     posts = paginator.page(paginator.num_pages)
    # return render(request,
    #     'blog/post_list.html',
    #     {'page': page,
    #     'posts': posts})
    #tag_slug = None #usado solo al filtrar por tag
    return paginate_post_list(request, object_list, None)


def post_detail(request, slug=None):
    post = get_object_or_404(Post, slug=slug)

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

            return redirect('post_detail', slug=post.slug)

    #Si se pidio la pagina por GET: cargar formulario en blanco        
    else:
        form = CommentForm()

    return render(request, 'blog/post_detail.html', {'post': post, 'form': form})

def post_new(request):
    print("entro a la funcion post_new")
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', slug=post.slug)
            
    else:
        #print("paso por el else")
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})

def post_edit(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', slug=post.slug)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})

#@login_required
#Pendiente tener esquema de seguridad. @login_required es un decorator que viene de "from django.contrib.auth.decorators import login_required"
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('post_detail', slug=comment.post.slug)

#@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return redirect('post_detail', slug=comment.post.slug)

#Muestra posts filtrados por un tag
def tags_list(request, slug=None):
    tag = None
    tag = get_object_or_404(Tag, slug=slug)
    
    object_list = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    object_list = object_list.filter(tags__in=[tag]) #separado para facilitar refactoring

    return paginate_post_list(request, object_list, str(tag))

