from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create/",views.create,name="create"),
    path("detail/<int:listing_id>",views.detail,name='detail'),
    path("watchlist/",views.watchlist,name='watchlist'),
    path("add/<int:listing_id>",views.add,name='add'),
    path("remove/<int:listing_id>",views.remove,name='remove')
]
