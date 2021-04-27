from django.contrib import admin
from .models import Product

class ProductModelAdmin(admin.ModelAdmin):
	list_display = ["title", "date_posted"]

	list_display_links = ["date_posted"]
	list_filter = ["last_updated", "date_posted"]
	search_fields = ["title", "description"]

	list_editable = ["title"]

	class Mata:
		model = Product

admin.site.register(Product, ProductModelAdmin)

