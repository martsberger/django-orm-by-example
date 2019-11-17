from django.db.models import Count, Q, F, Avg, Subquery, OuterRef
from django.db.models.functions import Coalesce
from django.shortcuts import render
from django_pivot.pivot import pivot
from sql_util.utils import SubqueryCount, SubqueryAggregate, Exists

from app.models import Author, Book, UserRating, Genre
from app.utils import add_function_body_as_kwarg


def app(request):
    return render(request, 'app.html', {})


@add_function_body_as_kwarg
def author_list(request, **context):
    authors = Author.objects.all()[:25]
    context.update({
        'authors': authors
    })
    return render(request, 'author_list.html', context)


@add_function_body_as_kwarg
def prolific_author_list(request, **context):
    authors = Author.objects.annotate(book_count=Count('book')).order_by('-book_count')
    context.update({
        'authors': authors
    })
    return render(request, 'prolific_author_list.html', context)


@add_function_body_as_kwarg
def prolific_author_collaborators_list_bug_v1(request, **context):
    # Bug -- `Count`s are missing `distinct=True`
    annotations = {
        'book_count': Count('book'),
        'collaborator_count': Count('book__authors')
    }
    authors = Author.objects.annotate(**annotations).order_by('-book_count', '-collaborator_count')
    context.update({
        'authors': authors
    })
    return render(request, 'prolific_author_collaborators_list.html', context)


@add_function_body_as_kwarg
def prolific_author_collaborators_list_bug_v2(request, **context):
    # Bug -- Counting self collaboration
    annotations = {
        'book_count': Count('book', distinct=True),
        'collaborator_count': Count('book__authors', distinct=True)
    }
    authors = Author.objects.annotate(**annotations).order_by('-book_count', '-collaborator_count')
    context.update({
        'authors': authors
    })
    return render(request, 'prolific_author_collaborators_list.html', context)


@add_function_body_as_kwarg
def prolific_author_collaborators_list(request, **context):
    annotations = {
        'book_count': Count('book', distinct=True),
        'collaborator_count': Count('book__authors', filter=~Q(book__authors__id=F('id')))
    }
    authors = Author.objects.annotate(**annotations).order_by('-book_count', '-collaborator_count')
    context.update({
        'authors': authors
    })
    return render(request, 'prolific_author_collaborators_list.html', context)


@add_function_body_as_kwarg
def book_list_slow(request, **context):
    books = Book.objects.all()[:55]
    context.update({
        'books': books
    })
    return render(request, 'book_list.html', context)


@add_function_body_as_kwarg
def book_list(request, **context):
    books = Book.objects.all().prefetch_related('authors')[:55]
    context.update({
        'books': books
    })
    return render(request, 'book_list.html', context)


@add_function_body_as_kwarg
def highly_rated_books(request, **context):
    books = Book.objects.annotate(rating=Avg('userrating__rating'),
                                  rating_count=Count('userrating')).order_by('-rating', '-rating_count')
    context.update({
        'books': books[:50]
    })
    return render(request, 'popular_books.html', context)


@add_function_body_as_kwarg
def popular_books(request, **context):
    books = Book.objects.annotate(rating=Avg('userrating__rating'),
                                  rating_count=Count('userrating')).order_by('-rating', '-rating_count')
    context.update({
        'books': books[:50]
    })
    return render(request, 'popular_books.html', context)


@add_function_body_as_kwarg
def popular_books_with_author_count(request, **context):
    annotations = {
        'rating': Avg('userrating__rating'),
        'rating_count': Count('userrating', distinct=True),
        'author_count': Count('authors', distinct=True)
    }
    books = Book.objects.annotate(**annotations).order_by('-rating', '-rating_count')[:50]
    context.update({
        'books': books
    })
    return render(request, 'popular_books_author_count.html', context)


@add_function_body_as_kwarg
def popular_books_with_author_count_subquery(request, **context):
    annotations = {
        'rating': Subquery(UserRating.objects
                           .filter(book=OuterRef('pk'))
                           .values('book__pk')
                           .annotate(avg_rating=Avg('rating'))
                           .values('avg_rating')),
        'rating_count': Subquery(UserRating.objects
                                 .filter(book=OuterRef('pk'))
                                 .values('book__pk')
                                 .annotate(count=Count('pk'))
                                 .values('count')),
        'author_count': Subquery(Author.objects
                                 .filter(book=OuterRef('pk'))
                                 .values('book__pk')
                                 .annotate(count=Count('book'))
                                 .values('count'))
    }
    books = Book.objects.annotate(**annotations).order_by('-rating', '-rating_count')[:50]
    context.update({
        'books': books
    })
    return render(request, 'popular_books_author_count.html', context)


class SubqueryAvg(SubqueryAggregate):
    aggregate = Avg
    unordered = True


@add_function_body_as_kwarg
def popular_books_with_author_count_easy_subquery(request, **context):
    annotations = {
        'rating': SubqueryAvg('userrating__rating'),
        'rating_count': SubqueryCount('userrating'),
        'author_count': SubqueryCount('authors')
    }
    books = Book.objects.annotate(**annotations).order_by('-rating')[:50]
    context.update({
        'books': books
    })
    return render(request, 'popular_books_author_count.html', context)


@add_function_body_as_kwarg
def author_genre_counts(request, **context):
    authors = Author.objects.annotate(book_count=Count('book')).order_by('-book_count')
    authors = pivot(authors, ['first_name', 'last_name'], 'book__genres__name', 'pk', Count, default=0)
    genre_names = Genre.objects.all().values_list('name', flat=True)
    context.update({
        'authors': authors[:50],
        'genre_names': genre_names
    })
    return render(request, 'author_genre_counts.html', context)


@add_function_body_as_kwarg
def author_with_rating_counts(request, **context):
    authors = Author.objects.annotate(
        five_star_ratings=Coalesce(Count('book__userrating', filter=Q(book__userrating__rating=5)), 0),
        four_star_ratings=Coalesce(Count('book__userrating', filter=Q(book__userrating__rating=4)), 0),
        three_star_ratings=Coalesce(Count('book__userrating', filter=Q(book__userrating__rating=3)), 0),
        two_star_ratings=Coalesce(Count('book__userrating', filter=Q(book__userrating__rating=2)), 0),
        one_star_ratings=Coalesce(Count('book__userrating', filter=Q(book__userrating__rating=1)), 0)
    ).order_by('-five_star_ratings', '-four_star_ratings', '-three_star_ratings')
    context.update({
        'authors': authors[:50]
    })
    return render(request, 'author_rating_counts.html', context)


def star_number_to_label(number):
    number_map = {'5': 'five', '4': 'four', '3': 'three', '2': 'two', '1': 'one'}
    return f'{number_map.get(number)}_star_ratings'


@add_function_body_as_kwarg
def author_with_rating_counts_pivot(request, **context):
    authors = pivot(Author.objects.order_by('-five_star_ratings', '-four_star_ratings', '-three_star_ratings'),
                    ['pk', 'first_name', 'last_name'],
                    'book__userrating__rating',
                    'pk', Count,
                    default=0,
                    choices=((x, str(x)) for x in range(1, 6)),
                    display_transform=star_number_to_label)
    context.update({
        'authors': authors[:50]
    })
    return render(request, 'author_rating_counts.html', context)


@add_function_body_as_kwarg
def authors_with_no_books_django_exists(request, **context):
    authors = Author.objects.annotate(no_books=~Exists(
        Book.objects.filter(authors=OuterRef('pk'))
    )).filter(no_books=True)
    context.update({
        'authors': authors[:50]
    })
    return render(request, 'author_list.html', context)


@add_function_body_as_kwarg
def authors_with_no_books(request, **context):
    authors = Author.objects.annotate(no_books=~Exists('book')).filter(no_books=True)
    context.update({
        'authors': authors[:50]
    })
    return render(request, 'author_list.html', context)
