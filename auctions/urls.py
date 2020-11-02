from django.urls import include,path

from . import views

watchlist_patterns = [
    path("",views.watchlist,name='watchlist'),
    path("add/<int:listing_id>",views.add,name='add'),
    path("remove/<int:listing_id>",views.remove,name='remove')
]

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create/",views.create,name="create"),
    path("detail/<int:listing_id>",views.detail,name='detail'),
    path("bid/<int:listing_id>",views.bid,name='bid'),
    path("watchlist/",include(watchlist_patterns)),
    path("close/<int:listing_id>",views.close,name='close'),
    path('comment/<int:listing_id>',views.comment,name='comment'),
    path('delete_comment/<int:listing_id>/<int:comment_id>',views.delete_comment,name='delete_comment'),
    path('category/<int:category_id>',views.category,name='category')
]

