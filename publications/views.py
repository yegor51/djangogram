from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from djangogramm.utils import confirm_email_required
from .models import Publication, Comment
from users.models import User, Follow
from .forms import CreatePublicationForm, CreateCommentForm


@login_required
@confirm_email_required
def publication_view(request, publication_id):
    """
    Publication Page.

    GET method: display publication, comments, and comment write form.
    POST method: create comment to this publication.
    """
    publication_object = get_object_or_404(Publication, id=publication_id)
    if request.method == 'POST':
        comment_form = CreateCommentForm(request.POST)
        if comment_form.is_valid():
            Comment.create(publication_object,
                                   request.user,
                                   comment_form.cleaned_data.get('text')
                                   )
            return redirect('view_publication', publication_id)
    else:
        comment_form = CreateCommentForm()

    return render(request, 'publications/view_publication.html', {
        'publication': publication_object,
        'comments': Comment.objects.filter(publication=publication_object),
        'comment_form': comment_form,
    })


@login_required
@confirm_email_required
def create_publication(request):
    """
    create publication form page.

    GET method: display publication create form.
    POST method: create publication by form.
    """
    if request.method == 'POST':
        form = CreatePublicationForm(request.POST, request.FILES)
        if form.is_valid():
            new_publication = Publication.create(
                author=request.user,
                name=form.cleaned_data.get('name'),
                image=form.cleaned_data.get('image'),
                description=form.cleaned_data.get('description'),
            )
            return redirect('view_publication', new_publication.id)
    else:
        form = CreatePublicationForm()

    return render(request, 'publications/create_publication.html', {
        'form': form,
    })


@login_required
@confirm_email_required
def set_publication_mark(request, publication_id):
    """
    POST method, set like or dislike to publication by publication id.
    """
    if request.method == 'POST':
        next = request.GET.get('next')
        publication = get_object_or_404(Publication, id=publication_id)
        value = request.POST.get('value')
        if value == 'like':
            publication.set_like(request.user)
        elif value == 'dislike':
            publication.set_dislike(request.user)

        if next:
            return redirect(next)

    return redirect('view_publication', publication_id)


@login_required
@confirm_email_required
def delete_comment(request, comment_id):
    """
    POST method, delete comment by comment id.
    """
    comment = get_object_or_404(Comment, id=comment_id)
    if request.method == 'POST':
        if comment.author == request.user:
            comment.delete()

    return redirect('view_publication', comment.publication.id)


@login_required
@confirm_email_required
def delete_publication(request, publication_id):
    """
    POST method, delete publication by publication id.
    """
    publication = get_object_or_404(Publication, id=publication_id)
    if request.method == 'POST':
        if publication.author == request.user:
            publication.delete()

    return redirect('view_user', publication.author.id)


@login_required
@confirm_email_required
def news_feed(request):
    """last publications of users' followings page."""
    followings_list = followings_list = User.objects.filter(id__in=
                                                            Follow.objects.filter(follower=
                                                                                  request.user).values_list('following'))
    return render(request, 'users/news_feed.html', {
        'publications': Publication.objects.filter(author__in=followings_list).order_by('-publication_date'),
        'followings': followings_list,
    })