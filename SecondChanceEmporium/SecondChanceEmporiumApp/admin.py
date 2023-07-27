from django.contrib import admin
from .models import *
# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return True

    def has_delete_permission(self, request, obj=None):
        return True

    def has_change_permission(self, request, obj=None):
        return True

class ShopUserAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return True

    def has_change_permission(self, request, obj=None):
        if obj:
            return request.user == obj.user_id


class ProductAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        if request.user:
            return True

    def has_delete_permission(self, request, obj=None):
        if obj and request.user == obj.seller.user_id and obj.seller.is_seller:
            return True

    def has_change_permission(self, request, obj=None):
        if obj and request.user == obj.seller.user_id and obj.seller.is_seller:
            return True


admin.site.register(Category, CategoryAdmin)
admin.site.register(ShopUser, ShopUserAdmin)
admin.site.register(Product, ProductAdmin)
