from django.shortcuts import render, redirect
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
            'user_login': request.user,
        })
    except ObjectDoesNotExist:
        return render(request, 'sorry_massage.html', {'message': 'This user does not exist.',
                                                      'user_login': request.user,
                                                      })


@login_required
def all_users(request):
    return render(request, 'users/all_users.html', {
        'users': User.objects.all(),
        'user_login': request.user,
    })


@login_required
def my_profile(request):
    return redirect(f'/users/{request.user.id}/')