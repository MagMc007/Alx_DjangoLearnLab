#command to create an instance of Book class
book = Book(title="1984", author="George Orwell",publication_year=1949)
book.save()

#command to obtain a book object with the title 1984
book_by_title = Book.objects.filter(title="1984")
#<QuerySet [<Book: Title: 1984 by George Orwell publsihed in 1949>]


#python command to update the book 1984 filtered by name
Book.objects.filter(title="1984").update(title="Nineteen Eighty-Four")
#1


#command to delete an object
Book.objects.filter(title="Nineteen Eighty-Four").delete()
#(1, {'bookshelf.Book': 1})
