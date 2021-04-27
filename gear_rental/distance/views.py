from django.shortcuts import render, get_object_or_404
import geopy.distance
from .models import Geodata
from django.contrib.auth.models import User
from users.models import Profile
from product.models import Product 
import numpy as np
# Create your views here.
# a and b are two post code
def check(geoa,geob):
    a = None
    for i in geoa:
        if i[0] <= 90 and i[0]>= -90 and i[1]>=-180 and i[1]<=180 :
            a = (i[0],i[1])
            break
    b = None
    for i in geob:
        if i[0] <= 90 and i[0]>= -90 and i[1]>=-180 and i[1]<=180 :
            b = (i[0],i[1])
            break
    return a,b
def distance(a,b):
    geoa = Geodata.objects.filter(postcode = a).values_list('lat','lon')
    geob = Geodata.objects.filter(postcode = b).values_list('lat','lon')
    # print(geoa)
    # print(geob)
    geoa,geob = check(geoa,geob)
    if geoa is None or geob is None:
        return "Sorry, distance unavailable"
    return geopy.distance.vincenty(geoa,geob).km

def closetrecommends(request):
    products = Product.objects.all().values_list('id','postcode')
    # print(products)
    user = request.user
    user_postcode = list(Profile.objects.filter(user=user).values_list('user_postcode',flat=True))
    # print(user_postcode)

    dis = []
    idx = []
    for product in products:
        dis.append(distance(user_postcode[0],product[1]))
        idx.append(product[0])
    dis = np.asarray(dis)
    idx = np.asarray(idx)
    idx_dis = np.argpartition(dis, 3)
    ret_pk = []
    for i in idx_dis[0:3]:
        ret_pk.append(idx[i])
    print(idx_dis)
    print(ret_pk)
    return Product.objects.filter(pk__in = ret_pk)
