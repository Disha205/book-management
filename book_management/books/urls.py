from django.urls import path
from . import views

app_name = 'books'

urlpatterns = [
    path('upload/', views.upload_excel, name='upload_excel'),
    path('preview/', views.preview_excel, name='preview_excel'),
    path('save/', views.save_excel_data, name='save_excel_data'),
    path('view/books/', views.view_books, name='view_books'),
    path('view/authors/', views.view_authors, name='view_authors'),
]
