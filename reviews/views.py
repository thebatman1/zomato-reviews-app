from django.shortcuts import render, redirect
from django.http import HttpResponse
import requests
from reviews.forms import RegistrationForm, CreateReview
from django.contrib.auth.forms import AuthenticationForm 
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
import json
from . models import Review
from django.utils import timezone
import os
from django.contrib.auth.models import User

# TODO: Hide this key
API_KEY = os.environ['ZOMATO_API_KEY']
CITY_ID = 4  # For Bengaluru


def index(request):
    '''
        This view returns the main or the home page of the app
    '''
    return render(request, 'reviews/index.html')


def login_view(request):
    '''
        This function handles both the GET and POST requests to the 
        /login url.
        If it is a GET request, the method just renders the empty form
        If it is a POST request,
        - The form is validated
        - The user is redirected to index
    '''
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)        
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            # Checking from where the user has come from
            # and redirecting suitably
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            else:
                return redirect('reviews:dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'reviews/login.html', {'form':form})
    


def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('reviews:login')
    else:
        form = RegistrationForm()
    args={'form': form}
    return render(request, 'reviews/register.html', args)


@login_required(login_url='/reviews/login/')
def logout_view(request):
    logout(request)
    return redirect('/reviews')


@login_required(login_url='/reviews/login/')
def dashboard_view(request):
    '''
        This function handles the rendering of the dashboard
        - If the request method is GET, 
            the user is able to select some params 
            and make an AJAX POST call to this url
        - If the request method is POST,
            api call is made with the parameters
            and the response is returned to the AJAX 
            that then populates the views
    '''

    # headers for the zomato API
    headers = {
            'Accept' : 'application/json',
            'user-key' : API_KEY
    }
    # params for the zomato API
    params = {}

    if request.method == 'POST':
        cuisines_get = request.POST['cuisines']
        categories_get = request.POST['categories']
        establishments_get = request.POST['establishments']
        query = request.POST['query']

        # Check if any of the strings is empty
        if cuisines_get:
            params['cuisines'] = cuisines_get
        
        if categories_get:
            params['category'] = categories_get

        if establishments_get:
            params['establishment_type'] = establishments_get
        
        if query:
            params['q'] = query

        params['entity_id'] = CITY_ID
        params['entity_type'] = 'city'
        params['sort'] = 'rating'
        params['order'] = 'desc'

        search_results = requests.get(
            'https://developers.zomato.com/api/v2.1/search',
            headers=headers,
            params=params
        )

        # return the search results to the AJAX to populate
        # the list
        return HttpResponse(search_results)
    else:
        params['city_id'] = CITY_ID

        # get the categories from the API
        categories = json.loads(requests.get(
            'https://developers.zomato.com/api/v2.1/categories',
            headers=headers
        ).text)['categories']
    

        # get the cuisines from the API
        cuisines = json.loads(requests.get(
            "https://developers.zomato.com/api/v2.1/cuisines",
            headers=headers,
            params=params
        ).text)['cuisines']
    
        # get the establishments from the API
        establishments = json.loads(requests.get(
            "https://developers.zomato.com/api/v2.1/establishments",
            headers=headers,
            params=params
        ).text)['establishments']
    
        # return the form to select the params
        return render(
            request, 
            'reviews/dashboard.html', 
            {'categories':categories,
            'cuisines':cuisines,
            'establishments':establishments}
        )


@login_required(login_url='/reviews/login/')
def place_view(request, restaurant_id):
    '''
        If the request method is POST
        - User's review is submitted to the db and the reviews are refreshed
        If the request method is GET
        - The page is populated with the details of the restaurant
    '''
    # headers for the zomato API
    headers = {
            'Accept' : 'application/json',
            'user-key' : API_KEY
    }
    # params for the zomato API
    params = {}
    params['res_id'] = restaurant_id
    if request.method == 'POST':
        review_text = request.POST['review_text']
        rating = request.POST['rating']

        author = request.user.get_username() 
        
        print(type(author))
        review = Review(restaurant_id=restaurant_id,
            username=author,
            rating=rating,
            description=review_text,
            timestamp=timezone.now())
        review.save()
        print(review)
        return HttpResponse("Success")
    else:
        restaurant_details = json.loads(requests.get(
            "https://developers.zomato.com/api/v2.1/restaurant",
            headers=headers,
            params=params
        ).text)
        reviews = json.loads(requests.get(
            "https://developers.zomato.com/api/v2.1/reviews",
            headers=headers,
            params=params
        ).text)['user_reviews']
        stored_reviews = Review.objects.filter(restaurant_id=restaurant_id).values()
        print(type(stored_reviews))
        print(stored_reviews)
    return render(request, 
        'reviews/place.html', 
        {
            'res_id':restaurant_id,
            'details':restaurant_details,
            'reviews': reviews,
            'stored_reviews': stored_reviews,
            'username': request.user.get_username()
        })