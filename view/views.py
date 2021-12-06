from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from users.models import User
from publications.models import Publication, Comment, Mark
from django.core.exceptions import ObjectDoesNotExist


@login_required
def profile(request, id):
    try:
        user_object = User.objects.get(id=id)
        return render(request, 'main/view_profile.html', {
            'user': user_object,
            'publications': Publication.objects.filter(author=user_object),
            'comments_count': Comment.objects.filter(author=user_object).count(),
        })
    except ObjectDoesNotExist:
        return render(request, 'main/sorry_massage.html', {'message': 'This user does not exist.'})


@login_required
def publication(request, id):
    try:
        publication_object = Publication.objects.get(id=id)
        return render(request, 'main/view_publication.html', {
            'publication': publication_object,
            'comments': Comment.objects.filter(publication=publication_object),
            'likes_count': Mark.objects.filter(publication=publication_object, value=True).count(),
            'dislikes_count': Mark.objects.filter(publication=publication_object, value=False).count(),
        })
    except ObjectDoesNotExist:
        return render(request, 'main/sorry_massage.html', {'message': 'This publication does not exist.'})


@login_required
def all_users(request):
    return render(request, 'main/all_users.html', {
        'users': User.objects.all(),
    })