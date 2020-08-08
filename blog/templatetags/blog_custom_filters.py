from django import template
from django.core.files.storage import default_storage

#Register your filter with your Library instance, to make it available to Django’s template language
register = template.Library()

#Custom filter to check if file exists
@register.filter(name='file_exists')
def file_exists(filepath):
    if default_storage.exists(filepath):
        return filepath
    else:
        #index = filepath.rfind('/')
        #new_filepath = filepath[:index] + '/image.png'
        new_filepath = '/media/images/Mata_mua-Paul_Gauguin.jpg'
        return new_filepath

