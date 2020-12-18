from django import forms
import datetime

# used to provde category options for listings
CATEGORY = [
    ('Modern', 'Modern'),
    ('Classic', 'Classic'),
    ('American', 'American')
]

# to get a range of years for form 
YEAR_CHOICES = []
for r in range(1900, (datetime.datetime.now().year+1)):
    YEAR_CHOICES.append((r,r))

# model choices
MODEL_CHOICES = [
    ('Audi', 'Audi'),
    ('BMW', 'BMW'),
    ('Citroen', 'Citroen'),
    ('Datsun', 'Datsun'),
    ('Enfield', 'Enfield'),
    ('Ford', 'Ford')
]

# form for creating new lisitng
class NewListingForm(forms.Form):
    category = forms.ChoiceField(choices=CATEGORY)
    title = forms.CharField(label='Title', max_length=100)
    make = forms.ChoiceField(label="Make", choices=MODEL_CHOICES)
    model = forms.CharField(label="Model", max_length=20)
    year = forms.ChoiceField(choices=YEAR_CHOICES, initial=2020, label="Year")
    description = forms.CharField(label="Description", widget=forms.Textarea(attrs={"rows":5, "cols":30}))
    image = forms.ImageField(required=False) # allows images to be uploaded using form, can be left empty though
    # user info added in model 
    startBid = forms.IntegerField(max_value=10000000, min_value=0)
    # starttime inputed by django
    # endtime inputed by django - hopefully
    # active defaults to true 