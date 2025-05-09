document.addEventListener('DOMContentLoaded', function () {
    const teamDropdown = document.getElementById('team');
    const csrfToken = document.querySelector('[name=]').value; 
    teamDropdown.addEventListener('change', async function () {
       const selectedTeam = this.value;
       try {
          const response = await fetch("/teaminfo/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": ,
            },
	    body: JSON.stringify({ team:selectedTeam })
          });
	  const data = await response.json();
	  console.log("data: ",data);
          if (data.teamInfo) {
             document.getElementById('tlogo').src = data.teamInfo.nflComLogo1;
             document.getElementById('teamname').innerHTML = data.teamInfo.teamName;
	     document.getElementById('teamcity').innerHTML = data.teamInfo.teamCity;
	     document.getElementById('conference').innerHTML = data.teamInfo.conferenceAbv;
	     document.getElementById('division').innerHTML = data.teamInfo.division;
	     document.getElementById('rushYds').innerHTML = data.teamInfo.rushYds;
	     document.getElementById('carries').innerHTML = data.teamInfo.carries;
             document.getElementById('rushTD').innerHTML = data.teamInfo.rushTD;
             document.getElementById('fgAttempts').innerHTML = data.teamInfo.fgAttempts;
	     document.getElementById('fgMade').innerHTML = data.teamInfo.fgMade;
	     document.getElementById('fgYds').innerHTML = data.teamInfo.fgYds;
	     document.getElementById('kickYards').innerHTML = data.teamInfo.kickYards;
	     document.getElementById('xpAttempts').innerHTML = data.teamInfo.xpAttempts;
             document.getElementById('xpMade').innerHTML = data.teamInfo.xpMade;
	     document.getElementById('passAttempts').innerHTML = data.teamInfo.passAttempts;
             document.getElementById('passTD').innerHTML = data.teamInfo.passTD;
             document.getElementById('passYds').innerHTML = data.teamInfo.passYds;
             document.getElementById('intercept').innerHTML = data.teamInfo.intercept;
             document.getElementById('passCompletions').innerHTML = data.teamInfo.passCompletions;
             document.getElementById('puntYds').innerHTML = data.teamInfo.puntYds;
             document.getElementById('puntsNum').innerHTML = data.teamInfo.punts;
             document.getElementById('receptions').innerHTML = data.teamInfo.receptions;
             document.getElementById('recTD').innerHTML = data.teamInfo.recTD;
             document.getElementById('targets').innerHTML = data.teamInfo.targets;
             document.getElementById('recYds').innerHTML = data.teamInfo.recYds;
             document.getElementById('fumblesLost').innerHTML = data.teamInfo.fumblesLost;
             document.getElementById('fumblesRecovered').innerHTML = data.teamInfo.fumblesRecovered;
             document.getElementById('defTD').innerHTML = data.teamInfo.defTD;
             document.getElementById('qbHits').innerHTML = data.teamInfo.qbHits;
             document.getElementById('passDeflections').innerHTML = data.teamInfo.passDeflections;
             document.getElementById('totalTackles').innerHTML = data.teamInfo.totalTackles;
             document.getElementById('rushing').style.display = 'block';
             document.getElementById('kicking').style.display = 'block';
	     document.getElementById('passing').style.display = 'block';
             document.getElementById('punts').style.display = 'block';
	     document.getElementById('receiving').style.display = 'block';
             document.getElementById('defense').style.display = 'block';
	  } else {
              console.log("No team info received");
          }
       } catch(error) {
             console.error('Error fetching team:', error);
       }
    });
});

document.addEventListener('DOMContentLoaded', function () {
    const searchtext = document.getElementById('stext');
    const steam = document.getElementById('steam');
    const sposition = document.getElementById('sposition');
    const ssort = document.getElementById('ssort');
    const sbutton = document.getElementById('searchbutton');
    const playerstable = document.getElementById('playerstable');
    const csrfToken = document.querySelector('[name=]').value;
    sbutton.addEventListener('click', async function () {
       const usertext = searchtext.value;
       const userteam = steam.value;
       const userposition = sposition.value;
       const usersort = ssort.value;
       try {
          const response = await fetch("/playerslist/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": ,
            },
	    body: JSON.stringify({ usertext:usertext, userteam:userteam, userposition:userposition, usersort:usersort })
          });
          const data = await response.json();
          console.log("data: ",data);
          if (data.players) {
             playerstable.innerHTML = `
                <tr>
		   <th>Headshot</th>
		   <th>Name</th>
                   <th>Age</th>
                   <th>Position</th>
                   <th>Team</th>
                   <th>Jersey Number</th>
                   <th>Profile</th>
		</tr>
	     `;
             data.players.forEach(player => {
                const row = `
                   <tr>
                      <td><img src="${player.espnHeadshot}" class="listphoto"></td>
		      <td class="listname">${player.espnName}</td>
		      <td class="listage">${player.age}</td>
		      <td class="listpos">${player.pos}</td>
		      <td class="listteam">${player.team}</td>
		      <td class="listjersey">${player.jerseyNum}</td>
		      <td><button id="playerbutton" class="playerbutton" type="button" value="${player.playerID}">Stats</button></td>
		   </tr>
		`;
                playerstable.innerHTML += row;
	     });
	  } else {
	     console.log("No player data received");
          } 
       } catch(error) {
          console.error("error fetching players: ", error);
       }
    });

    const playerbutton = document.getElementById("playerbutton");
    const playercard = document.getElementById("playercard");
    playerstable.addEventListener('click', async function () {
       if (event.target && event.target.classList.contains('playerbutton')){
          const playerID = event.target.value;
          try {
  	    const response = await fetch("/playerprofile/", {
  	       method: "POST",
	       headers: {
	  	  "Content-Type": "application/json",
		  "X-CSRFToken": ,
	       },
               body: JSON.stringify({ playerID:playerID})
            });
	    const data = await response.json();
	    if (data.player) {
               playercard.innerHTML = `
                  <div>${ data.player.espnHeadshot }</div>
                  <div class="pplayerName">${ data.player.espnName }</div>
                  <div>${ data.player.team }</div>
                  <div>${ data.player.jerseyNum }</div>
                  <div>${ data.player.pos }</div>
                  <div>${ data.player.age }</div>
                  <div>${ data.player.weight }</div>
  		  <a href=${ data.player.fantasyLink }>Fantasy Link</a>
                  <table id="rushtable" class="rushtable">
                    <thead>
                      <tr>
                        <th>Rush Yards</th>
                        <th>Carries</th>
                        <th>Rush TD</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr>
                        <td>${ data.player.rushYds }</td>
                        <td>${ data.player.carries }</td>
                        <td>${ data.player.rushTD }</td>
                      </tr>
                    </tbody>
                  </table>
                  <table id="passtable" class="passtable">
                    <thead>
                      <tr>
                        <th>Pass Attempts</th>
                        <th>Pass TD</th>
                        <th>Pass Yards</th>
                        <th>Interceptions</th>
                        <th>Pass Completions</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr>
                        <td>${ data.player.passAttempts }</td>
                        <td>${ data.player.passTD }</td>
                        <td>${ data.player.passYds }</td>
                        <td>${ data.player.intr }</td>
                        <td>${ data.player.passCompletions }</td>
                      </tr>
                    </tbody>
                  </table>
                  <table id="receivetable" class="receivetable">
                    <thead>
                      <tr>
                        <th>Receptions</th>
                        <th>Receive TD</th>
                        <th>targets</th>
                        <th>Receive Yards</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr>
                        <td>${ data.player.receptions }</td>
                        <td>${ data.player.recTD }</td>
                        <td>${ data.player.targets }</td>
                        <td>${ data.player.recYds }</td>
                      </tr>
                    </tbody>
                  </table>
                  <table id="defensetable" class="defensetable">
                    <thead>
                      <tr>
                        <th>Tackles</th>
                        <th>Fumbles Lost</th>
                        <th>Fumbles Recovered</th>
                        <th>Defense TD</th>
  	  	        <th>Solo Tackles</th>
		        <th>Def Interceptions</th>
		        <th>QB Hits</th>
                        <th>Pass Deflections</th>
		        <th>Sacks</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr>
                        <td>${ data.player.totalTackles }</td>
                        <td>${ data.player.fumblesLost }</td>
                        <td>${ data.player.fumblesRecovered }</td>
                        <td>${ data.player.defTD }</td>
 	  	        <td>${ data.player.soloTackles}</td>
		        <td>${ data.player.defensiveInterceptions }</td>
		        <td>${ data.player.qbHits }</td>
		        <td>${ data.player.passDeflections }</td>
		        <td>${ data.player.sacks }</td>
                      </tr>
                    </tbody>
                 </table>
	       `;
            } else {
               console.log("No player data received");
            }
         } catch(error) {
            console.error("error fetching players: ", error);
         }
       };
    });
});
