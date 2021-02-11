from django import forms

# form for creating post
class NewPost(forms.Form):
    content = forms.CharField(label="New Post", max_length=140)
