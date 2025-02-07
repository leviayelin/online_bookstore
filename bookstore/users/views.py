from django.shortcuts import render, redirect
from accounts.forms import CustomUserChangeForm

# Create your views here.
def user_view(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('users:user')
    else:
        form = CustomUserChangeForm()        
    return render(request, 'users/users.html', {'form':form})
