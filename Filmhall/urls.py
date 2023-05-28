from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='home'),
    path('createacc/', views.singup_user, name='signup'),
    path('login/', views.login_user, name='loginUser'),
    path('logout/', views.log_out, name='logout'),
    path('adminpage/', views.add_movie, name='adminpage'),
    path('makeshow/', views.makeShow, name='makeshow'),
    path('movies/<int:id>/review/', views.review, name='review'), 
    path('releasing/', views.releasing, name='releasing'),
    path('next/', views.nextRelease, name='next'),
    path('releasing/<int:id>/', views.updateMovie, name='updateMovie'),
    path('releasing/<int:id>/delete/', views.deleteMovie, name='deleteMovie'),
    path('book/<int:path>/', views.booking_seat, name='book'),
    path('movies/<int:id>/', views.moviebook, name="movie"),
    path('movies/<int:id>/review/', views.review, name="review"),
    path('movies/<int:id>/review/<int:path>/', views.updateReview, name="reviewUpdate"),
    path('movies/<int:id>/review/<int:path>/delete/', views.deleteReview, name="deleteReview"),
]
