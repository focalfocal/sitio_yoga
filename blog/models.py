from django.conf import settings
from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.utils.text import slugify

# Create your models here.
class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    slug = models.SlugField(blank=True, default='')

    def publish(self):
        self.published_date = timezone.now()
        #Agregada 1 linea para slug, siguiendo Easy2. Pero no anda.
        #self.slug = slugify(self.title)
        self.save()

    def __str__(self):
        return self.title

    #Agregado para slug, siguiendo Easy2
    #Conviene separado de publish, para cuando haga drafts.
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Post, self).save()

    #Para uso con slug , al reves.
    def get_absolute_url(self):
        return reverse('detail', args=[str(self.slug)])

class Comment(models.Model):
    post = models.ForeignKey('blog.Post', on_delete=models.CASCADE, related_name='comments')
    author = models.CharField(max_length=200)
    text = models.TextField()
    email = models.CharField(max_length=250, blank=True)
    web_site = models.CharField(max_length=250, blank=True)
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.text