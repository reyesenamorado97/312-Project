var socket=io.connect('http://localhost:5000');

socket.on('connect', function(){
    console.log("connected to web sockets")
});

socket.on('disconnect', function(){
    console.log("disconnected to web sockets")
});

socket.on('user', function(message){
    console.log('Hi')
    console.log(message)
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

// allButtons = [
// 	button1,
// 	button2,
// 	button3,
// 	button4,
// 	button5,
// 	button6,
// 	button7,
// 	button8,
// 	button9,
// 	button10,
// 	button11,
// 	button12,
// 	button13,
// 	button14,
// 	button15,
// 	button16,
// ];

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

// Runs whenever a game button is pressed
async function pressAnyGameButton(buttonId) {

    missText.innerHTML = "Waiting...";
    // Add the id of this button to the list of pressed buttons
    pressedButtons.push(buttonId)

    disableAllGameButtons()

    // Simulate waiting for an opponent to press a button
    // Server stuff should happen
    await new Promise(r => setTimeout(r, 2000));

    if (buttonId == "button4") {
        missText.innerHTML = "You Won!";
        await new Promise(r => setTimeout(r, 10));
        winGame();
        window.location.replace("/home");


        return

    }

    // Reenable all the buttons that have not been pressed yet 
    buttonsMap.forEach((value, key) => {
        
        
        if (!pressedButtons.includes(key)) {
			value.disabled = false;
		}
    });
    
    missText.innerHTML = "You missed their ship!";
}

// need ajax for  for