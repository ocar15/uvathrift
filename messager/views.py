from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from django.urls import reverse
from django.http import Http404, JsonResponse
from postman.models import Message
from .forms import CreateGroupForm
from .models import GroupChat, GroupChatMessage
from django.contrib.auth.models import User

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

@login_required
def undelete_messages(request):
    if request.method != "POST":
        raise Http404("POST required")

    # Same shape as postman:delete -> accept list of pks
    pks = request.POST.getlist("pks")
    if not pks:
        raise Http404("No messages selected")

    qs = Message.objects.filter(pk__in=pks)
    if not qs.exists():
        raise Http404("Messages not found")

    user = request.user
    for msg in qs:
        # Clear deleted flags only for this user
        if msg.sender_id == user.id:
            msg.sender_deleted_at = None
        if msg.recipient_id == user.id:
            msg.recipient_deleted_at = None
        msg.save()

    next_url = request.POST.get("next") or reverse("postman:inbox")
    return redirect(next_url)

@login_required
def latest_unread_message_api(request):
    qs = Message.objects.filter(
        recipient=request.user,
        read_at__isnull=True
    ).select_related('sender').order_by('-sent_at')

    unread_count = qs.count()
    if unread_count == 0:
        return JsonResponse({"unread": 0})

    latest = qs.first()
    sender_name = latest.sender.get_username()
    subject = latest.subject or ""
    body_preview = (latest.body or "")[:80]

    return JsonResponse({
        "unread": unread_count,
        "latest": {
            "id": latest.id,
            "sender": sender_name,
            "subject": subject,
            "body_preview": body_preview,
        }
    })

@login_required
def report_message(request, pk):
    msg = get_object_or_404(Message, pk=pk)

    if msg.recipient != request.user:
        return redirect("postman:inbox")
    
    msg.moderation_status = 'p'
    msg.moderation_reason = "Reported by User"
    msg.save()

    return redirect("postman:inbox")

@login_required
def group_list(request):
    groups = GroupChat.objects.filter(members=request.user)
    return render(request, 'postman/group_list.html', {"groups": groups})


@login_required
def create_group(request):
    members = User.objects.exclude(id=request.user.id)
    if request.method == "POST":
        form = CreateGroupForm(request.POST)
        form.fields['members'].queryset = members
        
        if form.is_valid():
            group = form.save(commit=False)
            group.created_by = request.user
            group.save()
            form.save_m2m()
            group.members.add(request.user)
            return redirect("group_list")
        else:
            print("ERROR", form.errors)
    else:
        form = CreateGroupForm()
        form.fields['members'].queryset = members

    return render(request, 'postman/create_group.html', {'form': form})

@login_required
def send_group_message(request, group_id):
    group = GroupChat.objects.get(id=group_id)

    if request.method == "POST":
        body = request.POST.get("body")
        if body:
            GroupChatMessage.objects.create(group = group, sender = request.user, body=body)
        return redirect('group_detail', group_id=group.id)
    return render(request, 'postman/send_message.html', {"group": group})

@login_required
def group_detail(request, group_id):
    group = GroupChat.objects.get(id=group_id)
    messages = group.messages.order_by('sent_at')

    return render(request, "postman/group_detail.html", {"group": group, "messages": messages})

@login_required
def delete_group(request, group_id):
    group = get_object_or_404(GroupChat, id=group_id)

    if request.user != group.created_by:
        return redirect("group_list")
    
    if request.method == "POST":
        group.delete()
        return redirect("group_list")
    
    return render(request, 'postman/confirm_delete.html', {"group": group})

@login_required
def leave_group(request, group_id):
    group = get_object_or_404(GroupChat, id=group_id)

    if request.user == group.created_by:
        return redirect('group_detail', group_id=group.id)
    
    if request.method == "POST":
        group.members.remove(request.user)
        return redirect("group_list")
    
    return render(request, 'postman/confirm_leave.html', {'group': group})