from .models import Author, Library, Book


# query all books by an author
author_name = "specific author"

author = Author.objects.get(name=author_name)
Book.objects.filter(author=author)

# list all books in the library
library_name = "alx library"

library = Library.objects.get(name=library_name)

books = library.books.all()

for book in books:
    print(book)

# Retrieve the librarian for a library.
library = Library.objects.get(name=library_name)
print(library.librarian.name)
