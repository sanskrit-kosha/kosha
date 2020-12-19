function generateTab(data, outTran, hw) {
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
			v = []
			while((i = verse.indexOf(hw)) != -1) {
				i = verse.indexOf(hw);
				j = i + hw.length - 1;
				s = Sanscript.schemes['slp1']
				while (i > 0 && s.consonants.includes(verse[i-1]))
					i--;
				v.push(Sanscript.t(verse.slice(0, Math.max(0, i)), 'slp1', outTran));
				while (j < verse.length && s.consonants.includes(verse[j])) {
					j++;
				}
				if (j < verse.length && s.vowels.includes(verse[j]))
					j++;
				if (j < verse.length && s.other_marks.includes(verse[j]))
					j++;
				v.push('<b>' + Sanscript.t(verse.slice(i, j), 'slp1', outTran) + '</b>');
				verse = verse.slice(j, verse.length);
			}
			v.push(Sanscript.t(verse, 'slp1', outTran));
			x += v.join('');
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
	x = await generateTab(data, outTran, hw);
	document.getElementById("tabs").innerHTML = x;
}
