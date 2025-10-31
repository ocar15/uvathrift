from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def inbox(request):
    return render(request, "inbox.html")

@login_required
def sent(request):
    return render(request, "sent.html") 

@login_required
def view(request):
    return render(request, "view.html") 

@login_required
def write(request):
    return render(request, "write.html") 