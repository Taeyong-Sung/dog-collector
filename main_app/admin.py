from django.contrib import admin
# add Feeding to the import
from .models import Dog, Feeding, Toy

admin.site.register(Dog)
admin.site.register(Feeding)
admin.site.register(Toy)