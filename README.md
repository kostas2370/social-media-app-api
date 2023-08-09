
# About this project :

Netmindz is an exciting and ambitious project that is currently in the active development stage, poised to revolutionize the social media landscape within university communities. Leveraging the power of Django Rest Framework, WebSockets, and Celery, Netmindz's backend API is designed to create a seamless and engaging platform for university students and faculty. Through Django Rest Framework, the API provides a structured and efficient way to manage data, ensuring secure and consistent interactions. The integration of WebSockets introduces real-time communication, enabling instant updates on posts, comments, and notifications, fostering a vibrant and interactive virtual campus. Complementing this, Celery facilitates the background processing of tasks, ensuring optimal performance even during peak usage. As Netmindz continues its journey towards completion, its backend API, skillfully combining Django Rest Framework, WebSockets, and Celery, promises to redefine the university social media experience, fostering meaningful connections and enhancing collaboration among its users.

# Endpoints :

**For register Login**

   >api/token/  : End point for login
   >api/token/refresh/ : For refreshing the token
   >api/register/  : for registration
   >api/email-verify/ : for email verification

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

    REQUIRED_FIELDS = ["email", "date_of_birth"]

```
