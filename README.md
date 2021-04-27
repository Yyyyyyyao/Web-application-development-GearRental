# Web-application-development-GearRental
## Project teammates: Harris Yang, Aaron Gong, Edward Wang

## Project Ideas

### **Why Gear Rental**
> Ebay, amazon and gumtree are three main platforms which provide trading services in Australia. However, they do not have a rental service which allows users to release their products for rent or find something to rent. Therefore, our project is to fill this gap and create a rental information website.

### **What makes Gear Rental outstanding?**
* **User Management System**
> Each user has its own account. The website will store user’s personal information, the posts they released and the items they are in favourite. The user can access and manage their warehouse and favourite list. Users can also change their profiles and upload custom profile image they like.

* **Recommend System**
> Two recommend strategies are provided.

> For users who have not logged in, random product will be listed in recommend section.

> For users who have logged in, it will first retrieve users’ click records and favourite list, then recommend post that is similar to their interests. The algorithm is content based filtering and includes bag-of-words and distance metric (to calculate similarity) technique.

> Algorithm detail:
1. Retrieve all posts in database system.
2. Get feature from post including description and brand.
3. Delete stop words. For example, “that” “this” “and” etc.
4. Put feature into bag-of-words structure, i.e., ignore the position of the word.
5. Transfer the feature into count vector.
6. Calculate similarity using distance metric, here we use cosine similarity.
7. Find k most similar posts except the query one.
8. Return posts and render in recommend section.

* **Distance System / Map System**
> In each product detail page, there will be a map showing where the product is, which can tell users where product located roughly. This functionality invokes google map API.

> Distance System Implementation:
1. Construct Geodata table in database which includes suburb, postcode, longitude and latitude.
2. Populate database with australia data.
3. Implement distance function based on longitude and latitude.
4. Add support for search functionality.

> User can modify their locations in their profile. Eventually, users can search for products by a distance range in search filters.

* **Email System**
> Users can reset their password through email. For example, if a user forgets his password, he can enter the email he used to register and there will be a link sending to his mailbox; then the only thing he needs to do is to follow the link and set a new password.

> Users can contact the product owner quickly through the email sending functionality in product detail page. They only need to fill their names, emails and messages they want to send to the owner. When they click the send button, the email application in the user’s device will pop out.

## Pre-request packages
> pip3 install django

> pip3 install django-crispy-forms

> pip3 install django-phone-field

> pip3 install rake_nltk 

> pip3 install geopy 

> pip3 install pandas 

> pip3 install numpy

> pip3 install django-storages

> pip3 install scikit-learn

## To run the code
> /gear_rental/manage.py

run the code
> python3 manage.py runserver

then paste the web address to chrome and open
