python-sockjsroom
=================

Add multi-room and multi-message type support for sockjs-tornado.


Installation
------------

The most easy way to install sockjsroom is to use Pypi:
```
pip install sockjsroom
```
It will also auto-include tornado and sockjs-tornado

The alternative method is to clone this repository:
```
git clone https://github.com/Deisss/python-sockjsroom.git
```
And run setup:
```
python setup.py install
```



Usage
-----

The most basic usage can be a Ping system:

```python
from sockjsroom import SockJSDefaultHandler


class PingSocketHandler(SockJSDefaultHandler):
    """ Ping system """
    def on_open(self, info):
        pass

    def on_message(self):
        pass

    def on_close(self):
        pass
```

This example does only create an empty handler, without any room support.

Here a more complete example using room support:

```python
from sockjsroom import SockJSRoomHandler

class MySocketHandler(SockJSRoomHandler):
    def initialize(self):
        self.roomId = "0"

    # SOCKJS DEFAULT FUNCTION

    def on_open(self, info):
        pass

    def on_close(self):
        self.on_leave()

    # SOCKJS CUSTOM FUNCTION

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
```
Now you can have not only **on_open**, **on_message** and **on_close**, 
but almost what you want (except on_message already used internally).

The system will do the json convertion for you directly, and helps you
threw publishing process by providing:

  * **publishToRoom** send message to everybody
  * **publishToMyself** send message to yourself
  * **publishToOther** send message to everybody else

With those, it may become simple to publish data to subset of people with ease.



Furthermore
-----------

You can found an exaustive presentation of code, and possibilities [here](http://simplapi.wordpress.com/2013/09/22/sockjs-on-steroids/)
