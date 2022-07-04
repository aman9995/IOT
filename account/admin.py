from django.contrib import admin
from .models import Blogs, Leaderboard, Needy, Ngo, People, User, Forms, solved_cases

# Register your models here.
admin.site.register(User)
admin.site.register(Ngo)
admin.site.register(People)
admin.site.register(Blogs)
admin.site.register(Needy)
admin.site.register(Forms)
admin.site.register(solved_cases)
admin.site.register(Leaderboard)