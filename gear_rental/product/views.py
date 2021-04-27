from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
# from recommender.models import Userclick
from django.views.generic import (
	ListView, 
	DetailView, 
	CreateView,
	UpdateView,
	DeleteView
	)
from .models import Product
from recommender.models import Userclick
from recommender.views import recommendview
from django.db.models import Q
from users.models import Favourite,Profile
from distance.views import closetrecommends
from django.http import HttpResponseRedirect,HttpResponseNotModified
from distance.views import distance
import numpy as np
from django import forms
def home(request):
	context = {
		'products': Product.objects.all() # key: list of dics
	}
	return render(request, 'product/home.html', context)


class ProductSearchListView(ListView):
	model = Product
	template_name = "product/search_result.html"
	context_object_name = 'search_products'
	# paginate_by = 6
	def get_queryset(self):
		_title = self.request.GET.get('q')
		_cate = self.request.GET.get('cate')
		_postcode = self.request.GET.get('p')
		_range = self.request.GET.get('rang')
		lookups = None
		if _title:
			if lookups is None:
				lookups = Q(title__icontains=_title)
		if _cate:
			if _cate!='All':
				if lookups is None:
					lookups = Q(category__icontains=_cate)
				else:
					lookups = lookups&Q(category__icontains=_cate)
		if _postcode:
			if lookups is None:
				lookups = Q(postcode__icontains=_postcode)
			else:
				lookups = lookups&Q(postcode__icontains=_postcode)
		product = []
		# if lookups is None:
		# 		# lookups = Q(category__icontains=_cate)
		product = Product.objects.all()
		# else:
		# 	product = Product.objects.filter(lookups)
		if(not _cate  and not _postcode and not _range):
			if(_title):
				return Product.objects.filter(lookups)
			else:
				return Product.objects.all()
		
		dis = []
		idx = []
		user = self.request.user
		user_postcode = list(Profile.objects.filter(user=user).values_list('user_postcode',flat=True))
		if self.request.user.is_authenticated:
			if _range is not None :
				if int(_range) != 0 :
					for i in product.values_list('id','postcode'):
						if distance(user_postcode[0],i[1]) != "Sorry, distance unavailable":
							print()
							print(user_postcode[0])
							print(i[1])
							print(distance(user_postcode[0],i[1]))
							print(_range)
							
							if int(distance(user_postcode[0],i[1])) <= int(_range):
								print("In range")
								idx.append(i[0])
					if lookups is None:
						product =  Product.objects.filter(pk__in = idx)
					else:
						product = Product.objects.filter(lookups , pk__in = idx)
				else:
					if lookups is None:
						product = Product.objects.all()
					else:
						product = Product.objects.filter(lookups)		
		else:
			if lookups is None:
				product = Product.objects.all()
			else:
				product = Product.objects.filter(lookups)	
		return product
class UserFavouriteProduct(ListView):
	model = Product
	template_name = 'product/favourite_product.html'
	context_object_name = 'favourite_products'
	paginate_by = 6
	def get_queryset(self):
		user = get_object_or_404(User, username=self.kwargs.get('username'))
		pks = Favourite.objects.filter(user=user).values_list('product',flat=True)
		return Product.objects.filter(pk__in=pks).order_by('-date_posted')

def Addfavourite(request,username,pk):
	if not request.user.is_authenticated:
		return HttpResponseRedirect('/login/')
	user = get_object_or_404(User, username = username)
	product = Product.objects.get(pk=pk)
	#user = User.objects.filter(username = username)
	# favourite = get_object_or_404(Favourite, user = user)
	favourites = Favourite.objects.filter(user = user,product=product)
	

	if favourites.exists():
		favourites.delete()
	else:
		fav = Favourite(user=user,product=product)
		fav.save()


	return HttpResponseRedirect('/product/'+str(pk))
	# return HttpResponseNotModifiedon

def deletefavourite(request,username,pk):
	user = get_object_or_404(User, username = username)
	product = Product.objects.get(pk=pk)
	#user = User.objects.filter(username = username)
	# favourite = get_object_or_404(Favourite, user = user)
	favourites = Favourite.objects.filter(user = user,product=product)
	favourites.delete()
	return HttpResponseRedirect('/user/'+str(username)+'/fav/')
# def deletefavourite()

# list views (like Youtube) Video part10
class ProductListView(ListView):
	model = Product
	template_name = 'product/home.html' # <app>/<model>_<viewtype>.html (e.g. blog/post_list.html)
	context_object_name='products'
	ordering = ['-date_posted'] # this will make the post in inverse order
	paginate_by = 6 # http://127.0.0.1:8000/?page=2 (jump to page; ? means there will be parameters)
	def get_context_data(self,**kwargs):
		context = super().get_context_data(**kwargs)
		context['recommends'] = recommendview(self.request)
		if self.request.user.is_authenticated:
			context['close'] = closetrecommends(self.request)
		return context

class UserProductListView(ListView):
	model = Product
	template_name = 'product/user_products.html' # <app>/<model>_<viewtype>.html (e.g. blog/post_list.html)
	context_object_name='products'
	paginate_by = 6 # http://127.0.0.1:8000/?page=2 (jump to page; ? means there will be parameters)

	def get_queryset(self):
		user = get_object_or_404(User, username=self.kwargs.get('username'))
		print(user)
		return Product.objects.filter(author=user).order_by('-date_posted')

class ProductDetailView(DetailView):
	model = Product
	def get_context_data(self,**kwargs):
		context = super().get_context_data(**kwargs)

		is_fav = False
		if self.request.user.is_authenticated and Favourite.objects.filter(user=self.request.user,product=context['product']).exists():
			is_fav = True
		context['is_fav'] = is_fav
		# print(context)
		if self.request.user.is_authenticated:
			user = self.request.user.get_username()
			user = get_object_or_404(User, username=user)
			clicks_record = Userclick.objects.filter(user=user).order_by('created_at')
			if clicks_record.count() == 6:
				#delete old one	
				remained_id = clicks_record.values_list("pk",flat =True)[1:5]
				clicks_record.exclude(pk__in=list(remained_id)).delete()
			to_be_added = Userclick(user=self.request.user,product=context['product'])
			to_be_added.save()
			print("everthing all right")
		return context


class ProductCreateView(LoginRequiredMixin, CreateView):
	model = Product
	fields = ['title', 'description', 'price', 'postcode', 'availability', 'category', 'brand', 'image', 'image2', 'image3', 'image4']


	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):

	model = Product	

	fields = ['title', 'description', 'price', 'postcode', 'availability', 'category', 'brand', 'image', 'image2', 'image3', 'image4']
	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)

	def test_func(self):
		product = self.get_object()
		if self.request.user == product.author:
			return True
		return False

class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	model = Product
	success_url = '/'

	def test_func(self):
		product = self.get_object()
		if self.request.user == product.author:
			return True
		return False

def about(request):
	return render(request, 'product/about.html', {'title': 'About'})

class GalleryListView(ListView):
	model = Product
	template_name = 'product/gallery.html' # <app>/<model>_<viewtype>.html (e.g. blog/post_list.html)
	context_object_name='products'
	# ordering = ['-date_posted'] # this will make the post in inverse order
	# paginate_by = 6 # http://127.0.0.1:8000/?page=2 (jump to page; ? means there will be parameters)
	def get_queryset(self):
		all_post_size = Product.objects.all().count()
		random_choice = np.random.choice(all_post_size, 15, replace=False)
		all_post = list(Product.objects.all())
		chosen = []
		for i in range(15):
			chosen.append(all_post[random_choice[i]])
		return chosen