from django.conf import settings
from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.utils.text import slugify

class Tag(models.Model):
    title = models.CharField(max_length=255, default='')
    slug = models.SlugField(blank=True, default='')
    
    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        #Pending to add argument: allow_unicode=True
        self.slug = slugify(self.title)
        super(Tag, self).save()

    #Get tag_title based on tag
    def get_tag_title(self):
        return reverse('post_detail', args=[str(self.slug)])

class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, verbose_name='titulo')
    image = models.ImageField(default='', blank=True, upload_to='images')
    text = models.TextField(verbose_name='texto')
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    #slug = models.SlugField(max_length=250, unique_for_date='publish') 
    slug = models.SlugField(blank=True, default='')
    tags = models.ManyToManyField(Tag, blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        #debugging
        #print("url= ", self.image.url)
        #print("path= ", self.image.path)
        super(Post, self).save()

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

    #'View on site' for the admin. Generates slug path
    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.slug)])

class Comment(models.Model):
    post = models.ForeignKey('blog.Post', on_delete=models.CASCADE, related_name='comments')
    author = models.CharField(max_length=200, verbose_name='autor')
    text = models.TextField(verbose_name='texto')
    email = models.CharField(max_length=250, blank=True)
    web_site = models.CharField(max_length=250, blank=True, verbose_name='sitio web')
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.text

