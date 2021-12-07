from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from publications.models import Publication, Comment, Mark
from django.core.exceptions import ObjectDoesNotExist


@login_required
def publication_view(request, id):
    try:
        publication_object = Publication.objects.get(id=id)
        return render(request, 'publications/view_publication.html', {
            'publication': publication_object,
            'comments': Comment.objects.filter(publication=publication_object),
            'likes_count': Mark.objects.filter(publication=publication_object, value=True).count(),
            'dislikes_count': Mark.objects.filter(publication=publication_object, value=False).count(),
            'user_login': request.user,
        })
    except ObjectDoesNotExist:
        return render(request, 'sorry_massage.html', {'message': 'This publication does not exist.',
                                                      'user_login': request.user,
                                                      })
