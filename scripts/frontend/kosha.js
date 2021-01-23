function generateTab(data, outTran) {
	x = '';
	var starter = 0;
	for (dict in data){
	block2 = data[dict];
	if(block2.length > 0) {
		if (starter == 0){
			x += '<input type="radio" name="tabs" id="' + dict + '" checked="checked">';
		}
		else{
			x += '<input type="radio" name="tabs" id="' + dict + '">';
		}
		x += '<label for="'+ dict + '">' + dict + '</label>';
		x += '<div class="tab">';
		for (i in block2) {
			block1 = block2[i];
			chapterDetails = block1.dictionary + ', ' + block1.kanda + ', ' + block1.varga + ', ' + block1.adhyaya + ', ' + block1.versenum + ', ' + block1.page;
			chapterDetails = Sanscript.t(chapterDetails, 'slp1', outTran);
			verse = block1.verse;
			verse = Sanscript.t(verse, 'slp1', outTran);
			x += verse;
			x += '<br />(' + chapterDetails + ')';
			x += '<hr></hr>'
			}
		x += '</div>';
		starter = 1;
		}
	}
	return x;
}


async function getApi() {
	var hw = document.getElementById('headword').value;
	var inTran = document.getElementById('inTran').value;
	var outTran = document.getElementById('outTran').value;
	var dictionary = document.getElementById('dictionary').value;
	hw = Sanscript.t(hw, inTran, 'slp1');
	var url = '';
	var reg1 = /[.*+?]/g;
	
	if (dictionary == 'all'){
		url = 'https://kosha.sanskritworld.in/v0.0.1/query/' + hw;
	}
	else {
		url = 'https://kosha.sanskritworld.in/v0.0.1/query/' + hw + '/koshas/' + dictionary;
	}
	console.log(url);
	const response = await fetch(url);
	const data = await response.json();
	x = await generateTab(data, outTran);
	document.getElementById("tabs").innerHTML = x;
}

