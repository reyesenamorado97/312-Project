let room_name = "ass";
const addCard = document.getElementById("allCards");
const leaderboardData = document.getElementById("tableData");

function loadCard(room) {
	addCard.innerHTML +=
		'<div class="card card-size card-color grow" onclick="window.location.href=\'/game\';">' +
		'<div class="card-content"> <div class="media">' +
		'<div class="media-content">' +
		'<p class="title is-4">' +
		room +
		"</p>" +
		"</div>" +
		"</div>" +
		"</div></div><br />";
}

function loadLeaderboard(rank, username, wins) {
	leaderboardData.innerHTML +=  "<td>" + rank + "</td>" +
    "<td>" + username + "</td>" +
    "<td>" + wins + "</td>" ;
}


// Ajax call for getting the cards
function getCards() {
	const request = new XMLHttpRequest();
	request.onreadystatechange = function () {
		if (this.readyState === 4 && this.status === 200) {
			const rooms = JSON.parse(this.response);
			console.log("attempts", rooms.rooms);
			for (let i = 0; i < rooms.rooms.length; i++) {
				loadCard(rooms.rooms[i]);
			}
		}
	};
	request.open("GET", "/currentGames");
	request.send();
}
getCards();

// Ajax call for getting the leaderboard data
function getLeaderboard() {
	const request = new XMLHttpRequest();
	request.onreadystatechange = function () {
		if (this.readyState === 4 && this.status === 200) {
			const leader = JSON.parse(this.response).leaderboard;
			console.log("lb data:", leader.length);
            for (let i = 0; i < leader.length; i++) {
                console.log('hi')
                console.log(leader[i][0],leader[i][1])
				loadLeaderboard(i+1,leader[i][0], leader[i][1]);
			}
		}
	};
	request.open("GET", "/leaderboard");
	request.send();
}
getLeaderboard();
