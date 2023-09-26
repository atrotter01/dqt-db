var slimeStack = [];
var slimeAnimating = false;
var slimesSpawned = 0;

function spawnSlime() {
	slimesSpawned = slimesSpawned + 1;
	var slimeStackID = 'slimeStack_' + slimesSpawned;

	slimeStack.push({
		dx: 0,
		xp: Math.random() * (window.screen.width-50),
		yp: Math.random() * window.screen.height,
		am: Math.random() * 20,
		stx: 0.02 + Math.random() / 10,
		sty: 0.7 + Math.random(),
		num: slimesSpawned,
		id: slimeStackID
	})

	$(document.body).append("<div id='" + slimeStackID + "' style='position: absolute; z-index: "+ slimesSpawned +"; visibility: visible; top: 15px; left: 15px;'><img src='/static/images/SlimeStackFinal.gif' style='width:50px; height:47px;'></div>");
	
	if(!slimeAnimating) {
		rainSlimes();
	}
}

function rainSlimes() {
	for(const slime of slimeStack) {
		slime['yp'] += slime['sty'];

		if(slime['yp'] > window.screen.height - 250) {
			slime['xp'] = Math.random() * (window.screen.width - slime['am'] - 40);
			slime['yp'] = 0;
			slime['stx'] = 0.02 + Math.random() / 10;
			slime['sty'] = 0.7 + Math.random();
		}

		slime['dx'] += slime['stx'];

		document.getElementById(slime['id']).style.top=slime['yp']+"px";
		document.getElementById(slime['id']).style.left=slime['xp'] + slime['am']*Math.sin(slime['dx'])+"px";  
	}

	setTimeout(rainSlimes, 10);
	slimeAnimating = true;
}
