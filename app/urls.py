from django.urls import path

from app.views import (author_list, book_list, prolific_author_list, prolific_author_collaborators_list,
                       prolific_author_collaborators_list_bug_v1, prolific_author_collaborators_list_bug_v2,
                       popular_books, popular_books_with_author_count, popular_books_with_author_count_easy_subquery,
                       popular_books_with_author_count_subquery, app, book_list_slow, author_genre_counts,
                       author_with_rating_counts, author_with_rating_counts_pivot, authors_with_no_books,
                       authors_with_no_books_django_exists)

urlpatterns = [
    path('app/', app),
    path('authors/', author_list, name='author_list'),
    path('prolific_authors/', prolific_author_list, name='prolific_author_list'),
    path('prolific_author_collaborators/', prolific_author_collaborators_list, name='prolific_author_collaborators_list'),
    path('prolific_author_collaborators_bug_v1/', prolific_author_collaborators_list_bug_v1, name='prolific_author_collaborators_list_bug_v1'),
    path('prolific_author_collaborators_bug_v2/', prolific_author_collaborators_list_bug_v2, name='prolific_author_collaborators_list_bug_v2'),
    path('books/', book_list, name='book_list'),
    path('books_slow/', book_list_slow, name='book_list_slow'),
    path('popular_books/', popular_books, name='popular_books'),
    path('popular_books_author_count/', popular_books_with_author_count, name='popular_books_with_author_count'),
    path('popular_books_author_count_subquery/', popular_books_with_author_count_subquery, name='popular_books_with_author_count_subquery'),
    path('popular_books_author_count_easy_subquery/', popular_books_with_author_count_easy_subquery, name='popular_books_with_author_count_easy_subquery'),
    path('author_genre_counts/', author_genre_counts, name='author_genre_counts'),
    path('author_rating_counts/', author_with_rating_counts, name='author_rating_counts'),
    path('author_rating_counts_pivot/', author_with_rating_counts_pivot, name='author_rating_counts_pivot'),
    path('authors_with_no_books_django/', authors_with_no_books_django_exists, name='authors_with_no_books_django_exists'),
    path('authors_with_no_books/', authors_with_no_books, name='authors_with_no_books')
]
