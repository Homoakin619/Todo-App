from operator import imod
from django import forms
from ckeditor.widgets import CKEditorWidget
from django.contrib.admin.widgets import AdminDateWidget

from .models import Todo

class AddTodoForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    description = forms.CharField(widget=CKEditorWidget())
    done = forms.BooleanField(required=False,widget=forms.CheckboxInput(attrs={'class':'form-check-input','id':"flexCheckDefault"}))
    date = forms.DateField(widget=forms.DateInput(attrs={'id':'datepicker','class':'form-control'}))
    
    class Meta:
        model = Todo
        fields = ('title','description','done','date')