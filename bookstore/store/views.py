from django.shortcuts import render

# Create your views here.
def store_views(request):
    return render(request, 'store/store.html')