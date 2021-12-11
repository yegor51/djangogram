from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Publication, Comment
from .forms import CreatePublicationForm, CreateCommentForm


@login_required
def publication_view(request, publication_id):
    publication_object = get_object_or_404(Publication, id=publication_id)
    if request.method == 'POST':
        comment_form = CreateCommentForm(request.POST)
        if comment_form.is_valid():
            Comment.create_comment(publication_object,
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
def create_publication(request):
    if request.method == 'POST':
        form = CreatePublicationForm(request.POST, request.FILES)
        if form.is_valid():
            new_publication = Publication.create_publication(
                author=request.user,
                publication_name=form.cleaned_data.get('publication_name'),
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
def like_publication(request, publication_id):
    if request.method == 'POST':

        publication = get_object_or_404(Publication, id=publication_id)
        publication.set_mark(request.user, request.POST.get('value'))

    return redirect('view_publication', publication_id)


@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if comment.author == request.user:
        comment.delete()

    return redirect('view_publication', comment.publication.id)


@login_required
def delete_publication(request, publication_id):
    publication = get_object_or_404(Publication, id=publication_id)
    if publication.author == request.user:
        publication.delete()

    return redirect('view_user', publication.author.id)