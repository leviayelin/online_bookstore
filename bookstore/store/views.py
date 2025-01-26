#from django.contrib.auth import login 
from django.shortcuts import render, redirect
#from django.contrib.auth.forms import UserCreationForm, AuthenticationForm




def store_views(request):
    return render(request, 'store/home.html')

# def signup_view(request):
#    if request.method == 'POST':
#       form = UserCreateionForm(request.POST)
#        if form.is_valid():
#           form.save()
#            return redirect('login')
#    else:
#        form = UserCreationForm()
   
#    return render(request, 'store/signup.html', {'form': form})

#def login_view(request):
#    if request.method == "POST":
#        form = AuthenticationForm(data=request.POST)
#        if form.is_valid():
#            user = form.get_user()
#            login(request, user)
#            if 'next' in request.POST:
#                return redirect(request.POST.get('next'))
#            else:
#                return redirect('login')
#    else:
#        form = AuthenticationForm()
#    return render(request, 'store/login.html', {'form': form})
