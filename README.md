
# About this project :

Netmindz is an exciting and ambitious project that is currently in the active development stage, poised to revolutionize the social media landscape within university communities. Leveraging the power of Django Rest Framework, WebSockets, and Celery, Netmindz's backend API is designed to create a seamless and engaging platform for university students and faculty. Through Django Rest Framework, the API provides a structured and efficient way to manage data, ensuring secure and consistent interactions. The integration of WebSockets introduces real-time communication, enabling instant updates on posts, comments, and notifications, fostering a vibrant and interactive virtual campus. Complementing this, Celery facilitates the background processing of tasks, ensuring optimal performance even during peak usage. As Netmindz continues its journey towards completion, its backend API, skillfully combining Django Rest Framework, WebSockets, and Celery, promises to redefine the university social media experience, fostering meaningful connections and enhancing collaboration among its users.

# Authentication :

Using the Simple JWT (JSON Web Token) Bearer authentication method offers several compelling advantages for securing your Django-based web application:

Stateless Authentication: Simple JWT Bearer authentication is stateless, meaning the server doesn't need to store session data. This reduces server overhead and allows for easy scalability, making it well-suited for distributed and microservices-based architectures.

Efficient and Lightweight: JWTs are compact, self-contained tokens that carry all necessary information, such as user identity and roles. This eliminates the need to repeatedly query the database for user information during each request, leading to improved performance.

Enhanced Security: JWTs are digitally signed, ensuring the integrity and authenticity of the token. This guards against tampering and unauthorized access. Additionally, you can configure token expiration and implement token refreshing to mitigate the risk of long-lived tokens.

Cross-Origin Compatibility: JWT Bearer tokens can be easily included in HTTP headers, making them compatible with various client types, including web browsers, mobile apps, and third-party integrations.

Scalability and Microservices: Simple JWT Bearer is well-suited for distributed and microservices-based applications, allowing different services to authenticate and authorize users without relying on a centralized session store.

Decoupled Architecture: JWT Bearer authentication promotes a decoupled architecture by not relying on server-side sessions. This enables easier integration with third-party services and APIs.

Flexibility: JWTs can carry custom claims, enabling you to include additional user-specific data in the token. This can reduce the need for subsequent database queries to fetch user details.

Token Revocation: While Simple JWT Bearer tokens are not revocable like session-based tokens, you can implement token blacklisting or leverage short-lived tokens combined with token refreshing to effectively manage token lifetimes and improve security.

Easy Implementation: The djangorestframework_simplejwt library provides a straightforward and well-documented way to implement JWT Bearer authentication in your Django application. The library abstracts much of the complexity, making it easy to get started.

In summary, using Simple JWT Bearer authentication in your Django application offers a combination of security, performance, and flexibility. By leveraging JWTs, you can streamline the authentication process, improve API performance, and enhance the overall security posture of your application.


# DB SCHEMA

![dsasd](https://github.com/kostas2370/social-media-app-api/assets/96636678/9a25b62d-8aec-4ae7-883e-acb863e3f567)


```scss
User
├─ id
├─ email
├─ date_of_birth
├─ profile_image
├─ sex
├─ friends (ManyToMany with User)
├─ is_public
├─ is_official
├─ is_verified
├─ is_staff
├─ is_active
├─ is_online
├─ REQUIRED_FIELDS

FriendRequest
├─ id
├─ from_user (ForeignKey: User)
├─ to_user (ForeignKey: User)
└─ accepted

Post
├─ id
├─ author (ForeignKey: User)
├─ title
├─ text
├─ upload_date
├─ is_public
└─ tags (TaggableManager)

PostImage
├─ id
├─ post (ForeignKey: Post)
└─ image

Comment
├─ id
├─ post (ForeignKey: Post)
├─ author (ForeignKey: User)
├─ release_date
└─ text

Like
├─ id
├─ post (ForeignKey: Post)
└─ user (ForeignKey: User)

Dislike
├─ id
├─ post (ForeignKey: Post)
└─ user (ForeignKey: User)

PostView
├─ id
├─ post (ForeignKey: Post)
├─ user (ForeignKey: User)
├─ ip
└─ times_count

University
├─ id
├─ name
├─ admin (ForeignKey: User)
├─ email_domain
├─ university_profile
└─ is_active

UniversityFollower
├─ id
├─ university (ForeignKey: University)
└─ user (ForeignKey: User)

UniversityReview
├─ id
├─ university (ForeignKey: University)
├─ user (ForeignKey: User)
├─ rating
├─ review
└─ reply

UniversityPost
├─ id
├─ university (ForeignKey: University)
├─ author (ForeignKey: User)
├─ title
├─ text
└─ upload_date

UniversityPostImage
├─ id
├─ post (ForeignKey: UniversityPost)
└─ image

Message
├─ id
├─ sender (ForeignKey: User)
├─ recipient (ForeignKey: User)
├─ message
├─ image
├─ created
└─ isRead
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
>api/post/<int:post_id>/update    PUT (if you want to add images , add it in your form as upload_Image)
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
   > 
   > api/university/<university:id>/follow/ POST
    
    
    
# TO DO :

1. I have to create the messages app, with Websockets.
2. Better filtering in get_feed
3. Test Cases for university
4. Improve mail format
5. User settings
6. Check for security issues
7. Add comment section in University Posts
8. Better Api Documentation
9. Filtering in bad words (racism etc)


    




