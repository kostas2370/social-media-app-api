
# About this project :

Netmindz is an exciting and ambitious project that is currently in the active development stage, poised to revolutionize the social media landscape within university communities. Leveraging the power of Django Rest Framework, WebSockets, and Celery, Netmindz's backend API is designed to create a seamless and engaging platform for university students and faculty. Through Django Rest Framework, the API provides a structured and efficient way to manage data, ensuring secure and consistent interactions. The integration of WebSockets introduces real-time communication, enabling instant updates on posts, comments, and notifications, fostering a vibrant and interactive virtual campus. Complementing this, Celery facilitates the background processing of tasks, ensuring optimal performance even during peak usage. As Netmindz continues its journey towards completion, its backend API, skillfully combining Django Rest Framework, WebSockets, and Celery, promises to redefine the university social media experience, fostering meaningful connections and enhancing collaboration among its users.

# DB SCHEMA

![dsasd](https://github.com/kostas2370/social-media-app-api/assets/96636678/9a25b62d-8aec-4ae7-883e-acb863e3f567)


# Models :
**User Model**

```python


    sex_choices =(('M', 'MALE'), ('F', 'FEMALE'), ('O', 'OTHER'))
    email = models.EmailField(unique = True)
    date_of_birth = models.DateField()
    profile_image = models.ImageField(default = "default.jpg",upload_to = "profile_pics")
    sex = models.CharField(default = 'O', choices =sex_choices, max_length = 1)
    friends = models.ManyToManyField("User", blank = True)
    is_public = models.BooleanField(default = True)
    is_official = models.BooleanField(default = False)
    is_verified = models.BooleanField(default = False)
    is_staff = models.BooleanField(default = False)
    is_active = models.BooleanField(default = True)
    is_online = models.BooleanField(default = False)

    REQUIRED_FIELDS = ["email", "date_of_birth"] Username and Password

```
**Friend Request Model**
```python
    id = models.AutoField(primary_key=True)
    from_user = models.ForeignKey(User, related_name = 'from_user', on_delete = models.CASCADE)
    to_user = models.ForeignKey(User, related_name = 'to_user', on_delete = models.CASCADE)
    accepted = models.BooleanField(default = False)

```

# Posts :

**Posts Model**

```python

    id = models.AutoField(primary_key=True)
    author = models.ForeignKey(User, on_delete = models.CASCADE, related_name = "posts")
    title = models.CharField(max_length = 110, blank = True, null = True)
    text = models.TextField(blank = True)
    upload_date = models.DateField(auto_now = True)
    is_public = models.BooleanField(default = False)
    tags = TaggableManager()
```

**Post Images Model**

```python

   post = models.ForeignKey(Post, on_delete = models.CASCADE, related_name = "post_images")
   image = models.ImageField(upload_to = "post_images", blank = True, null = True)
```


**Comments Model**

```python

    post = models.ForeignKey(Post, on_delete = models.CASCADE, related_name = "comments")
    id = models.AutoField(primary_key = True)
    author = models.ForeignKey(User, on_delete = models.CASCADE)
    release_date = models.DateField(auto_now = True)
    text = models.CharField(max_length = 300, blank = False, null = False)

```


**Likes Model**

```python

    post = models.ForeignKey(Post, on_delete = models.CASCADE, related_name = "likes")
    user = models.ForeignKey(User, on_delete = models.CASCADE)

```
**Dislikes Model**

```python

    post = models.ForeignKey(Post, on_delete = models.CASCADE, related_name = "dislikes")
    user = models.ForeignKey(User, on_delete = models.CASCADE)

```

**Post View Model**

```python

    post = models.ForeignKey(Post, on_delete = models.CASCADE, related_name = "views")
    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name = "viewer")
    ip = models.CharField(max_length = 15)
    times_count = models.IntegerField(default = 1)

```

# University :

**Universities Model**
```python

    id = models.AutoField(primary_key=True)
    name = models.CharField(unique = True, max_length = 60)
    admin = models.ForeignKey(User, on_delete = models.SET_NULL, null = True)
    email_domain = models.CharField(max_length = 50)
    university_profile = models.ImageField(default = "default.jpg", upload_to = "universities_pic")
    is_active = models.BooleanField(default = False)

```

**UniversityFollowers**

```python

    university = models.ForeignKey(Universities, on_delete = models.CASCADE)
    user = models.ForeignKey(User, on_delete = models.CASCADE)

```

**UniversityReviews Model :**

```python

    id = models.AutoField(primary_key= True)
    university = models.ForeignKey(Universities, on_delete = models.CASCADE)
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    rating = models.IntegerField(default = 1, validators = [MaxValueValidator(5), MinValueValidator(1)], blank = True)
    review = models.TextField(max_length = 500)
    reply = models.CharField(max_length = 500)

```

**UniversityPosts Model :**

```python

    id = models.AutoField(primary_key=True)
    university = models.ForeignKey(Universities, on_delete = models.CASCADE, related_name = "universities_posts")
    author = models.ForeignKey(User, on_delete = models.CASCADE)
    title = models.CharField(max_length = 110, blank = True, null = True)
    text = models.TextField(blank = True)
    upload_date = models.DateField(auto_now = True)

```

**UniversityPostImages Model :**

```python

    post = models.ForeignKey(Universities, on_delete = models.CASCADE, related_name = "university_post_images")
    image = models.ImageField(upload_to = "university_post_images", blank = True, null = True)

```

**Messages model**

```python

    id = models.AutoField(primary_key= True)
    sender = models.ForeignKey(User, on_delete = models.CASCADE, blank = False, related_name= 'SenderToRec')
    recipient = models.ForeignKey(User, on_delete = models.CASCADE, blank = False, related_name ='recToSencer')
    message = models.CharField(max_length = 500, blank = False)
    image = models.ImageField(upload_to = "message_pics", blank = True, null = True)
    created = models.DateTimeField(auto_now_add = True)
    isRead = models.BooleanField(default = False)

```


# Endpoints :

**Login Endpoints**

   >api/token/  : POST
   >
   >api/token/refresh/ POST
   >
   >api/register/  : POST
   >
   >api/email-verify/ GET
   >
>

**User Endpoints**
   >api/sendrequest/<int:touserid>  POST
   >
   >api/acceptrequest/  PUT
   >
   >api/getrequest/  GET
   >
   >api/deletefriend/<int:friendid> DELETE
   >
   >api/getfriend/  GET
   >
   >api/getfriend/<int:otherid> GET
   >
   >api/user/<int:user_id>  GET
   >
   > api/user/  GET
>

**Post Endpoints**
>api/feed     GET
>
>api/post/new   POST
>
>api/post/    GET
>
>api/post/<int:post_id>/delete     DELETE
>
>api/post/<int:post_id>/update    PUT
>
>api/post/<int:post_id>/<int:image_id> DELETE
>
>api/post/<int:post_id>/like    POST
>
>api/post/<int:post_id>/dislike    POST    
>
>api/post/<int:post_id>/comment    POST
>


**University Endpoints**

   > api/university/<slug:slug>  GET
   >   
   > api/university/id/<int:id>' GET
   >   
   > api/university/ GET
   > 
   > api/university/register/  POST
   > 
   > api/university/review/ POST
    
    
    
     
    




