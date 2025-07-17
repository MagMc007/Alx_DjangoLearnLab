#query all books by an author
Book.objects.filter(author__name="specific author")

#list all books in the library
library = Library.objects.get(name="Central")

books = library.books.all()

for book in books:
    print(book)

#Retrieve the librarian for a library.
library = Library.objects.get(name="Central")
print(library.librarian.name)