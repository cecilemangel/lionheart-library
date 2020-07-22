from django.shortcuts import render, get_object_or_404
from .models import Book, Author, Booking, Contact
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .forms import ContactForm, ParagraphErrorList
from django.db import transaction, IntegrityError

def index(request):
    books = Book.objects.all().order_by('-created_at')[:12]
    context = {
        'books': books,
    }
    return render(request, 'store/index.html', context)

def listing(request):
    books_list = Book.objects.all().order_by('title')
    paginator = Paginator(books_list, 9)
    page = request.GET.get('page')

    try:
        books = paginator.page(page)
    except PageNotAnInteger:
        books = paginator.page(1)
    except EmptyPage:
        books =  paginator.page(paginator.num_pages)

    context = {
        'books': books,
        'paginate': True,
    }
    return render(request, 'store/listing.html', context)

def detail(request, book_id):
    book = get_object_or_404(Book, pk=book_id)   
    author_names_list = [author.name for author in book.author.all()]
    author_name = " ".join(author_names_list)
    author_id_list = [str(author.id) for author in book.author.all()]
    author_id = "".join(author_id_list)
    book_available = book.available

    context = {
        'book_title': book.title,
        'author_name': author_name,
        'book_id': book.id,
        'thumbnail': book.picture,
        'synopsis': book.synopsis,
        'author_id' : author_id,
        'book_available' : book_available,
    }
    if request.method == 'POST':
        form = ContactForm(request.POST, error_class=ParagraphErrorList)
        if form.is_valid():
            email = form.cleaned_data['email']
            name = form.cleaned_data['name']

            try:
                with transaction.atomic():
                    contact = Contact.objects.filter(email=email)
                    if not contact.exists():
                        contact = Contact.objects.create(
                            email=email,
                            name=name
                        )
                    else:
                        contact = contact.first()

                    book = get_object_or_404(Book, id=book_id)
                    booking = Booking.objects.create(
                        contact=contact,
                        book=book
                    )
                    book.available = False
                    book.save()
                    context = {
                        'book_title': book.title
                    }
                    return render(request, 'store/booking_confirmation.html', context)
            except IntegrityError:
                form.errors['internal'] = "An internal error occured. Please retry your request."
        else:
            context['errors'] = form.errors.items()
    else:
        form = ContactForm()
    context['form'] = form
    return render(request, 'store/detail.html', context)

def search(request):
    query = request.GET.get('query')
    if not query:
        books = Book.objects.all()
    else:
        books = Book.objects.filter(title__icontains=query)

    if not books.exists():
        books = Book.objects.filter(author__name__icontains=query)
    
    title = "Results for the search %s"%query
    context = {
        'books': books,
        'title': title
    }

    return render(request, 'store/search.html', context)


def profile(request, author_id):
    author = get_object_or_404(Author, pk=author_id)
    books_list = [book for book in author.books.all()]
    context = {
        'books_list': books_list,
        'author_name': author.name,
        'author_id': author.id,
        'thumbnail': author.picture,
        'about': author.about,
    }

    return render(request, 'store/profile.html', context)