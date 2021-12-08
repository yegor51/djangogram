from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import User
from .forms import EditProfileForm
from publications.models import Publication, Comment


@login_required
def user_view(request, user_id):
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
    })


@login_required
def all_users(request):
    return render(request, 'users/all_users.html', {
        'users': User.objects.all(),
    })


@login_required
def my_profile(request):
    return redirect(f'/users/{request.user.id}/')