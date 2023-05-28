from django.shortcuts import render, redirect
from .form import CreateUserForm
from django.contrib.auth import authenticate, login, logout
from .models import Movie,Review,Show,Seat,Booking
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse

# Create your views here.
def check_admin(user):
   return user.is_superuser

def updateMovie(request, id):
    if request.user.is_superuser:
        if request.method == "POST":
            name = request.POST['name']
            poster = request.FILES['picture']
            details = request.POST['details']
            stars = request.POST['stars']
            run_time = request.POST['run_time']
            IMDB_rating = request.POST['IMDB_rating']
            release = request.POST['release']
            status = request.POST['status']

            Movies = Movie(
                id = id,
                name=name,
                poster=poster,
                details=details,
                stars=stars,
                run_time=run_time,
                IMDB_rating=IMDB_rating,
                release=release,
                status=status,
            )

            Movies.save()
            return redirect('releasing')
    movie = Movie.objects.get(id=id)
    return render(request, 'Registration/updatemovie.html', {'movie':movie, })

def deleteMovie(request, id):
    Movie.objects.filter(id=id).delete()
    return redirect('releasing')

def add_movie(request):
    if request.user.is_superuser:
        if request.method == "POST":
            name = request.POST['name']
            poster = request.FILES['picture']
            details = request.POST['details']
            stars = request.POST['stars']
            run_time = request.POST['run_time']
            IMDB_rating = request.POST['IMDB_rating']
            release = request.POST['release']
            status = request.POST['status']

            Movies = Movie(
                name=name,
                poster=poster,
                details=details,
                stars=stars,
                run_time=run_time,
                IMDB_rating=IMDB_rating,
                release=release,
                status=status,
            )

            Movies.save()
            messages.success(request, 'Movie was created successfully!')
            return redirect('adminpage')
    
        movie = Movie.objects.all()
        context = {
            'Movie':movie
        }
    else:
        messages.warning(request, 'Only admin can enter the page')
        return redirect('loginUser')
    return render(request, 'Registration/admin.html', context)

def makeShow(request):
    if request.user.is_superuser:
        if request.method == "POST":
            selected_movie = Movie.objects.get(pk=request.POST['mov'])
            date = request.POST['date']
            time = request.POST['show_time']

            Shows = Show(
                date=date,
                start_time=time,
                movie_id=selected_movie,
            )
            Shows.save()
            return redirect('makeshow')
    movie = Movie.objects.filter(status="Releasing")
    return render(request, 'Registration/makeShow.html', {'movie':movie})

def index(request):
    movie = Movie.objects.all()
    context = {
        'movie':movie,
    }
    return render(request, 'Registration/home.html', context)

def singup_user(request):
    #default user creation form
    form = CreateUserForm()

    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
    context = {
        'form':form
    }
    return render(request, 'Registration/signup.html', context)

def login_user(request):  
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            print(username+" "+password)
            login(request, user)
            return redirect('home')
        else:
            messages.warning(request, 'Log In Error')
    return render(request, 'Registration/login.html')

def log_out(request):
    logout(request)
    return redirect('loginUser')

@login_required
def moviebook(request, id):
    if request.user.is_authenticated:
        movie = Movie.objects.get(id=id)
        review = Review.objects.filter(movie_id=id)
        reviewFiltered = Review.objects.filter(user_id=request.user, movie_id=id)
        show = Show.objects.filter(movie_id=id)
        context = {
            'movie':movie,
            'review':review,
            'reviewFiltered':reviewFiltered,
            'show':show,
        }
        return render(request, 'Registration/movie.html', context)

@login_required 
def booking_seat(request, path):
    if request.user.is_authenticated:
        if request.method == 'POST':
            user = request.user
            selected_seats = request.POST.getlist('seats')
            show = Show.objects.get(id=path)

            booked_seats = Booking.objects.filter(show=show).values_list('seat__id', flat=True)
            # Get a list of booked seat IDs for the show

            bookings = []
            for seat in selected_seats:
                if seat not in booked_seats:
                    booking = Booking(
                        user=user,
                        seat=Seat.objects.get(id=seat),
                        show=show,
                    )
                    bookings.append(booking)
            Booking.objects.bulk_create(bookings)
            return HttpResponse('Seats Selected Please contact the hall on time!!!!')
        
        available_seats = Seat.objects.exclude(id__in=Booking.objects.filter(show=path).values_list('seat__id', flat=True))
        # Get a queryset of available seats for the show
        seat = Seat.objects.all()
        show = Show.objects.get(id=path)
        context = {
            'seatSelected':seat,
            'seats': available_seats,
            'show': show,
        }
        return render(request, 'Registration/seat_chart.html', context)

def releasing(request):
    if request.user.is_authenticated:
        movie = Movie.objects.filter(status="Releasing")
        context = {
            'movie':movie,
        }
        return render(request, 'Registration/releasing.html', context)
    else:
        messages.warning(request, 'Log in first')
        return redirect('loginUser')
    
def nextRelease(request):
    if request.user.is_authenticated:
        movie = Movie.objects.filter(status="Next")
        context = {
            'movie':movie,
        }
        return render(request, 'Registration/next.html', context)
    else:
        messages.warning(request, 'Log in first')
        return redirect('loginUser')

#create reviews
def review(request, id):
    if request.method == "POST":
        user = request.user
        movie = Movie.objects.get(pk=id)
        message = request.POST['review']
        
        Reviews = Review(
            review=message,
            movie_id=movie,
            user_id=user,
        )

        Reviews.save()
        return redirect('movie', id=id)
    return render(request, 'Registration/movie.html', {"movie_id":id})

#update users review:
def updateReview(request, id, path):
    if request.method == "POST":
        user = request.user
        movie = Movie.objects.get(pk=id)
        message = request.POST['reviewUpdate']
            
        Reviews = Review(
            id = path,
            review=message,
            movie_id=movie,
            user_id=user,
        )

        Reviews.save()
        return redirect('movie', id=id)
    return render(request, 'Registration/movie.html', {"movie_id":id})


def deleteReview(request, id, path):
    Review.objects.filter(id=path).delete()
    return redirect('movie', id=id)