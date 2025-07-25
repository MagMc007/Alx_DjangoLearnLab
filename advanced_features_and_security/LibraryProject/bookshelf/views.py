from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import permission_required

@permission_required("bookshelf.can_create", raise_exception=True)
def create_view(request):
    return HttpResponse("This is the create page")

@permission_required("bookshelf.can_edit", raise_exception=True)
def book_list(request):
    return HttpResponse("This is the view page")

@permission_required("bookshelf.can_view", raise_exception=True)
def edit_view(request):
    return HttpResponse("This is the edit page")

@permission_required("bookshelf.can_delete", raise_exception=True)
def delete_view(request):
    return HttpResponse("This is the delete page")



