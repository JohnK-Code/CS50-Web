from django import forms

# form for creating post
class NewPost(forms.Form):
    content = forms.CharField(label="", max_length=140, widget=forms.TextInput(attrs={'placeholder':"What's happening?", 'autofocus': True}))
