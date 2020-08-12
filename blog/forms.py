from django import forms
from .models import Post, Comment
#from cloudinary.forms import CloudinaryFileField
#from cloudinary.models import CloudinaryField falla inicializ.

#reference: https://cloudinary.com/documentation/image_upload_api_reference#upload_method
class PostForm(forms.ModelForm):
    # image = CloudinaryFileField(
    #     options = {
    #         #'folder': 'yoga_site/post_image',
    #         'folder': 'yoga_site',
    #         'use_filename' : True
    #    	}
    # )

    class Meta:
        model = Post
        fields = ('title', 'text', 'image',)

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('author', 'email', 'web_site', 'text',)