from django.shortcuts import render, redirect
from .forms import ExcelUploadForm
from .models import Author, Book
import pandas as pd

def upload_excel(request):
    if request.method == 'POST':
        form = ExcelUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file_type = form.cleaned_data['file_type']
            excel_file = request.FILES['excel_file']

            df = pd.read_excel(excel_file)

            if file_type == 'book':
                required_columns = {'Name', 'ISBN Code', 'Author Id'}
                if not required_columns.issubset(df.columns):
                    return render(request, 'books/upload.html', {
                        'form': form,
                        'error': 'Invalid file format for Book. Required columns: Name, ISBN Code, Author Id'
                    })
            elif file_type == 'author':
                required_columns = {'Name', 'Email', 'Date of Birth'}
                if not required_columns.issubset(df.columns):
                    return render(request, 'books/upload.html', {
                        'form': form,
                        'error': 'Invalid file format for Author. Required columns: Name, Email, Date of Birth'
                    })

            request.session['file_type'] = file_type
            request.session['excel_data'] = df.to_dict('records')
            return redirect('books:preview_excel')

    else:
        form = ExcelUploadForm()

    return render(request, 'books/upload.html', {'form': form})

def preview_excel(request):
    if 'excel_data' not in request.session or 'file_type' not in request.session:
        return redirect('books:upload_excel')

    excel_data = request.session['excel_data']
    file_type = request.session['file_type']
    return render(request, 'books/preview.html', {'excel_data': excel_data, 'file_type': file_type})

def save_excel_data(request):
    if 'excel_data' not in request.session or 'file_type' not in request.session:
        return redirect('books:upload_excel')

    excel_data = request.session['excel_data']
    file_type = request.session['file_type']

    if file_type == 'book':
        for row in excel_data:
            author = Author.objects.get(id=row['Author Id'])
            Book.objects.create(
                name=row['Name'],
                isbn_code=row['ISBN Code'],
                author=author
            )
    elif file_type == 'author':
        for row in excel_data:
            Author.objects.create(
                name=row['Name'],
                email=row['Email'],
                date_of_birth=row['Date of Birth']
            )

    # Clear session after saving
    del request.session['excel_data']
    del request.session['file_type']
    return redirect('books:upload_excel')


def view_books(request):
    books = Book.objects.all()
    return render(request, 'books/view_books.html', {'books': books})

def view_authors(request):
    authors = Author.objects.all()
    return render(request, 'books/view_authors.html', {'authors': authors})
