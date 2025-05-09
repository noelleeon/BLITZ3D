from django.contrib import admin
from .models import Member
from .models import Articles
from .models import Author
from .models import Message

admin.site.register(Member)
admin.site.register(Articles)
admin.site.register(Author)
admin.site.register(Message)
# Register your models here.
