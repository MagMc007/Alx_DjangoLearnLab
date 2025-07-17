#query all books by an author
Book.objects.filter(author__name="specific author")

#list all books in the library
library_name="alx library"

library = Library.objects.get(name=library_name)

books = library.books.all()

for book in books:
    print(book)

#Retrieve the librarian for a library.
library = Library.objects.get(name=library_name)
print(library.librarian.name)