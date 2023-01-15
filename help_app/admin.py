from django.contrib import admin

from .models import *

# Register your models here.
admin.site.register(User)
admin.site.register(Ticket_counter)
admin.site.register(Ticket)


class BranchInline(admin.TabularInline):
    model = Branch_user
    extra = 1


class BranchUserAdmin(admin.ModelAdmin):
    inlines = [
        BranchInline
    ]


admin.site.register(Branch, BranchUserAdmin)
