## Installation

You need to install first sockjsroom to get this example working.
Also, you may have a CORS error. As this example is quite simple, nothing is defined for this part. You may have the application "not doing" anything because of this.

## Running

On the main folder (where ```server.py``` is located), open a command prompt:

```sh
python -m SimpleHTTPServer 7979
```

Will start the server, navigate to [localhost:7979](http://localhost:7979) to see the system in action.

The main server (serving files, css, js) is located on port ```7979``` while the SockJS one, is on port ```7878```.

__This may cause some Origin Policy errors (CORS error)__. To correct that, the most simple way is to disable Origin Policy (only for testing purpose !), or use a proxy like HAProxy which will fake a single URL for both server (this is the recommanded way, way much better).

Basically, as SockJS run aside from official Tornado instance, you will always need to do something like this, on the other side, HAProxy is a killer tool, so just dig into, it will save some kittens !


## Elements to watch

There is several files in this example, yet, only few of them deserve a look:
  - **server.py**: This is the single server side element. Take a look at **ChatSocketHandler** which is the most important class here.
  - **js/socket.js**: This file is a wrapper around official SockJS data, it helps to create a kind of message/action object which is the core of SockJSRoom functionnality. You probably just need to copy it, without touching it.
  - **js/chat.js**: The main chat system (specific to chat system) is located here. This is the file you should definitely see and understand.


 Other files are less importants, some of them takes care of CSS, others of link between button and actions...
