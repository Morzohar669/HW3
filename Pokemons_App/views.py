from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, 'index.html')

def Query(request):
    return render(request, 'Query.html')

def Add(request):
    return render(request, 'Add.html')