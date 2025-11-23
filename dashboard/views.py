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
from django.http import JsonResponse
from django.template.loader import render_to_string


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
    items = Item.objects.all().order_by("-created_at")
    
    return render(request, 'dashboard/dashboard.html', {
     'mode': get_mode(request),
     'user': request.user,
     'items': items,
     })

@login_required(login_url="login")
def dashboard(request):
    #First page of items
    items = Item.objects.order_by("-created_at")
    paginator = Paginator(items, 10)  #10 items per "page"
    page_obj = paginator.get_page(1)

    return render(request, "dashboard.html", {
        "mode": "admin" if request.user.is_staff else "user",
        "items": page_obj.object_list,
        "has_next": page_obj.has_next(),
    })

@login_required(login_url="login")
def items_page(request, page):
    items = Item.objects.order_by("-created_at")
    paginator = Paginator(items, 10)

    page_obj = paginator.get_page(page)

    html = render_to_string(
        "partials/item_cards.html",  
        {"items": page_obj.object_list},
        request=request,
    )

    return JsonResponse({
        "html": html,
        "has_next": page_obj.has_next(),
        "next_page": page + 1,
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