from django import forms
from .models import Book


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'price', 'edition']
from .models import Student11, Address11, Student12, Address12, Product11

class Student11Form(forms.ModelForm):
    class Meta:
        model = Student11
        fields = ['name', 'address']
class Student12Form(forms.ModelForm):
    class Meta:
        model = Student12
        fields = ['name', 'addresses']
        widgets = {
            'addresses': forms.CheckboxSelectMultiple()
        }
class Product11Form(forms.ModelForm):
    class Meta:
        model = Product11
        fields = ['name', 'image']