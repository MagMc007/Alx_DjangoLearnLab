book_to_update = Book.objects.filter(title="1984")
book_to_update.title("Nineteen Eighty-Four")