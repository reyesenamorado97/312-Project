var socket=io.connect('http://localhost:5000');

socket.on('connect', function(){
    console.log("connected to web sockets")
});

socket.on('disconnect', function(){
    console.log("disconnected to web sockets")
});

socket.on('users', function(message){
    console.log('Hi')
    console.log(message)
});