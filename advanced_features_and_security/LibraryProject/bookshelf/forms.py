from django import forms


class ExampleForm(forms.Form):
    title = forms.CharField(max_length=200)
    author = forms.CharField(max_length=200)
    publication_year = forms.IntegerField(required=False, min_value=0, max_value=9999)

    def clean_publication_year(self):
        y = self.cleaned_data.get('publication_year')
        if y is None:
            return y
        if y < 0:
            raise forms.ValidationError('Publication year must be positive')
        return y
