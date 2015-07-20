// Bind the form submit to a new room event of server side
$(document).ready(function() {
    $('#newRoom').on('submit', function() {
        // See the file chat.js for createNewChatRoom function
        createNewChatRoom();
        return false;
    });
});