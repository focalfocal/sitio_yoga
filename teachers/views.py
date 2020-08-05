from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Teacher, Tag
#from .forms import PostForm, CommentForm
import json
import urllib
from django.conf import settings
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
#from django.db.models import Q
from django.contrib.auth.decorators import permission_required

#Auxiliary to paginate teachers lists
#def paginate_teacher_list(request, object_list, tag_title, search_string):
# def paginate_teacher_list(request, object_list, tag_title):
#     #Do not change object_list name as causes paginator to fail
#     paginator = Paginator(object_list, 10) # posts in each page
#     page = request.GET.get('page')
#     try:
#         teachers = paginator.page(page)
#     except PageNotAnInteger:
#     # If page is not an integer deliver the first page
#         teachers = paginator.page(1)
#     except EmptyPage:
#     # If page is out of range deliver last page of results
#         teachers = paginator.page(paginator.num_pages)
#     return render(request,
#         'teachers/teacher_list.html',
#         {'page': page,
#         'teachers': teachers,
#         'tag_title' : tag_title})

#Lists all the teachers
def teacher_list(request):
    # search_string = request.GET.get('search_string', None)
    
    # if search_string == None or search_string == "":
        #No cambiar el nombre a object_list porque falla paginator
        #object_list = Teacher.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    object_list = Teacher.objects.all().order_by('published_date')
    # elif search_string != None:
    #     object_list = Post.objects             \
    #         .filter(published_date__lte=timezone.now())    \
    #         .filter(
    #             Q(title__icontains = search_string) | Q(text__icontains = search_string))\
    #         .order_by('published_date')

    #return paginate_teacher_list(request, object_list, tag_title=None)
    tag_title=None
    return render(request,
        'teachers/teacher_list.html',
        {'teachers': object_list,
        'tag_title' : tag_title})

#Show a single post
def teacher_detail(request, slug=None):
    teacher = get_object_or_404(Teacher, slug=slug)

    # If form submited by post, process form:
    # if request.method == "POST":
    #     form = CommentForm(request.POST)
    #     if form.is_valid():
    #         #Begin reCAPTCHA validation
    #         recaptcha_response = request.POST.get('g-recaptcha-response')
    #         url = 'https://www.google.com/recaptcha/api/siteverify'
    #         values = {
    #             'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
    #             'response': recaptcha_response
    #         }
    #         data = urllib.parse.urlencode(values).encode()
    #         req =  urllib.request.Request(url, data=data)
    #         response = urllib.request.urlopen(req)
    #         result = json.loads(response.read().decode())
    #         #End reCAPTCHA validation

    #         if result['success']:

    #             comment = form.save(commit=False)
    #             comment.post = post
    #             comment.save()
    #             messages.success(request, '¡Se envió exitosamente el comentario para aprobación!')
    #         else:
    #             messages.error(request, 'reCAPTCHA inválido. Por favor intente nuevamente.')

    #         return redirect('post_detail', slug=post.slug)

    # #If page requested by GET: load blank form        
    # else:
    #     form = CommentForm()

    #return render(request, 'blog/post_detail.html', {'post': post, 'form': form})
    return render(request, 'teachers/teacher_detail.html', {'teacher': teacher})

# @permission_required('blog.add_post')
# def post_new(request):
#     if request.method == "POST":
#         #form = PostForm(request.POST)
#         form = PostForm(request.POST, request.FILES)
#         if form.is_valid():
#             post = form.save(commit=False)
#             post.author = request.user
#             post.published_date = timezone.now()
#             #debugging
#             #print("url= ", post.image.url)
#             #print("url= ", post.image.path)
#             post.save()
#             return redirect('post_detail', slug=post.slug)
            
#     else:
#         #Use form defined on forms.py
#         form = PostForm()
#     return render(request, 'blog/post_edit.html', {'form': form})

# @permission_required('blog.change_post')
# def post_edit(request, slug):
#     post = get_object_or_404(Post, slug=slug)
#     if request.method == "POST":
#         #form = PostForm(request.POST, instance=post)
#         #form = PostForm(data=request.POST, files=request.FILES, instance=post)
#         form = PostForm(request.POST, request.FILES, instance=post)
#         if form.is_valid():
#             post = form.save(commit=False)
#             post.author = request.user
#             post.published_date = timezone.now()
#             #debugging
#             #print("url= ", post.image.url)
#             #print("url= ", post.image.path)
#             post.save()
#             return redirect('post_detail', slug=post.slug)
#     else:
#         form = PostForm(instance=post)
#     return render(request, 'blog/post_edit.html', {'form': form})

# @permission_required('blog.change_comment')
# def comment_approve(request, pk):
#     comment = get_object_or_404(Comment, pk=pk)
#     comment.approve()
#     return redirect('post_detail', slug=comment.post.slug)

# @permission_required('blog.delete_comment')
# def comment_remove(request, pk):
#     comment = get_object_or_404(Comment, pk=pk)
#     comment.delete()
#     return redirect('post_detail', slug=comment.post.slug)

#Shows tag filtered posts
def teacher_tags_list(request, slug=None):
    tag = None
    tag = get_object_or_404(Tag, slug=slug)
    
    object_list = Teacher.objects.all().order_by('published_date')
    object_list = object_list.filter(tags__in=[tag]) #kept separate to facilitate refactoring
    tag_title = str(tag)
    #return paginate_post_list(request, object_list, tag_title, search_string=None)
    return render(request,
        'teachers/teacher_list.html',
        {'teachers': object_list,
        'tag_title' : tag_title})

