#command to delete an object
Book.objects.filter(title="Nineteen Eighty-Four").delete()
#(1, {'bookshelf.Book': 1})
