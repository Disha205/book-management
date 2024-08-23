from django import forms

class ExcelUploadForm(forms.Form):
    FILE_TYPE_CHOICES = [
        ('book', 'Book'),
        ('author', 'Author'),
    ]
    file_type = forms.ChoiceField(choices=FILE_TYPE_CHOICES, label="Select file type")
    excel_file = forms.FileField(label="Upload Excel File")
