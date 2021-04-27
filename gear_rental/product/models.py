from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from PIL import Image
from django import forms
# MVC Model View Controller

class Product(models.Model):

	# title of the product
	title = models.CharField(max_length=100)

	# description of the product
	description = models.TextField()

	# price of the product
	price = models.PositiveIntegerField(default=0)

	# postcode of the product
	postcode = models.PositiveIntegerField(default=2000)

	# last updated date of the product
	last_updated = models.DateTimeField(auto_now=True, auto_now_add=False)

	# the date product was created
	date_posted = models.DateTimeField(default=timezone.now) #auto_now_add: time created not changable

	# the availaiblity of the product
	availability = models.BooleanField(default=True)

	# foreignkey connects to the User model
	author = models.ForeignKey(User, on_delete=models.CASCADE) # on_delete: if user is deleted, this post is deleted

	# the category of the product 
	LENCE = 'Lens'
	DSLR_CAMERA = 'DSLR Camera'
	OTHER_CAMERA = 'Other Camera'
	ACCESORY = 'Accesory'
	CATEGORY_CHOICES = [
        (LENCE, 'Lens'),
        (DSLR_CAMERA, 'DSLR Camera'),
		(OTHER_CAMERA, 'Other Camera'),
		(ACCESORY, 'Accesory'),
    ]
	category = models.CharField(
        max_length=13,
        choices=CATEGORY_CHOICES,
        default=DSLR_CAMERA,
    )

	# the brand of the product
	Nikon = 'Nikon'
	Canon = 'Canon'
	Sony = 'Sony'
	Casio = 'Casio'
	Panasonic = 'Panasonic'
	Pentax = 'Pentax'
	Lumix = 'Lumix'
	GoPro = 'GoPro'
	Olympus = 'Olympus'
	other_brand = 'Other Brand'
	BRAND_CHOICES = [
		(Nikon, 'Nikon'),
		(Canon, 'Canon'),
		(Sony, 'Sony'),
		(Casio, 'Casio'),
		(Panasonic, 'Panasonic'),
		(Pentax, 'Pentax'),
		(Lumix, 'Lumix'),
		(GoPro, 'GoPro'),
		(Olympus, 'Olympus'),
		(other_brand, 'Other Brand'),
	]
	brand = models.CharField(
        max_length=11,
        choices=BRAND_CHOICES,
        default=other_brand,
    )

	# Four Images 
	image = models.ImageField(default='des.png', upload_to='product_pics')

	image2 = models.ImageField(default='des.png', upload_to='product_pics')

	image3 = models.ImageField(default='des.png', upload_to='product_pics')

	image4 = models.ImageField(default='des.png', upload_to='product_pics')

	# regulize the size of the image
	# def save(self, *args, **kwargs):
	# 	super().save() # important

	# 	img = Image.open(self.image.path)

	# 	if img.height > 300 or img.width > 300:
	# 		output_size = (300, 300)
	# 		img.thumbnail(output_size)
	# 		img.save(self.image.path)

	# 	img2 = Image.open(self.image2.path)

	# 	if img2.height > 300 or img2.width > 300:
	# 		output_size = (300, 300)
	# 		img2.thumbnail(output_size)
	# 		img2.save(self.image2.path)

	# 	img3 = Image.open(self.image3.path)

	# 	if img3.height > 300 or img3.width > 300:
	# 		output_size = (300, 300)
	# 		img3.thumbnail(output_size)
	# 		img3.save(self.image3.path)

	# 	img4 = Image.open(self.image4.path)
	# 	if img4.height > 300 or img4.width > 300:
	# 		output_size = (300, 300)
	# 		img4.thumbnail(output_size)
	# 		img4.save(self.image4.path)

	# string return of the Product model
	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('product-detail', kwargs={'pk': self.pk})