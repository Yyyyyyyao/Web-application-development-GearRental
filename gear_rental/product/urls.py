from django.urls import path
from .views import deletefavourite,Addfavourite,UserFavouriteProduct,ProductSearchListView, ProductListView, ProductDetailView, ProductCreateView, ProductUpdateView, ProductDeleteView, UserProductListView, GalleryListView
from . import views # . is the current folder


urlpatterns = [
	#path('', views.home, name='blog-home'),
    path('', ProductListView.as_view(), name='product-home'),
    path('user/<str:username>', UserProductListView.as_view(), name='user-products'),
    path('user/<str:username>/fav/', UserFavouriteProduct.as_view(), name='favourite-products'),
    path('user/<str:username>/<int:pk>/addfav/', Addfavourite, name='add-favourite-products'),
    path('user/<str:username>/<int:pk>/delfav/', deletefavourite, name='del-favourite-products'),
    path('search/', ProductSearchListView.as_view(), name='search-products'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product-detail'), # <int:pk> is the integer of primary key
    path('product/new/', ProductCreateView.as_view(), name='product-create'),
    path('product/<int:pk>/update/', ProductUpdateView.as_view(), name='product-update'),
    path('product/<int:pk>/delete/', ProductDeleteView.as_view(), name='product-delete'),
    path('gallery',GalleryListView.as_view(), name='gallery'),
    path('about/', views.about, name='product-about'), # match /about/

]
