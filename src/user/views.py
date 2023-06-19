from django.shortcuts import render
from .models import Follow, User
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

@login_required
def follow_user(request, id):

    user_id = request.user.id
    follow = Follow.objects.filter(follower__id=user_id, following__id=id).first()

    if follow is not None:
        follow.delete()
    else:
        follow = Follow.objects.create(follower_id=user_id, following_id=id)
    return HttpResponse(status=200)