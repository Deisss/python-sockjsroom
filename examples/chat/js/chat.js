/**
 * Create a new socket instance between client and server,
 * and start use it
 *
 * @method mySocketChatRoom
 *
 * @param roomId {String} A unique string to represent a single room
 * @param username {String} The username to use on this room
*/
function mySocketChatRoom(roomId, username) {
    var sckt = new socket('chat', true);

    // On every connect, the server 'loose' us
    // so we have to join again
    sckt.on('connect', function() {
        // Everytime a connect appear, we have to logon again
        this.emit('join', {
            username: username,
            roomId:   roomId
        });
    }, sckt);

    // Start socket instance
    sckt.connect();

    return sckt;
};


/**
 * Create a new chat room (with HTML content and so on...)
*/
function createNewChatRoom() {
    var roomId = $('#newRoomId').val(),
        username = $('#newUsername').val();

    // XXX: roomId should probably not be specified by client...
    if(roomId && username && roomId != '' && username != '') {
        // Create a new socket instance
        var sckt = mySocketChatRoom(roomId, username);

        // Create the html content (uber ugly way)
        var chatRoom  = $('<div>'),
            textRoom  = $('<div>'),
            inputRoom = $('<input>');

        chatRoom.addClass('chatRoom');

        chatRoom.append(textRoom);
        chatRoom.append(inputRoom);

        // On enter key, we send the message to server
        inputRoom.keyup(function(event) {
            if(event.keyCode == 13) {
               var message = inputRoom.val();
               inputRoom.val('');
               // XXX: we should trim message before testing '' value
               if(message && message != '') {
                    sckt.emit('chat', {
                        message: message
                    });
               }
            }
        });

        // On 'chat' receive, we update the textRoom
        sckt.on('chat', function(data) {
            var currentUser = $('<a>');
            currentUser.html(data.username);

            var currentMessage = $('<p>');
            currentMessage.html(data.message);

            textRoom.append(currentUser);
            textRoom.append(currentMessage);
        });

        // On 'leave/join' receive, we say to all other user who connect/disco
        sckt.on('join', function(data) {
            var currentUser = $('<small>');
            currentUser.html('User ' + data.username + ' enter room');
            textRoom.append(currentUser);
            textRoom.append($('<br>'));
        });
        sckt.on('leave', function(data) {
            var currentUser = $('<small>');
            currentUser.html('User ' + data.username + ' leave room');
            textRoom.append(currentUser);
            textRoom.append($('<br>'));
        })

        // Final: Appending to existing dom
        $('#chatContent').append(chatRoom);
    }
};