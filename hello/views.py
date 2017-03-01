from django.shortcuts import render
from django.contrib.auth.decorators import login_required


# Create your views here.
def get_index(request):
    return render(request, 'index.html')


@login_required(login_url='/login/')
def profile(request):
    return render(request, 'profile.html')
