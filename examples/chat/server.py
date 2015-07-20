#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, logging, tornado.web
from datetime import datetime
from sockjs.tornado import SockJSRouter
from sockjsroom import SockJSRoomHandler



class ChatSocketHandler(SockJSRoomHandler):
    ''' Basic chat system '''
    #
    # ---------------------------
    #   CLASS INIT
    # ---------------------------
    #
    def initialize(self):
        ''' Initialize any new connection '''
        self.roomId   = '-1'
        self.username = ''

    #
    # ---------------------------
    #   SOCKJS DEFAULT FUNCTION
    # ---------------------------
    #
    def on_open(self, info):
        pass

    def on_close(self):
        self.on_leave()

    #
    # ---------------------------
    #   SOCKJS CUSTOM FUNCTION
    # ---------------------------
    #
    def on_join(self, data):
        # data => username, roomId
        self.initialize()

        self.roomId = str(data['roomId'])
        self.username = str(data['username'])

        # Joining room
        self.join(self.roomId)

        # TODO: on real system, we should here check login/password
        # can access to roomId

        # TODO: on a real system, we should use self.publishToMyself
        # to send back latest 100 chat sended (for example) on this room

        # Say to other users a new user enter room
        self.publishToOther(self.roomId, 'join', {
            'username': self.username
        })


    def on_chat(self, data):
        ''' Transfert a message to everybody '''
        # XXX: we cannot use on_message as it's 'official' one already used
        # by sockjsroom to create multiple on_* elements (like on_chat),
        # so we use on_chat instead of on_message

        # data => message
        if self.roomId != '-1':
            self.publishToRoom(self.roomId, 'chat', {
                'username': self.username,
                'time': datetime.now(),
                'message': str(data['message'])
            })


    def on_leave(self):
        ''' Quit chat room '''
        # Only if user has time to call self.initialize
        # (sometimes it's not the case)
        if self.roomId != '-1':
            # Debug
            logging.debug('chat: leave room (roomId: %s)' % self.roomId)

            # Say to other users the current user leave room
            self.publishToOther(self.roomId, 'leave', {
                'username': self.username
            })

            # Remove sockjsroom link to this room
            self.leave(self.roomId)

        # Erasing data
        self.initialize()













class IndexHandler(tornado.web.RequestHandler):
    ''' Regular HTTP handler (unused) '''
    pass

def configureLogger(logFolder, logFile):
    ''' Start the logger instance and configure it '''
    # Set debug level
    logLevel = 'DEBUG'
    logger = logging.getLogger()
    logger.setLevel(logLevel)

    # Format
    formatter = logging.Formatter('%(asctime)s - %(levelname)s | %(name)s -> %(message)s', '%Y-%m-%d %H:%M:%S')

    # Remove default handler to keep only clean one
    for hdlr in logger.handlers:
        logger.removeHandler(hdlr)

    # Create missing folder if needed
    if not os.path.exists(logFolder):
        os.makedirs(logFolder, 0700)

    #
    # ----------------------------
    #   CREATE CONSOLE HANDLER
    # ----------------------------
    #

    # Create console handler
    consoleh = logging.StreamHandler()
    consoleh.setLevel(logLevel)
    consoleh.setFormatter(formatter)

    # Set our custom handler
    logger.addHandler(consoleh)

    #
    # ----------------------------
    #   CREATE FILE HANDLER
    # ----------------------------
    #
    fileh = logging.FileHandler(logFile, 'a')
    fileh.setLevel(logLevel)
    fileh.setFormatter(formatter)

    # Set our custom handler
    logger.addHandler(fileh)

def printWelcomeMessage(msg, place=10):
    ''' Print any welcome message '''
    logging.debug('*' * 30)
    welcome = ' ' * place
    welcome+= msg
    logging.debug(welcome)

    logging.debug('*' * 30 + '\n')













if __name__ == '__main__':
    serverPort = 7878

    logFile   = './application.log'
    logFolder = os.path.dirname(logFile)
    configureLogger(logFolder, logFile)

    # Print logger message
    logging.debug('\n\nSystem start at: %s\nSystem log level: %s\n' % (datetime.now(), 'DEBUG'))
    printWelcomeMessage('STARTING', 11)
    printWelcomeMessage('SETUP ROUTES', 8)

    # Create route
    chatRouter  = SockJSRouter(ChatSocketHandler,  '/chat')

    # Create tornado app
    app = tornado.web.Application([
                (r'/', IndexHandler),
         ]
                + chatRouter.urls
                #XXX: add + myRouter.urls here to add more class
    )

    # Listening port
    app.listen(serverPort)
    printWelcomeMessage('SERVER RUNNING ON PORT %i' % serverPort, 1)

    # Start IOLoop
    tornado.ioloop.IOLoop.instance().start()
