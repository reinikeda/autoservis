from django import forms
from . import models


class OrderReviewForm(forms.ModelForm):
    class Meta:
        model = models.OrderReview
        fields = ('order', 'reviewer', 'content')
        widgets = {'order': forms.HiddenInput(), 'reviewer': forms.HiddenInput()}
