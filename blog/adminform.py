from django import forms

class PostAdminForm(forms.ModelForm):
    decs = forms.CharField(widget=forms.Textarea, label='摘要', required=False)