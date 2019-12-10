# My Picture Hobby aka pichobby
This is an api meant to combine my three hobbies.
<ul>
  <li>Photography,</li>
  <li>Programming in python, and</li>
  <li>Web design.</li>
</ul>
Am <em>not</em> an expert in all three, but have basic knowledge of all and have decided to combine them.

## The following is the url map
<ul>
  <li><strong>GET :</strong> /</li>
  <li><strong>GET :</strong> /login</li>
  <li><strong>POST :</strong> /add/user</li>
  <li><strong>GET :</strong> /guests</li>
  <li><strong>GET :</strong> /user/&ltusername&gt</li>
  <li><strong>POST :</strong> /pic/post</li>
  <li><strong>GET :</strong> /pics</li>
  <li><strong>GET :</strong> /pic/&ltpic_id&gt</li>
  <li><strong>POST :</strong> /comment/post</li>
  <li><strong>GET :</strong> /pic/&ltpic_id&gt/comments</li>
  <li><strong>POST :</strong> /pic/&ltpic_id&gt/like</li>
  <li><strong>GET :</strong> /pic/&ltpic_id&gt/likes</li>
  <li><strong>GET :</strong> /&ltusername&gt/mylikes</li>
</ul>

## The resource guide
#### 1. <strong>GET :</strong> /
This is the homepage that returns this documentation in html format

#### 2. <strong>GET :</strong> /login
Accepts basic authentication details of a user; <em>username</em> and <em>password</em>. An access token is returned for use in all subsequent requests. The access token is used in the authorization header in the format <em>Authorization: Bearer \<access_token\></em>

#### 3. <strong>POST :</strong> /add/user
Adds a user to the system. The details needed are; "name", "username", "email", "password".

#### 4. <strong>GET :</strong> /guests
Returns a dictionary of users present {"Users Present": [{"name": "myname", "username": "myusername", "email": "user@mail.com" }]}. The username and email must be unique values.

#### 5. GET :</strong> /user/\<username\>
Returns a user's details: {
    "name": "myname",
    "username": "myusername",
    "email": "user@mail.com"
} .

#### 6. POST :</strong> /pic/post
Posts a picture. Details needed are; "pic_id", which is the unique identifier of the picture and "link" , which is the location of the picture. The system does not store the pictures.

#### 7. <strong>GET :</strong> /pics
Returns a dictionary of all the pictures posted. {
    "Posted Pictures": [
        {
            "date": "2019-12-10T08:35:02.710375",
            "link": "/to/no/where",
            "pic_id": "pic1"
        },
        {
            "date": "2019-12-10T08:35:12.976921",
            "link": "/to/no/where",
            "pic_id": "pic2"
        }
    ]
} .

#### 8. GET :</strong> /pic/\<pic_id\>
Returns the details of a picture. {
    "date": "2019-12-10T08:35:02.710375",
    "link": "/to/no/where",
    "pic_id": "pic1"
} .

#### 9. POST :</strong> /comment/post
Posts a comment about a picture. What's required is the "pic_id", "ctext", which is the comment text, and the "username" of who commented.

#### 10. GET :</strong> /pic/\<pic_id\>/comments
Returns all comments on a picture. {
    "pic1 comments": [
        {
            "ctext": "no comment",
            "date": "2019-12-10T08:51:55.512439",
            "pic_id": "pic1",
            "username": "timk"
        },
        {
            "ctext": "no comment yet",
            "date": "2019-12-10T08:57:22.491245",
            "pic_id": "pic1",
            "username": "tim"
        }
    ]
} .

#### 11. POST :</strong> /pic/\<pic_id\>/like
Posts a like or a dislike for a picture. <strong>Detials:</strong> "like", which is a boolean value, true for a like and false for a dislike. "username", which is who liked/disliked.

#### 12. <strong>GET :</strong> /pic/\<pic_id\>/likes
Returns the likes and dislikes of a picture. {
    "pic1 likes and dislikes": [
        {
            "like": true,
            "pic_id": "pic1",
            "username": "timk"
        },
        {
            "like": false,
            "pic_id": "pic1",
            "username": "tim"
        }
    ]
} .

#### 13. GET :</strong> /\<username\>/mylikes
Returns the likes and dislikes made by the user, \<username\>. {
    "My Likes": [
        {
            "like": true,
            "pic_id": "pic1",
            "username": "timk"
        },
        {
            "like": false,
            "pic_id": "pic2",
            "username": "timk"
        }
    ]
}


## NOTE
All GET requests return a 200 OK status while the POST return a 201 CREATED status. All data exchanged is in JSON format unless otherwise stated in the documentation.

<p>For any enquiries contact me at <a mailto:njorogetimk@gmail.com>njorogetimk@gmail.com</a></p>
