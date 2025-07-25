from django.forms import forms


class Exampleform(forms.Form):
    query = forms.CharField(max_length=100, label="Search")
