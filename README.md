python-sockjsroom
=================

Add multi-room and multi-message type support for sockjs-tornado.


Installation
------------

The most easy way to install sockjsroom is to use PyPI:
```
pip install sockjsroom
```
It will also auto-install tornado and sockjs-tornado (if needed)

The alternative method is to clone this repository:
```
git clone https://github.com/Deisss/python-sockjsroom.git
```
And run setup:
```
python setup.py install
```

Will register sockjsroom into your local python repo.


Usage
-----

The most basic usage should be a chat system:

```python

#
# ------------------------------
#   sockjsroom example
# ------------------------------
#

from sockjsroom import SockJSRoomHandler

class MySocketHandler(SockJSRoomHandler):
    def initialize(self):
        self.roomId = "0"

    # SOCKJS DEFAULT FUNCTION

    def on_open(self, info):
        pass

    def on_close(self):
        self.on_leave()

    # SOCKJSROOM CUSTOM FUNCTION

    def on_join(self, data):
        """ Join timer system """
        # data => roomId
        self.initialize()

        self.roomId = str(data.roomId)

    def on_chat(self, data):
        """ Start timer for everybody """
        # data => message
        self.publishToRoom(self.roomId, "chat", {"message" : data.message})

    def on_leave(self):
        """ Quit timer system """
        if self.roomId != "0":
            self.leave(self.roomId)

        self.initialize()


#
# ------------------------------
#   This part is not specific
#   to sockjsroom. It's a
#   sockjs-tornado part
# ------------------------------
#

import tornado.web, tornado.ioloop

from sockjs.tornado import SockJSRouter

class dummyHandler(tornado.web.RequestHandler):
    """ Regular HTTP handler (unused) """
    pass

if __name__ == "__main__":
    # Create route (use MySocketHandler here)
    Router = SockJSRouter(MySocketHandler, "/chat")

    # Create tornado app
    app = tornado.web.Application(
        [(r"/", dummyHandler)] + Router.urls
    )

    # Listening to application
    app.listen(8585)

    # Start IOLoop
    tornado.ioloop.IOLoop.instance().start()
```
Now you can have not only **on_open**, **on_message** and **on_close**, 
but almost what you want (except on_message already used internally).

The system will do the json convertion for you directly, and helps you
threw publishing process by providing:

  * **publishToRoom** send message to everybody
  * **publishToMyself** send message to yourself
  * **publishToOther** send message to everybody else

With those, it may become simple to __publish data to subset of people__ with ease.

We also provide in example how to use it with default sockjs-tornado: as sockjsroom is built
on top of sockjs-tornado/tornado couple, the way for starting system, remains quite the same.



Full usage
----------
You can found a real usage, implementing a simple multi-room chat system here:

  * server: [here](https://gist.github.com/Deisss/7941149)
  * client: [here](https://gist.github.com/Deisss/7941180)

To run the server simply do ```python server.py```.
To run the client, put all file in same directory, navigate to this directory and do on the command line ```python -m SimpleHTTPServer 7979```

Navigate with browser to [localhost:7979](http://localhost:7979) and you should be able to run the example.


Furthermore
-----------

You can found an exaustive presentation of code, and possibilities [here](http://simplapi.wordpress.com/2013/09/22/sockjs-on-steroids/)
