from django.shortcuts import render, redirect
from .models import Room, Topic
from django.db.models import Q
from .forms import RoomForm


def home(request):
    q = request.GET.get("q")
    if q is None:
        q = ""
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q)
        | Q(name__icontains=q)
        | Q(description__icontains=q)
        | Q(host__username__icontains=q)
    )
    topics = Topic.objects.all()
    room_count = rooms.count()
    context = {"rooms": rooms, "topics": topics, "room_count": room_count}
    return render(request, "base/home.html", context)


def rooms(request, id):
    context = {"room": Room.objects.get(id=id)}
    return render(request, "base/rooms.html", context=context)


def createRoom(request):
    form = RoomForm()
    if request.method == "POST":
        form_data = RoomForm(request.POST)
        if form_data.is_valid:
            form_data.save()
            return redirect("home")

    context = {"form": form}
    return render(request=request, template_name="base/room_form.html", context=context)


def updateRoom(request, id):
    room = Room.objects.get(id=id)
    form_data = RoomForm(instance=room)

    if request.method == "POST":
        form_data = RoomForm(request.POST, instance=room)
        if form_data.is_valid:
            form_data.save()
            return redirect("home")
    context = {"form": form_data}
    return render(request=request, template_name="base/room_form.html", context=context)


def deleteRoom(request, id):
    room = Room.objects.get(id=id)
    if request.method == "POST":
        room.delete()
        return redirect("home")
    return render(
        request=request, template_name="base/delete.html", context={"obj": room}
    )
