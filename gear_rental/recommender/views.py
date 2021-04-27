import numpy as np
from django.shortcuts import render, get_object_or_404
from product.models import Product
from users.models import Favourite
from recommender.models import Userclick
from django.contrib.auth.models import User
import pandas as pd 
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
from rake_nltk import Rake
from django.views.generic import (
    ListView, 
    DetailView, 
    CreateView,
    UpdateView,
    DeleteView
    )

#TODO randon select chunk of product database if it is too big
def random_recommending(request):
    all_post_size = Product.objects.all().count()
    # select 5 from all product, careful with all post size less than 6
    random_choice = np.random.choice(all_post_size, 6, replace=False)

    all_post = list(Product.objects.all())
    chosen = []
    for i in range(6):
        chosen.append(all_post[random_choice[i]])
    return chosen
def content_based_recommending(request,fav,clicks):
    # we need favourite at most 2, clicks at most 6
    choice_fav = None
    choice_clicks = None
    fav_select_count = 2
    clicks_select_count = 4
    if fav.count() > 2:
        choice_fav = np.random.choice(fav.count(), 2, replace=False)
        choice_clicks = np.random.choice(clicks.count(), 4, replace=False)
    else:
        choice_fav = np.random.choice(fav.count(), fav.count(), replace=False)
        choice_clicks = np.random.choice(clicks.count(), 6-fav.count(), replace=False)
        fav_select_count = fav.count()
        clicks_select_count = 6-fav.count()
    all_post = list(Product.objects.values_list('title','description','brand','category'))
    df = pd.DataFrame(all_post, columns = ['title', 'description','brand','category']) 
    df['brand'] = df['brand'].map(lambda x: x.split(' '))
    df['category'] = df['category'].map(lambda x: x.split(' '))
    # df['price'] = df['price'].map(lambda x: x.split(' '))
    df['keywords']= ""
    # print(df)
    df = df.astype('object')
    for index, row in df.iterrows():
        
        desc = row['description']
        r = Rake()
        r.extract_keywords_from_text(desc)
        key_words_dict_scores = r.get_word_degrees()
        df.loc[index,'keywords'] = list(key_words_dict_scores.keys())
        # df.loc[index,'price'] = str(df.loc[index,'price'])

# dropping the Plot column
    df.drop(columns = ['description'], inplace = True)
    # print(df)
    df.set_index('title', inplace = True)
    df['bag_of_words'] = ''
    columns = df.columns
    for index, row in df.iterrows():
        words = ''
        for col in columns:
            if col!='bag_of_words':
                # if col != 'price':
                #     words = words + ' '.join((row[col]))+ ' '
                # else:
                #     words = words + row[col]+ ' '
                words = words + ' '.join((row[col]))+ ' '
                # print(row[col])
        # print(words)
        # print()
        df.loc[index,'bag_of_words'] = words
        
    df.drop(columns = [col for col in df.columns if col!= 'bag_of_words'], inplace = True)
    count = CountVectorizer()
    count_matrix = count.fit_transform(df['bag_of_words'])
    indices = pd.Series(df.index)
    cosine_sim = cosine_similarity(count_matrix, count_matrix)
    def recommend(title, cosine_sim = cosine_sim):
    
        recommended_product = []
        
        # gettin the index of the movie that matches the title
        idx = indices[indices == title].index[0]

        # creating a Series with the similarity scores in descending order
        score_series = pd.Series(cosine_sim[idx]).sort_values(ascending = False)

        # getting the indexes of the 10 most similar movies
        top_10_indexes = list(score_series.iloc[1:6].index)
        
        # populating the list with the titles of the best 10 matching movi  es
        for i in top_10_indexes:
            recommended_product.append(list(df.index)[i])
            
        return recommended_product
    # print(count_matrix)

    recommends = []
    # pk = list(fav.values_list('product'))[0]
    # title = Product.objects.filter(pk__in=pk).values_list('title',flat=True)
    # rec_gen = recommend(title[0])
    # for rec in rec_gen:
    #     recommends.append(rec)
    pk = list(clicks.values_list('product'))[0]
    title = Product.objects.filter(pk__in=pk).values_list('title',flat=True)
    rec_gen = recommend(title[0])
    for rec in rec_gen:
        recommends.append(rec)
    # for i in range(fav_select_count):
    #     # print(list(fav.values_list('product',flat=True))[choice_fav[i]])
    #     pk = list(fav.values_list('product'))[i]
    #     title = Product.objects.filter(pk__in=pk).values_list('title',flat=True)
    #     rec_gen = recommend(title[0])
    #     for rec in rec_gen:
    #         recommends.append(rec)
    # # print(recommends)

    # for j in range(clicks_select_count):
    # #    print(list(clicks.values_list('product',flat=True))[choice_clicks[j]])
    #    pk = list(clicks.values_list('product'))[j]
    #    title = Product.objects.filter(pk__in=pk).values_list('title',flat=True)
    #    rec_gen = recommend(title[0])
    #    for rec in rec_gen:
    #        recommends.append(rec)
    return Product.objects.filter(title__in=recommends)
# Create your views here.
def recommendview(request):
    # check if we staisfy content_based_recommending
    if request.user.is_authenticated:
        #get favourite list count and clicks count
        user = request.user.get_username()
        user = get_object_or_404(User, username=user)
        fav = Favourite.objects.filter(user=user)
        clicks = Userclick.objects.filter(user=user)
        # If we have less than 5, random recommend
        if fav.count()+clicks.count() < 6:
            # print("sss")
            return random_recommending(request)
        # print(str(fav.count()+clicks.count()))
        #return content_based_recommending(self.request,fav,clicks)
        # print("aaa")
        return content_based_recommending(request,fav,clicks)
        # print("bbb")
    return random_recommending(request)
