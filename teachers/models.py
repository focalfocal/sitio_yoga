from django.conf import settings
from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.utils.text import slugify

class Tag(models.Model):
    title = models.CharField(max_length=255, default='')
    slug = models.SlugField(blank=True, default='', unique=True, allow_unicode=True, max_length=255)
    
    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Tag, self).save()

    #Get tag_title based on tag
    def get_tag_title(self):
        return reverse('post_detail', args=[str(self.slug)])

class Teacher(models.Model):
    title = models.CharField(max_length=200, verbose_name='nombre')
    thumbnail = models.ImageField(default='', blank=True, upload_to='teach_thumbnails')
    image = models.ImageField(default='', blank=True, upload_to='teach_images')
    text = models.TextField(verbose_name='texto')
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(default=timezone.now)
    slug = models.SlugField(blank=True, default='')
    #yoga styles
    tags = models.ManyToManyField(Tag, blank=True)
    #locations = models.ManyToManyField(Location, blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Teacher, self).save()

    #def publish(self):
    #    self.published_date = timezone.now()
    #    self.save()

    def __str__(self):
        return self.title

    #'View on site' for the admin. Generates slug path
    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.slug)])