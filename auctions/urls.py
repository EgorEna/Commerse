from django.urls import include,path

from . import views

watchlist_patterns = [
    path("",views.watchlist,name='watchlist'),
    path("add/<int:listing_id>",views.add,name='add'),
    path("remove/<int:listing_id>",views.remove,name='remove')
]

app_name = "auctions"

detail_actions_patterns = [
    path("",views.detail,name='detail'),
    path("bid",views.bid,name='bid'),
    path("close",views.close,name='close'),
    path("comment/",views.comment,name='comment'),
    path("<int:comment_id>/delete_comment",views.delete_comment,name='delete_comment'),
]

detail_patterns = [
    path("<int:listing_id>/",include(detail_actions_patterns))
]

urlpatterns = [
    path("create/",views.create,name="create"),
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("detail/",include(detail_patterns)),

    path("watchlist/",include(watchlist_patterns)),
    path('category/<str:category_name>',views.category,name='category')
]

