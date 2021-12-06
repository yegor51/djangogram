from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from users.models import User
from publications.models import Publication, Comment, Mark
from django.core.exceptions import ObjectDoesNotExist


@login_required
def user_view(request, id):
    try:
        user_object = User.objects.get(id=id)
        return render(request, 'users/view_user.html', {
            'user': user_object,
            'publications': Publication.objects.filter(author=user_object),
            'comments_count': Comment.objects.filter(author=user_object).count(),
        })
    except ObjectDoesNotExist:
        return render(request, 'main/sorry_massage.html', {'message': 'This user does not exist.'})


@login_required
def all_users(request):
    return render(request, 'users/all_users.html', {
        'users': User.objects.all(),
    })