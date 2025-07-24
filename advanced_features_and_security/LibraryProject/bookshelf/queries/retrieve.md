#command to obtain a book object with the title 1984
book_by_title = Book.objects.get(title="1984")
#<QuerySet [<Book: Title: 1984 by George Orwell publsihed in 1949>]