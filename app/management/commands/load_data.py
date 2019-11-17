from itertools import cycle, islice
import random
from time import time

from django.core.management import BaseCommand

from app.models import Author, Genre, User, Book, UserRating


class Command(BaseCommand):
    """
    load a bunch of data into the database
    """

    def handle(self, *args, **options):
        start_time = time()
        Author.objects.all().delete()
        User.objects.all().delete()
        Book.objects.all().delete()
        UserRating.objects.all().delete()
        Genre.objects.all().delete()
        print("deletes done", time() - start_time)

        first_names = [
            'Lacy', 'Alaine' 'Marylin', 'Tula', 'Roberta', 'Tania', 'Gary', 'Kristal', 'Jeannine', 'Shela', 'Kyra',
            'Bo', 'Mozelle', 'Tyron', 'Mai', 'Oda', 'Kerry', 'Lorretta', 'Laureen', 'Aretha', 'Bobette', 'Whitley',
            'Angelique', 'Mario', 'Asia', 'Sharlene', 'Johnette', 'Rod', 'Erasmo', 'Marlyn', 'Yvette', 'Elizabeth',
            'Tawanda', 'Ivory', 'Tyisha', 'Emmaline', 'Randall', 'Odette', 'Isabelle', 'Granville', 'Jay', 'Darleen',
            'Arlean', 'Un', 'Louanne', 'Devora', 'Rodney', 'Sixta', 'Martine', 'Hollie', 'Raul', 'Anette', 'Yolande',
            'Monserrate', 'Kellye', 'Casimira', 'Karlene', 'Donya', 'Nelda', 'Joesph', 'Tyrone', 'Dorothea', 'Lesli',
            'Rozanne', 'Mirian', 'Jae', 'Gavin', 'Vita', 'Corrinne', 'Roscoe', 'Veola',
            'Wynona', 'Dorcas', 'Cristin', 'Faith', 'Erin', 'Linda', 'Debi', 'Marquitta', 'Kathi', 'Shasta', 'Britni',
            'Rina', 'Emelda', 'Evalyn', 'Sal', 'Lawerence', 'Verena', 'Tennille', 'Ben', 'Elouise', 'Sook', 'Kiyoko',
            'Roselyn', 'Pia', 'Delaine', 'Mirtha', 'Bianca', 'Risa', 'Mila', 'Taisha', 'Karyl', 'Cary', 'Jani',
            'Chad', 'Nigel', 'Danny', 'Azucena', 'Marti', 'Fannie', 'Cassy', 'Hyman', 'Glinda', 'Percy', 'Joanna',
            'Jeromy', 'Simonne', 'Diane', 'Shantel', 'Tom', 'Lang',
        ]

        last_names = [
            'Snellgrove', 'Gilliland', 'Wellington', 'Panzer', 'Gittens', 'Czajkowski', 'Bloomquist', 'Abramson',
            'Keating', 'Valenzuela', 'Moritz', 'Blasko', 'Arceneaux', 'Stotz', 'Ospina', 'Bushnell', 'Buonocore',
            'Husain', 'Koons', 'Mash', 'Alvarez', 'Moudy', 'Brownlow', 'Rothenberg', 'Tope', 'Andreas', 'Remer',
            'Decarlo', 'Savoy', 'Armstead', 'Snook', 'Barthel', 'Sheehan', 'Gebhardt', 'Gaut', 'Erickson',
            'Widell', 'Swilley', 'Dodge', 'Benedict', 'Debonis', 'Byfield', 'Brisco', 'Spatz', 'Neifert', 'Mcmunn',
            'Keller', 'Boulay', 'Rolling', 'Toothaker', 'Jock', 'Fullmer', 'Schoepp', 'Lasker', 'Dow', 'Wingerter',
            'Fortman', 'Crowe', 'Rhodes', 'Mckee', 'Hoop', 'Hales', 'Sandell', 'Murnane', 'Sirmans', 'Fry',
            'Avitia', 'Wittmer', 'Criado', 'Zelinski', 'Berumen', 'Kennett', 'Brayboy', 'Providence', 'Reddick',
            'Spinney', 'Organ', 'Middlebrook', 'Brownell', 'Kimmel', 'Sorensen', 'Brossard', 'Temple', 'Mayes',
            'Gade', 'Kary', 'Firkins', 'Porcaro', 'Moschella', 'Aquilino', 'Soule', 'Glenn', 'Dandrea', 'Woolston',
            'Ewald', 'Junior', 'Nanez', 'Berlanga', 'Eppinger', 'Payton', 'Linke',
            'Roache', 'Overall', 'Pitre', 'Kirtley', 'Seeman', 'Belliveau', 'Lathrop', 'Barrington', 'Dargie',
            'Sauers', 'Carpentier', 'Peavey', 'Bocanegra', 'Albers', 'Searfoss', 'Worthen', 'Demps', 'Orchard',
            'Kromer', 'Gauthier',
        ]

        print("len first", len(first_names))
        print("len las", len(last_names))

        authors = [Author(first_name=element[0], last_name=element[1])
                   for element in islice(zip(cycle(first_names), cycle(last_names)), 10000)]

        Author.objects.bulk_create(authors)
        print("authors created", time() - start_time)

        genres_names = ['Sci-Fi', 'Fantasy', 'Romance', 'Western', 'Thriller', 'Mystery', 'Detective', 'Dystopia',
                        'Memoir', 'Biography', 'Play', 'Musical', 'Satire', 'Haiku', 'Horror', 'Do It Yourself']

        genres = [Genre(name=name) for name in genres_names]
        Genre.objects.bulk_create(genres)

        users = [User(username=f'username {n}') for n in range(100000)]
        User.objects.bulk_create(users)
        print("users created", time() - start_time)

        articles = ['The', 'A']
        adjectives = [
            'able', 'bad', 'best', 'better', 'big', 'black', 'certain', 'clear', 'different', 'early', 'easy',
            'economic', 'federal', 'free', 'full', 'good', 'great', 'hard', 'high', 'human', 'important',
            'international', 'large', 'late', 'little', 'local', 'long', 'low', 'major', 'military', 'national',
            'new', 'old', 'only', 'other', 'political', 'possible', 'public', 'real', 'recent', 'right', 'small',
            'social', 'special', 'strong', 'sure', 'true', 'white', 'whole', 'young',
        ]
        nouns = [
            'area', 'book', 'business', 'case', 'child', 'company', 'country', 'day', 'eye', 'fact', 'family',
            'government', 'group', 'hand', 'home', 'job', 'life', 'lot', 'man', 'money', 'month', 'mother', 'Mr',
            'night', 'number', 'part', 'people', 'place', 'point', 'problem', 'program', 'question', 'right', 'room',
            'school', 'state', 'story', 'student', 'study', 'system', 'thing', 'time', 'water', 'way', 'week',
            'woman', 'word', 'work', 'world', 'year',
        ]

        book_titles = set()

        vowels = {'a', 'e', 'i', 'o', 'u'}

        def word_with_article(word):
            article = random.choice(articles)
            if word[0].lower() in vowels and article.lower() == 'a':
                article += 'n'

            return f'{article} {word}'

        def generate_book_title():
            title = f'{word_with_article(random.choice(adjectives))} {random.choice(nouns)}'

            if title in book_titles:
                title += f' and {word_with_article(random.choice(adjectives))} {random.choice(nouns)}'

            return title

        print("generating book titles:", time() - start_time)
        for _ in range(20000):
            book_titles.add(generate_book_title())

        books = [Book(title=title) for title in book_titles]
        Book.objects.bulk_create(books)

        print("making author and genre lists", time() - start_time)
        all_authors = list(Author.objects.all())
        all_genres = list(Genre.objects.all())
        print("getting user list", time() - start_time)
        all_users = list(User.objects.all())

        print("assigning authors and genres", time() - start_time)
        count = 0
        for book in Book.objects.all():
            authors = [random.choice(all_authors)]
            while random.randint(1, 10) > 9:
                authors.append(random.choice(all_authors))

            book.authors.add(*authors)

            genres = [random.choice(all_genres)]
            while random.randint(1, 20) > 10:
                genres.append(random.choice(all_genres))

            book.genres.add(*genres)

            rating_count = abs(int(random.gauss(100, 50)))
            users = random.sample(all_users, rating_count)
            user_ratings = [UserRating(user=user, book=book, rating=random.randint(1, 5)) for user in users]
            UserRating.objects.bulk_create(user_ratings)

            count += 1
            if count % 1000 == 0:
                print("count", count, "time:", time() - start_time)


