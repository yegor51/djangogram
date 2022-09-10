from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from djangogramm.utils import confirm_email_required
from .models import User, Follow
from .forms import EditProfileForm
from publications.models import Publication, Comment


@login_required
@confirm_email_required
def user_view(request, user_id):
    """
    user profile view page.

    POST method: edit user profile.
    """
    edit_profile_form_inital = {
        'first_name': request.user.first_name,
        'last_name': request.user.last_name,
        'bio': request.user.bio,
        'avatar': request.user.avatar,
    }

    if request.method == 'POST':
        edit_profile_form = EditProfileForm(request.POST,
                                            request.FILES,
                                            initial=edit_profile_form_inital)

        if edit_profile_form.is_valid():
            request.user.edit_profile(
                bio=edit_profile_form.cleaned_data.get('bio'),
                first_name=edit_profile_form.cleaned_data.get('first_name'),
                last_name=edit_profile_form.cleaned_data.get('last_name'),
                avatar=edit_profile_form.cleaned_data.get('avatar'),
            )
            return redirect('view_user', user_id)
    else:
        edit_profile_form = EditProfileForm(initial=edit_profile_form_inital)

    user_object = get_object_or_404(User, id=user_id)

    return render(request, 'users/view_user.html', {
        'user': user_object,
        'publications': Publication.objects.filter(author=user_object),
        'comments_count': Comment.objects.filter(author=user_object).count(),
        'edit_profile_form': edit_profile_form,
        'is_user_followed': request.user.check_user_followed(user_object)
    })


@login_required
@confirm_email_required
def all_users(request):
    """all users list page."""
    return render(request, 'users/all_users.html', {
        'users': User.objects.all(),
        'followings': request.user.followings(),
    })


@login_required
@confirm_email_required
def my_profile(request):
    """redirect to login user profile page."""
    return redirect(f'/users/{request.user.id}/')


@login_required
@confirm_email_required
def my_followings(request):
    """list of followings of user page."""
    return render(request, 'users/my_followings.html', {
        'followings': request.user.followings(),
    })


@login_required
@confirm_email_required
def create_follow(request, following_id):
    """
    """
    if request.method == 'POST':
        next = request.GET.get('next')
        following = get_object_or_404(User, id=following_id)
        Follow.create(request.user, following)

        if next:
            return redirect(next)

    return redirect('view_user', following_id)


def delete_follow(request, following_id):
    if request.method == 'POST':
        next = request.GET.get('next')
        following = get_object_or_404(User, id=following_id)
        follow = get_object_or_404(Follow, follower=request.user, following=following)
        if follow:
            follow.delete()

        if next:
            return redirect(next)

    return redirect('view_user', following_id)