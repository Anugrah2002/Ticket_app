from django import forms

from .models import Branch


class BranchForm(forms.ModelForm):
    class Meta:
        model = Branch
        fields = "__all__"
        widgets = {
            'branch_name': forms.DateInput(attrs={'placeholder': 'Branch Name'}),
            'branch_code': forms.DateInput(attrs={'placeholder': 'Branch Code (3 Letters Only)'}),
        }

    def clean_branch_code(self):
        return self.cleaned_data["branch_code"].upper()
