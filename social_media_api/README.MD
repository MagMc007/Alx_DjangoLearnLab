# Social Media API Documentation

## 1. Authentication  

### A. Register  

**Description:**  
Creates a new user account. Returns a token for authentication on success. 


**Endpoint:**   POST /accounts/register/
 

**Request (JSON):**  
```json
{
    "username": "johndoe",
    "email": "john@doe.com",
    "password": "johnydoe"
}
```
Success Response (201 Created):
```json
{
    "user": {
        "username": "johndoe",
        "email": "john@doe.com"
    },
    "token": "b3edbdf3c45a13c5582740de1d48648978a4f7a1"
}
```
Error Response (400 Bad Request):    
(incase of a used username)
```json
{
    "username": [
        "A user with that username already exists."
    ]
}
```

### B. Login

**Description:**
 Authenticates a user and returns a token with user details.


**Endpoint:** POST /accounts/login/

  
**Request (JSON):**  
```json
{
    "username": "johndoe",
    "password": "johnydoe"
}
```
Success Response (200 OK):
```json
{
    "token": "b3edbdf3c45........82740de1d48648978a4f7a1",
    "user": {
        "id": 5,
        "username": "johndoe",
        "email": "john@doe.com",
        "bio": "",
        "profile_picture": null,
        "following_count": 0
    }
}
```
Error Response (400 Bad Request):
```json
{
    "non_field_errors": [
        "Invalid credentials"
    ]
}
```

### C. Profile

**Description:**
Fetches the authenticated user’s profile. Requires a valid token.

**Endpoint:**   GET /accounts/profile/


**Notice:**

- Set Authorization → Type = No Auth.

- Go to the Headers tab.

- Add a header:

  - Key: Authorization

  - Value: Token 12...34 (replace with your actual token).
Success Response (200 OK):
```json
{
    "id": 5,
    "username": "johndoe",
    "email": "john@doe.com",
    "bio": "",
    "profile_picture": null,
    "following_count": 0
}
```

Error Response (401 Unauthorized):

```json
{
    "detail": "Invalid token."
}
```

## 2.Posting and comments
**Note that you must be authenticated like in profile above to be able to view the ones below**

### A.Posting
**Description:**
An authenticated user can make a post.

**Endpoint:** POST  /contents/post/

**Request (json):**
```json
{
    "title": "My First Post",
    "author": 5,
    "content": "Hello world! This is my first post."
}
```
Success Response (201 CREATED):

```json
{
    "id": 2,
    "title": "My First Post",
    "author": 5,
    "content": "Hello world! This is my first post.",
    "comments": [],
    "likes_count": 0
}
```
Error Response (400 Bad Request):
```json
{
    "author": [
        "Invalid pk \"22\" - object does not exist."
    ]
}
```
or
```json 
{
    "title": "My First Post",
    "content": "Hello world! This is my first post."
}
```
## B. Getting Posts

**Description:**
Viewing all posts

**Endpoint:**  GET  /contents/post/1

**Request (json):** Not required

Success Response (200 OK):
```json
{
    "id": 1,
    "title": "My First Post",
    "author": 1,
    "content": "This is my post body.",
    "comments": [
        {
            "id": 1,
            "post": 1,
            "author": 3,
            "content": "Nice post!"
        }
    ],
    "likes_count": 0
}
```
**Using the above format you can perfom actions with with the provided request**
- delete: DELETE
- update: PUT (needs full json body)
- update: PATCH (needs partial json body)


## C. Commenting

**Description:**
An authenticated user can make a comment on a post. 

**Endpoint:**  POST /contents/comments/

**Request (json):**
```json
{
    "post": 1,
    "author": 2,
    "content": "Great post! Really enjoyed reading this."
}
```
Success Response (201 CREATED):

```json
{
    "id": 2,
    "post": 1,
    "author": 5,
    "content": "Great post! Really enjoyed reading this."
}
```
Error message will be 400   BAD_REQUEST with a  message error

## D. Getting Comments

**Description:**
User can make view comments under a post. 

**Endpoint:**  GET  /contents/comments/1/

**Request (json):** Not required

Success Response (200 OK):
```json
{
    "id": 2,
    "post": 1,
    "author": 5,
    "content": "Great post! Really enjoyed reading this."
}
```
**Using the above format you can perfom actions with with the provided request**
- delete: DELETE
- update: PUT (needs full json body)
- update: PATCH (needs partial json body)


## 3. Following and  unfollowing

**Note you must be authenticated to perform the ones below like in profile**

### A. Follwing

**Description:**
An authenticated user can follow other users.


**Endpoint:** POST  /accounts/follow/user_id/

Substitute the **user_id** 
with the id of the user you want to follow

**Request (json):** None

Success Response (200 OK):
```json
{
    "message": "You are now following johndoe"
}
```
In case you try to follow your self by inserting your own id

Error Response (400 Bad Request):
``` json
{
    "error": "You cannot unfollow yourself"
}
```
if you try to follow a user again
Error Response (400 Bad Request):
``` json
{
    "error": "You already follow this user"
}
```
if you try to follow a use that does not exist
Error Response (404 Not found):
``` json
{
     "error": "User not found"
}
```

### B. Unfollwing

**Description:**
Auser can unfollow other user it follows.


**Endpoint:** POST  /accounts/unfollow/user_id

Substitute the **user_id** 
with the id of the user you want to unfollow

**Request (json):** None

Success Response (200 OK):
```json
{
    "message": "You unfollowed johndoe"
}
```
In case you try to unfollow a use you donnot follow

Error Response (400 Bad Request):
``` json
{
    "error": "You do not follow this user"
}
```
In case you try to unfollow your self by inserting your own id

Error Response (400 Bad Request):
``` json
{
    "error": "You cannot unfollow yourself"
}
```
if you try to unfollow a use that does not exist
Error Response (404 Not found):
``` json
{
     "error": "User not found"
}
```

## 4. Feed

**Description:**
Feeds a user with the posts of the user it follows

**Endpoint:** GET  /contents/feed/


**Request (json):**
Not required
Success Response (200 OK):

```json
[
    {
        "id": 6,
        "title": "trial title 4",
        "author": 3,
        "content": "Trial content 4",
        "comments": [],
        "likes_count": 0
    },
    {
        "id": 1,
        "title": "My First Post",
        "author": 1,
        "content": "This is my post body.",
        "comments": [
            {
                "id": 1,
                "post": 1,
                "author": 3,
                "content": "Nice post!"
            },
]
```
If there is no post from the user if follows, user will get 
Success Response (200 OK) but an empty array
```json
{
    []
}
```

## 5. Like and Unlike
### A. Like
**Description:**
Allows user to like a post 

**Endpoint:** POST contents/post/post_id/like/

**Request (json):** Not required

Success Response (201 CREATED):

```json
{
    "detail": "Post liked successfully!"
}
```
If you try to like it again

Error Response (400 BAD REQUEST):
```json
{
    "detail": "You already liked this post."
}
```

### B. UnLike
**Description:**
Allows user to unlike a post 

**Endpoint:** POST contents/post/post_id/unlike/

**Request (json):** Not required

Success Response (200 OK):

```json
{
    "detail": "Unliked successfully"
}

```

if you try to unlike a post that you already unliked again

Error Response (404 NOT FOUND):
```json
{
    "detail": "No Like matches the given query."
}
```
## 6. Notifications
**Description:**
Provides notifications for a user 

**Trigger Logic:**
Notifications are automatically created when:
- A user comments on another user's post
- A user likes another user's post


### A. All notifications
**Endpoint:** GET notifications/notifications/
**Notice**
- make sure you have changed the user you are checking with on post man to get a populated notifcation result

**Request (json):**Not required

Success Response (200 OK):

```json
{
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 2,
            "actor": "johndoe",
            "verb": "commented on your post",
            "target": "Comment object (3)",
            "timestamp": "2025-08-21T12:45:22.792624Z",
            "is_read": false
        }
    ]
}
```
### B. Getting Individual Notification
**Request (json):** Not required

Success Response (200 OK):
```json
{
    "id": 2,
    "actor": "johndoe",
    "verb": "commented on your post",
    "target": "Comment object (3)",
    "timestamp": "2025-08-21T12:45:22.792624Z",
    "is_read": false
}
```

### C. Mark a Notification as Read
**Endpoint:** POST notifications/not_id/mark_read/  
Replace not_id with the notification id

**Request (json):** Not required  

**Success Response (200 OK):**
```json
{
    "detail": "Notification marked as read"
}

### D. Mark all Notification as Read
**Endpoint:** POST notifications/mark_all_read/  

**Request (json):** Not required  

**Success Response (200 OK):**
```json
{
        "detail": "All notifications marked as read"
}
