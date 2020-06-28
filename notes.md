# Some notes for rest api using flask
---

### Http
* Whenever we visit a website we make a `GET` request from our browser to a remote server.

* Some of the common http methods are
    - `GET` `POST` `PUT` `DELETE` `OPTIONS` `HEAD` and much more.

`GET` : retrieve something
`POST` : Receive data and use it
`PUT` : make sure the item is there
`DELETE` : remove something


## Rest Principles

* It's a way of thinking of how web server will respond to your request.
* It dosen't respond with just data
* It responds with resources

## Rest is Stateless

**what does this mean ?**

- It means one request cannot depend on any other resource.
- The server only knows about the current request not the previous one.

## Flask offers some tools for creating api's in more standard way i.e Flask-RESTful

### A common term often pop's up i.e Resource which is nothing but the object with which our api will be interacting.

## Status codes

* `404` - not found
* `201` - resource created
* `200` - everything okay
* `202` - request accepted
* `400` - bad request. user fault




