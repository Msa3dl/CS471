from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q, Count, Sum, Avg, Max, Min
from .models import Book, Card, Department, Course, Student, Student11, Address11, Student12, Address12, Product11
from .forms import BookForm, Student11Form, Student12Form, Product11Form
from django.contrib.auth.decorators import login_required
def index(request):
    return render(request, "bookmodule/index.html")


def list_books(request):
    return render(request, "bookmodule/list_books.html")


def viewbook(request, bookId):
    return render(request, "bookmodule/one_book.html")


def aboutus(request):
    return render(request, "bookmodule/aboutus.html")

def links(request):
    return render(request, "bookmodule/links.html")

def formatting(request):
    return render(request, "bookmodule/formatting.html")

def listing(request):
    return render(request, "bookmodule/listing.html")

def tables(request):
    return render(request, "bookmodule/tables.html")
def __getBooksList():
    book1 = {
        'id': 12344321,
        'title': 'Continuous Delivery',
        'author': 'J.Humble and D. Farley'
    }

    book2 = {
        'id': 56788765,
        'title': 'Reversing: Secrets of Reverse Engineering',
        'author': 'E. Eilam'
    }

    book3 = {
        'id': 43211234,
        'title': 'The Hundred-Page Machine Learning Book',
        'author': 'Andriy Burkov'
    }

    return [book1, book2, book3]


def search(request):
    if request.method == "POST":
        string = request.POST.get('keyword', '').lower()
        isTitle = request.POST.get('option1')
        isAuthor = request.POST.get('option2')

        books = __getBooksList()
        newBooks = []

        for item in books:
            contained = False

            if isTitle and string in item['title'].lower():
                contained = True

            if not contained and isAuthor and string in item['author'].lower():
                contained = True

            if contained:
                newBooks.append(item)

        return render(
            request,
            'bookmodule/bookList.html',
            {'books': newBooks}
        )

    return render(request, 'bookmodule/search.html')

def simple_query(request):
    mybooks = Book.objects.filter(title__icontains='and')
    return render(request, 'bookmodule/bookList.html', {'books': mybooks})


def complex_query(request):
    mybooks = (
        Book.objects
        .filter(author__isnull=False)
        .filter(title__icontains='and')
        .filter(edition__gte=2)
        .exclude(price__lte=100)[:10]
    )

    if len(mybooks) >= 1:
        return render(request, 'bookmodule/bookList.html', {'books': mybooks})

    return render(request, 'bookmodule/index.html')

def lab8_task1(request):
    books = Book.objects.filter(Q(price__lte=80))
    return render(request, 'bookmodule/bookList.html', {'books': books})


def lab8_task2(request):
    books = Book.objects.filter(
        Q(edition__gt=3) &
        (Q(title__icontains='co') | Q(author__icontains='co'))
    )
    return render(request, 'bookmodule/bookList.html', {'books': books})


def lab8_task3(request):
    books = Book.objects.filter(
        ~Q(edition__gt=3) &
        ~Q(title__icontains='co') &
        ~Q(author__icontains='co')
    )
    return render(request, 'bookmodule/bookList.html', {'books': books})


def lab8_task4(request):
    books = Book.objects.order_by('title')
    return render(request, 'bookmodule/bookList.html', {'books': books})


def lab8_task5(request):
    statistics = Book.objects.aggregate(
        number_of_books=Count('id'),
        total_price=Sum('price'),
        average_price=Avg('price'),
        maximum_price=Max('price'),
        minimum_price=Min('price'),
    )

    return render(
        request,
        'bookmodule/bookStatistics.html',
        {'statistics': statistics}
    )
def students_per_city(request):
    cities = Address.objects.annotate(
        student_count=Count('students')
    )

    return render(
        request,
        'bookmodule/studentsPerCity.html',
        {'cities': cities}
    )
def lab9_task1(request):
    departments = Department.objects.annotate(
        student_count=Count('students')
    )
    return render(
        request,
        'bookmodule/lab9_task1.html',
        {'departments': departments}
    )


def lab9_task2(request):
    courses = Course.objects.annotate(
        student_count=Count('students')
    )
    return render(
        request,
        'bookmodule/lab9_task2.html',
        {'courses': courses}
    )


def lab9_task3(request):
    departments = Department.objects.prefetch_related('students')

    results = []
    for department in departments:
        oldest_student = department.students.order_by('id').first()
        results.append({
            'department': department,
            'oldest_student': oldest_student
        })

    return render(
        request,
        'bookmodule/lab9_task3.html',
        {'results': results}
    )


def lab9_task4(request):
    departments = (
        Department.objects
        .annotate(student_count=Count('students'))
        .filter(student_count__gt=2)
        .order_by('-student_count')
    )

    return render(
        request,
        'bookmodule/lab9_task4.html',
        {'departments': departments}
    )
def lab10_part1_listbooks(request):
    books = Book.objects.all()
    return render(
        request,
        'bookmodule/lab10_part1_listbooks.html',
        {'books': books}
    )


def lab10_part1_addbook(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        author = request.POST.get('author')
        price = request.POST.get('price')
        edition = request.POST.get('edition')

        Book.objects.create(
            title=title,
            author=author,
            price=price,
            edition=edition
        )

        return redirect('books.lab10_part1_listbooks')

    return render(request, 'bookmodule/lab10_part1_form.html')


def lab10_part1_editbook(request, id):
    book = get_object_or_404(Book, id=id)

    if request.method == 'POST':
        book.title = request.POST.get('title')
        book.author = request.POST.get('author')
        book.price = request.POST.get('price')
        book.edition = request.POST.get('edition')
        book.save()

        return redirect('books.lab10_part1_listbooks')

    return render(
        request,
        'bookmodule/lab10_part1_form.html',
        {'book': book}
    )


def lab10_part1_deletebook(request, id):
    book = get_object_or_404(Book, id=id)
    book.delete()
    return redirect('books.lab10_part1_listbooks')

def lab10_part2_listbooks(request):
    books = Book.objects.all()
    return render(
        request,
        'bookmodule/lab10_part2_listbooks.html',
        {'books': books}
    )


def lab10_part2_addbook(request):
    if request.method == 'POST':
        form = BookForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('books.lab10_part2_listbooks')
    else:
        form = BookForm()

    return render(
        request,
        'bookmodule/lab10_part2_form.html',
        {'form': form}
    )


def lab10_part2_editbook(request, id):
    book = get_object_or_404(Book, id=id)

    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)

        if form.is_valid():
            form.save()
            return redirect('books.lab10_part2_listbooks')
    else:
        form = BookForm(instance=book)

    return render(
        request,
        'bookmodule/lab10_part2_form.html',
        {'form': form, 'book': book}
    )


def lab10_part2_deletebook(request, id):
    book = get_object_or_404(Book, id=id)
    book.delete()
    return redirect('books.lab10_part2_listbooks')


@login_required(login_url='/users/login')
def lab11_task1_list(request):
    students = Student11.objects.all()
    return render(
        request,
        'bookmodule/lab11_task1_list.html',
        {'students': students}
    )

@login_required(login_url='/users/login')
def lab11_task1_add(request):
    if request.method == 'POST':
        form = Student11Form(request.POST)

        if form.is_valid():
            form.save()
            return redirect('books.lab11_task1_list')
    else:
        form = Student11Form()

    return render(
        request,
        'bookmodule/lab11_task1_form.html',
        {'form': form}
    )

@login_required(login_url='/users/login')
def lab11_task1_edit(request, id):
    student = get_object_or_404(Student11, id=id)

    if request.method == 'POST':
        form = Student11Form(request.POST, instance=student)

        if form.is_valid():
            form.save()
            return redirect('books.lab11_task1_list')
    else:
        form = Student11Form(instance=student)

    return render(
        request,
        'bookmodule/lab11_task1_form.html',
        {'form': form, 'student': student}
    )

@login_required(login_url='/users/login')
def lab11_task1_delete(request, id):
    student = get_object_or_404(Student11, id=id)
    student.delete()

    return redirect('books.lab11_task1_list')

@login_required(login_url='/users/login')
def lab11_task2_list(request):
    students = Student12.objects.all()
    return render(
        request,
        'bookmodule/lab11_task2_list.html',
        {'students': students}
    )

@login_required(login_url='/users/login')
def lab11_task2_add(request):
    if request.method == 'POST':
        form = Student12Form(request.POST)

        if form.is_valid():
            form.save()
            return redirect('books.lab11_task2_list')
    else:
        form = Student12Form()

    return render(
        request,
        'bookmodule/lab11_task2_form.html',
        {'form': form}
    )

@login_required(login_url='/users/login')
def lab11_task2_edit(request, id):
    student = get_object_or_404(Student12, id=id)

    if request.method == 'POST':
        form = Student12Form(request.POST, instance=student)

        if form.is_valid():
            form.save()
            return redirect('books.lab11_task2_list')
    else:
        form = Student12Form(instance=student)

    return render(
        request,
        'bookmodule/lab11_task2_form.html',
        {'form': form, 'student': student}
    )

@login_required(login_url='/users/login')
def lab11_task2_delete(request, id):
    student = get_object_or_404(Student12, id=id)
    student.delete()

    return redirect('books.lab11_task2_list')

@login_required(login_url='/users/login')
def lab11_task3_list(request):
    products = Product11.objects.all()
    return render(
        request,
        'bookmodule/lab11_task3_list.html',
        {'products': products}
    )

@login_required(login_url='/users/login')
def lab11_task3_add(request):
    if request.method == 'POST':
        form = Product11Form(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect('books.lab11_task3_list')
    else:
        form = Product11Form()

    return render(
        request,
        'bookmodule/lab11_task3_form.html',
        {'form': form}
    )

@login_required(login_url='/users/login')
def lab11_task3_edit(request, id):
    product = get_object_or_404(Product11, id=id)

    if request.method == 'POST':
        form = Product11Form(
            request.POST,
            request.FILES,
            instance=product
        )

        if form.is_valid():
            form.save()
            return redirect('books.lab11_task3_list')
    else:
        form = Product11Form(instance=product)

    return render(
        request,
        'bookmodule/lab11_task3_form.html',
        {'form': form, 'product': product}
    )

@login_required(login_url='/users/login')
def lab11_task3_delete(request, id):
    product = get_object_or_404(Product11, id=id)
    product.delete()

    return redirect('books.lab11_task3_list')