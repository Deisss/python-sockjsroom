# python-sockjsroom

Add multi-room and multi-message type support for sockjs-tornado.


## Installation

The most easy way to install sockjsroom is to use PyPI:
```
pip install sockjsroom
```
It will also auto-install tornado and sockjs-tornado. If, for any reason, they are not installed, you can do it manually:
```
pip install tornado sockjs-tornado
pip install sockjsroom
```

The alternative method is to clone this repository:
```
git clone https://github.com/Deisss/python-sockjsroom.git
```
And run setup:
```
python setup.py install
```

Will register sockjsroom into your local python repo.


## Interest

Now you can have not only **on_open**, **on_message** and **on_close**, 
but almost what you want (except on_message already used internally).
Every **on_*** will be consider as available from outside (from socket call),
please refer to example below for seeing it in action.

The system will also do the json convertion for you directly, and helps you
threw publishing process by providing:

  * **publishToRoom** send message to everybody (in the same room)
  * **publishToMyself** send message to yourself
  * **publishToOther** send message to everybody else (in the same room)

With those, it may become simple to __publish data to subset of people__ with ease.

As sockjsroom is built
on top of sockjs-tornado/tornado couple, the way for starting system, remains the same
compare to sockjs-tornado.



## Usage

You can found an implementation of a simple multi-room chat system here:

  * server: [here](https://gist.github.com/Deisss/7941149)
  * client: [here](https://gist.github.com/Deisss/7941180)

To run the server simply do ```python server.py```.
To run the client, put all file in same directory, navigate to this directory and do on the command line ```python -m SimpleHTTPServer 7979```

Navigate with browser to [localhost:7979](http://localhost:7979) and you should be able to run the example.


## Furthermore

You can found an exaustive presentation of code, and possibilities [here](http://simplapi.wordpress.com/2013/09/22/sockjs-on-steroids/)
