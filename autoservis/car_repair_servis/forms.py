from django import forms
from . import models

class DateInput(forms.DateInput):
    input_type = 'date'

class OrderReviewForm(forms.ModelForm):
    class Meta:
        model = models.OrderReview
        fields = ('order', 'reviewer', 'content')
        widgets = {'order': forms.HiddenInput(), 'reviewer': forms.HiddenInput()}

class UserOrderCreateForm(forms.ModelForm):
    class Meta:
        model = models.Order
        fields = ('car', 'date_finish', 'status')
        widgets = {
            'date_finish': DateInput(),
            'status': forms.HiddenInput(),
        }

class UserOrderUpdateForm(forms.ModelForm):
    class Meta:
        model = models.Order
        fields = ('car', 'status')
        widgets = {'status': forms.HiddenInput(), }
