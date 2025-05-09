//https://forum.djangoproject.com/t/updating-model-after-click-event-with-javascript/6795/3
//https://forum.djangoproject.com/t/making-an-update-shifts-template/27395/3
let nowinterval = null;
document.addEventListener('DOMContentLoaded', function () {
    const weekDropdown = document.getElementById('week');
    const gamesList = document.getElementById('gamesList');
    const csrfToken = document.querySelector('[name=]').value; 
    //https://stackoverflow.com/questions/72251730/how-to-properly-catch-fetch-request-in-django	
    //https://stackoverflow.com/questions/73796661/how-to-pass-csrf-token-manually-for-post-requests-in-ajax-django
    //https://stackoverflow.com/questions/51033185/addeventlistener-onchange-dropdown-selected-value-javascript
    //https://simplifyscript.com/blogs/how-to-setinterval-and-clearinterval-in-javascript/
    weekDropdown.addEventListener('change', function () {
       const selectedWeek = this.value;
       fetch("/gameperweek/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": ,
            },
	    body: JSON.stringify({ week:selectedWeek })
        })
        .then(response => response.json())
        .then(data => {
	    gamesList.innerHTML = ''; // Clear previous games
            if (data.allgames && data.allgames.length > 0) {
                data.allgames.forEach(game => {
                    const gameButton = document.createElement('button');
                    gameButton.className = 'gamebutton';
		    gameButton.value = game.gameID;
                    gameButton.innerHTML = `${game.away} @ ${game.home} - ${game.gameTime}`;
		    gameButton.addEventListener('click', function() {
                        const gameID = this.value;
			if (nowinterval) {
                            clearInterval(nowinterval);
			}
                        nowinterval = setInterval(() => {
			    fetchData(gameID, csrfToken);
			}, 5000);
                    });
                    gamesList.appendChild(gameButton);
                });
            } else {
                console.log("No games this week")
            }
        })
        .catch(error => {
            console.error('Error fetching games:', error);
        });
    });
});

//https://stackoverflow.com/questions/78959067/how-do-i-update-the-dom-using-javascript-fetch-method-to-filter-user-data-from-a
const fetchData = async (gameID, csrfToken) => {
  console.log("fetching");
  try {
    const response = await fetch('/playbyplay/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': 
      },
	    body: JSON.stringify({ gameID:gameID }),
    });
    const data = await response.json()
    const allPlayByPlay = data['allPlayByPlay']
    console.log("All play by play", allPlayByPlay);
    if (allPlayByPlay) {
      document.getElementById('nowplay').textContent = allPlayByPlay[allPlayByPlay.length - 1].play;
      document.getElementById('currentperiod').textContent = data.currentPeriod;
      document.getElementById('gameclock').textContent = data.gameClock;
      document.getElementById('homepoints').textContent = data.homePts;
      document.getElementById('awaypoints').textContent = data.awayPts;
    }
  } catch (error) {
    console.error('Error fetching data:', error);
  }
};
