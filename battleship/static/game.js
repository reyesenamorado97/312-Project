let room;
let youAre;

var socket = io.connect('http://localhost:8080');

socket.on('room', function(data){
    data=JSON.parse(data)
    room = data.room;
    youAre=data.youAre;
    if (data.start){
        buttonsMap.forEach((value, key) => {
            if (!pressedButtons.includes(key)) {
                value.disabled = false;
            }
        });
    }
})
socket.on('players', function(data){
    data=JSON.parse(data)
    if (data.p1==youAre){
        update_opponent(data.p2)
    }
    else{
        update_opponent(data.p1)
    }
})

socket.on('connect', function(){
    // console.log("connected to web sockets")
});

socket.on('disconnect', function(){
    // console.log("disconnected to web sockets")
});

socket.on('user', function (message) {
    // console.log('Hi')
    // console.log(message)
});

// Runs when server responds 
socket.on('gameResponse', function (message) {
   // message=JSON.parse(message);
    if (message.user!=youAre){
        // Reenable all the buttons that have not been pressed yet 
        buttonsMap.forEach((value, key) => {
            if (!pressedButtons.includes(key)) {
                value.disabled = false;
            }
        });
        
        missText.innerHTML = "They missed your ship!";
    }
    if (message.winner==youAre) {
        missText.innerHTML = "You Won!";
        winGame();
        window.location.replace("/home");
        return
    }   
    if (message.winner!='None'){
        missText.innerHTML = "You Lost!";
        loseGame()
        window.location.replace("/home");
        return
    }
    
});

// Get buttons from html
const button1 = document.getElementById("button1");
const button2 = document.getElementById("button2");
const button3 = document.getElementById("button3");
const button4 = document.getElementById("button4");
const button5 = document.getElementById("button5");
const button6 = document.getElementById("button6");
const button7 = document.getElementById("button7");
const button8 = document.getElementById("button8");
const button9 = document.getElementById("button9");
const button10 = document.getElementById("button10");
const button11 = document.getElementById("button11");
const button12 = document.getElementById("button12");
const button13 = document.getElementById("button13");
const button14 = document.getElementById("button14");
const button15 = document.getElementById("button15");
const button16 = document.getElementById("button16");


const missText = document.getElementById("miss");

const buttonsMap = new Map();
buttonsMap.set("button1", button1);
buttonsMap.set("button2", button2);
buttonsMap.set("button3", button3);
buttonsMap.set("button4", button4);
buttonsMap.set("button5", button5);
buttonsMap.set("button6", button6);
buttonsMap.set("button7", button7);
buttonsMap.set("button8", button8);
buttonsMap.set("button9", button9);
buttonsMap.set("button10", button10);
buttonsMap.set("button11", button11);
buttonsMap.set("button12", button12);
buttonsMap.set("button13", button13);
buttonsMap.set("button14", button14);
buttonsMap.set("button15", button15);
buttonsMap.set("button16", button16);



// This array will hold all the buttons that this player has pressed already
var pressedButtons= []

// Use this when one of the players is waiting for the other to make a move
function disableAllGameButtons() {
	buttonsMap.forEach((value, key) => {
			value.disabled = true;
	});
}

function winGame() {
    alert("You sunk their ship! You win!")
}

function loseGame() {
    alert("You lost!")
}

function update_opponent(opp){
    const opponent = document.getElementById("opponent")
    opponent.innerHTML="Opponent: "+ opp
}

// Runs whenever a game button is pressed
async function pressAnyGameButton(buttonId) {
    missText.innerHTML = "Waiting...";
    // Add the id of this button to the list of pressed buttons
    pressedButtons.push(buttonId)

    disableAllGameButtons()
    buttonsMap.delete(buttonId)

    socket.emit('button', {'user':youAre, 'button': buttonId , 'room': room})
}

//start disabled
disableAllGameButtons()