import operator
from datetime import date
from django.shortcuts import render
from django.contrib import messages
from .models import *
from itertools import chain

import numpy as np

from .utils import getvalue
from better_profanity import profanity


# Create your views here.


def index(request):
    try:
        movies = Movie.objects.all()
        new_release = sorted(movies, key=operator.attrgetter('date'), reverse=True)[0]
    except:
        new_release = None
    try:
        movies = Movie.objects.all()
        high = sorted(movies, key=operator.attrgetter('rating'), reverse=True)[0]
    except:
        high = None
    try:
        movies = Movie.objects.first()
    except:
        movies = None
    params = {
        'new_releases': new_release,
        'top_rated': high,
        'movies': movies,
    }
    return render(request, 'index.html', params)


def top_rated(request):
    movies = Movie.objects.all()
    ordered = sorted(movies, key=operator.attrgetter('rating'), reverse=True)
    params = {
        'title': 'Top Rated',
        'query': ordered,
    }
    return render(request, 'movies.html', params)


def new_releases(request):
    new_release = Movie.objects.filter(date__gte=date.today())
    ordered = sorted(new_release, key=operator.attrgetter('date'), reverse=True)
    params = {
        'query': ordered,
        'title': 'New Releasing'
    }
    return render(request, 'movies.html', params)


def about(request):
    params = {'title': 'About Us'}
    return render(request, 'about.html', params)


def contact(request):
    params = {'title': 'Contact Us'}
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        query = request.POST.get('message')

        obj = Contact.objects.create(
            name=name,
            email=email,
            query=query
        )
        obj.save()
        messages.info(request, 'Thank you for Contacting us:)')
    return render(request, 'contact.html', params)


def single(request, my_id):
    query = Movie.objects.filter(id=my_id)
    user_id = request.user.id
    reviews = Review.objects.filter(movie_name=my_id)
    ordered = sorted(reviews, key=operator.attrgetter('review'), reverse=True)
    params = {'query': query[0], 'placeholder': 'Post Your Review...', 'reviews': ordered}

    if Review.objects.filter(author=user_id, movie_name=my_id).exists():
        x = Review.objects.filter(author=user_id, movie_name=my_id)
        y = x.values('review')[0]
        params['placeholder'] = y['review']

    if request.method == 'POST':
        review = request.POST.get('review')
        if review == 'Post Your Review...':
            return render(request, 'single.html', params)

        if profanity.contains_profanity(review):
            messages.error(request, 'No bad words are accepted!')
            return render(request, 'single.html', params)

        if request.user.is_anonymous:
            messages.error(request, 'You need to login first!')
            return render(request, 'single.html', params)

        if Review.objects.filter(author=user_id, movie_name=my_id).exists():
            Review.objects.filter(author=user_id, movie_name=my_id).delete()

        value = getvalue(review)
        try:
            value = round(value, 3)
        except:
            value = 0
        obj = Review.objects.create(author=request.user,
                                    movie_name=Movie.objects.get(id=my_id),
                                    review=review.strip(),
                                    rated_as=value * 10
                                    )
        obj.save()

        new_rating = Review.objects.values_list('rated_as').filter(movie_name=my_id)

        obj = Movie.objects.get(pk=my_id)
        obj.rating = np.mean(new_rating)
        obj.save()

        x = Review.objects.filter(author=user_id, movie_name=my_id).all()
        y = x.values('review')[0]
        params['placeholder'] = y['review']
        reviews = Review.objects.filter(movie_name=my_id)
        ordered = sorted(reviews, key=operator.attrgetter('review'), reverse=True)
        params['reviews'] = ordered
        params['query'] = query[0]
        return render(request, 'single.html', params)

    else:
        return render(request, 'single.html', params)


def test(request):
    print(getvalue('I Loved it:))))'))
    x = Review.objects.filter(movie_name=5)
    y = x.values('review')
    print(y)

    return render(request, 'index.html')


def search(request):
    query = request.GET.get('k')
    print(query)
    movies = Movie.objects.filter(title__icontains=query)
    stars = Movie.objects.filter(cast__icontains=query)
    directors = Movie.objects.filter(director__icontains=query)
    producers = Movie.objects.filter(producer__icontains=query)
    desc = Movie.objects.filter(desc__icontains=query)

    reviews = Movie.objects.none()

    # reviews_model = Review.objects.filter(review__icontains=query)
    # for i in reviews_model:
    #     obj = Movie.objects.get(pk=i.movie_name_id)
    #     reviews = list(chain(reviews, obj))
    # print(reviews)

    result = list(chain(movies, stars, desc, producers, directors, reviews))

    params = {
        'title': 'Results: ' + query,
        'query': result
    }
    return render(request, 'movies.html', params)

