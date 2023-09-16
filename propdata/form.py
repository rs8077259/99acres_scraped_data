from django import forms

class PropertyFilterForm(forms.Form):
    property_data = forms.CharField(label='Property city Name', max_length=100)
