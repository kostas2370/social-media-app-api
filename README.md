
# About this project :

Netmindz is an exciting and ambitious project that is currently in the active development stage, poised to revolutionize the social media landscape within university communities. Leveraging the power of Django Rest Framework, WebSockets, and Celery, Netmindz's backend API is designed to create a seamless and engaging platform for university students and faculty. Through Django Rest Framework, the API provides a structured and efficient way to manage data, ensuring secure and consistent interactions. The integration of WebSockets introduces real-time communication, enabling instant updates on posts, comments, and notifications, fostering a vibrant and interactive virtual campus. Complementing this, Celery facilitates the background processing of tasks, ensuring optimal performance even during peak usage. As Netmindz continues its journey towards completion, its backend API, skillfully combining Django Rest Framework, WebSockets, and Celery, promises to redefine the university social media experience, fostering meaningful connections and enhancing collaboration among its users.

# Endpoints :

**Login Endpoints**

   >api/token/  : End point for login
   >
   >api/token/refresh/ : For refreshing the token
   >
   >api/register/  : for registration
   >
   >api/email-verify/ : for email verification


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
**Friend Request Model
```python
    id = models.AutoField(primary_key=True)
    from_user = models.ForeignKey(User, related_name = 'from_user', on_delete = models.CASCADE)
    to_user = models.ForeignKey(User, related_name = 'to_user', on_delete = models.CASCADE)
    accepted = models.BooleanField(default = False)

```
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
