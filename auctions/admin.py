from django.contrib import admin

from .models import *


# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "id", "email")


class ListingAdmin(admin.ModelAdmin):
    list_display = ("title", "owner", "id", "date", "active", "category")


class BidAdmin(admin.ModelAdmin):
    list_display = ("member", "listing")


class CommentAdmin(admin.ModelAdmin):
    list_display = ("creater", "listing")


admin.site.register(User, UserAdmin)
admin.site.register(Listing, ListingAdmin)
admin.site.register(Bid, BidAdmin)
admin.site.register(Comment, CommentAdmin)
