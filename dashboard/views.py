from django.shortcuts import *
from django.http import HttpResponse
from django.contrib.auth.decorators import *
from django.contrib.auth.models import User
from django.contrib.auth import logout as user_logout
from allauth.socialaccount.models import *
from .models import Item
from .forms import ItemForm
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.contrib.postgres.search import SearchVector


def super_user_required(func):
    return user_passes_test(lambda u: u.is_superuser, login_url='dashboard')(func)

def get_mode(request):
    return 'admin' if request.user.is_superuser else 'user'

# Create your views here.

def logout(request):
    user_logout(request)
    return redirect('/')


@login_required
def dashboard(request):
    mode = "admin" if request.user.is_staff else "user" 
    item_list = Item.objects.all().order_by("-created_at")
    query = request.GET.get('q')
    if query:
        item_list = item_list.annotate(
            search=SearchVector('title', 'description'),
        ).filter(search=query)

    paginator = Paginator(item_list, 4)
    page_number = request.GET.get('page')
    items = paginator.get_page(page_number)
    
    return render(request, 'dashboard/dashboard.html', {
     'mode': get_mode(request),
     'user': request.user,
     'items': items,
     })

@login_required(login_url="account_login")
def create_item(request):
    if request.method == "POST":
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.seller = request.user
            item.save()
            return redirect("dashboard")
    else:
        form = ItemForm()

    return render(request, "dashboard/item_form.html", {"form": form})


@login_required(login_url="account_login")
def delete_item(request, pk):
    item = get_object_or_404(Item, pk=pk)

    #only seller or staff can delete
    if request.user != item.seller and not request.user.is_staff:
        return redirect("dashboard")

    if request.method == "POST":
        item.delete()
        return redirect("dashboard")

    return render(request, "dashboard/item_confirm_delete.html", {"item": item})

def items_list(request):
     return HttpResponse("")

def item_create(request):
     return HttpResponse("")

def cart(request):
     return HttpResponse("")

def checkout(request):
     return HttpResponse("")

def orders(request):
     return HttpResponse("")