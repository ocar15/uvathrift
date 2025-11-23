from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse
from django.http import Http404
from postman.models import Message


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

@login_required
def unarchive_messages(request):
    if request.method != "POST":
        raise Http404("POST required")

    # same style as postman:delete — accept pks list
    pks = request.POST.getlist("pks")
    if not pks:
        raise Http404("No messages selected")

    qs = Message.objects.filter(pk__in=pks)

    if not qs.exists():
        raise Http404("Messages not found")

    user = request.user
    for msg in qs:
        # clear the archived flag only for the current user
        if msg.sender_id == user.id:
            msg.sender_archived = False
        if msg.recipient_id == user.id:
            msg.recipient_archived = False
        msg.save()

    next_url = (
        request.POST.get("next")
        or reverse("postman:inbox")  # default if next is missing
    )
    return redirect(next_url)
