from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from product.models import Product
from phone_field import PhoneField
# Create your models here.

class Favourite(models.Model):
	#TODO add date
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	
	phone_number = PhoneField(blank=True, help_text='Contacting phone number')

	# add whatever field i want
	image = models.ImageField(default='default_u.jpg', upload_to='profile_pics')

	user_postcode = models.PositiveIntegerField(default=2000)

	def __str__(self):
		return f'{self.user.username} Profile'

	# def save(self, *args, **kwargs):
	# 	super().save() # important

	# 	img = Image.open(self.image.path)

	# 	if img.height > 300 or img.width > 300:
	# 		output_size = (300, 300)
	# 		img.thumbnail(output_size)
	# 		img.save(self.image.path)


# in order to make these change to database
# > python3 manage.py makemigrations
# > python3 manage.py migrate
# then do not forget to register model in users/admin.py 
###############################
# from .models import Profile
# Register your models here.
# admin.site.register(Profile)
###############################