from django.shortcuts import *
from django.http import HttpResponse
from django.contrib.auth.decorators import *
from django.contrib.auth.models import User
from django.contrib.auth import logout as user_logout
from allauth.socialaccount.models import *
from .models import Item, SavedItem
from .forms import ItemForm
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.contrib.postgres.search import SearchVector
from moderation.models import Reports


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
    item_list = Item.objects.all()

    for item in item_list:
        item.is_saved = item.is_saved_by(request.user)

    sort = request.GET.get('sort', 'newest')
    verified = request.GET.get('verified', False)
    condition_filter = request.GET.get('condition', None)
    query = request.GET.get('q')

    if query:
        item_list = item_list.annotate(
            search=SearchVector('title', 'description'),
        ).filter(search=query)

    if verified:
        item_list = item_list.filter(seller__profile__student_email_verified=True)
    
    if condition_filter:
        item_list = item_list.filter(condition=condition_filter)

    if sort == 'newest':
        item_list = item_list.order_by('-created_at')
    elif sort == 'oldest':
        item_list = item_list.order_by('created_at')
    elif sort == 'price_asc':
        item_list = item_list.order_by('price')
    elif sort == 'price_desc':
        item_list = item_list.order_by('-price')
    elif sort == 'condition_asc':
        item_list = item_list.order_by('condition')
    elif sort == 'condition_desc':
        item_list = item_list.order_by('-condition')

    paginator = Paginator(item_list, 4)
    page_number = request.GET.get('page')
    items = paginator.get_page(page_number)
    
    return render(request, 'dashboard/dashboard.html', {
        'mode': get_mode(request),
        'user': request.user,
        'items': items,
        'sort': sort,
        'condition': condition_filter,
        'verified': verified,
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

@login_required(login_url='account_login')
def report_post(request, pk):
    action = request.POST.get('action')
    item = get_object_or_404(Item, pk=pk)
    user = request.user

    if action:
        if action == "submitReport":
            desc = request.POST.get("report")
            Reports.objects.create(item=item, reported_by=user, report_description=desc)
            return redirect("dashboard")
    return render(request, 'dashboard/report_post.html', {'mode': get_mode(request), 'item': item})

@login_required(login_url="account_login")
def toggle_save_item(request, pk):
    item = get_object_or_404(Item, pk=pk)
    saved_item, created = SavedItem.objects.get_or_create(user=request.user, item=item)

    if not created: # this looks funny but it's right! this part does the toggling
        saved_item.delete()
    
    return redirect(request.META.get('HTTP_REFERER', 'dashboard'))

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