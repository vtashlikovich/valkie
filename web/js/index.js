function processForm() {
	let phraseValue = $("#phrase").val();

	if (phraseValue)
		$.post('/api/say',
			{ phrase: phraseValue },
			function(data, status, jqXHR) {
				// console.log(data);
				// $('#status').html(JSON.stringify(data['answer']['tagged_phrase']));
				$('#status').html('');
				outputAnswer(phraseValue, data.answer);
				$("#phrase").val('');
			},
			'json');
}

let currentLineIndex = 0;
let MAX_OUTPUT_LINES = 5;
let spanMark = '<span id="silentone"></span>';

function outputAnswer(question, answerDict) {

	let answer = answerDict['phrase'] + '<br/>';

	answer += '<span style="color:darkgray; font-size:0.8em">';
	for (let index in answerDict['tagged_phrase']) {
		answerDict['tagged_phrase'][index][1] = '<b>' + answerDict['tagged_phrase'][index][1] + '</b>';
		answer += '[' + answerDict['tagged_phrase'][index].slice(1) + '] ';
	}
	answer += '</span>';
	answer += '<br/>';
	answer += (answerDict['devsao_detected']?'<span style="color:green">':'') + answerDict['sao'] +
		(answerDict['devsao_detected']?'</span>':'') + '<br/>';

	let outputDiv = $('#output');
	outputDiv.append('<span style="color: cornflowerblue">&gt; ' + question + '</span><br/>' + answer + '<br/>' + spanMark);
	currentLineIndex++;

	// remove first line if there are too many lines already
	if (currentLineIndex > MAX_OUTPUT_LINES) {
		var text = outputDiv.html();
		var i = text.indexOf(spanMark);
		if (i > 0) $('#output').html(text.substring(i + spanMark.length));
	}

	$('#status').append('<b>Topics:</b> ' + answerDict['topics']);
	let algorithmText = '';
	for (let i in answerDict['algorithm'])
		algorithmText += (algorithmText?'<br/>':'') + (parseInt(i) + 1) + '. [' + answerDict['algorithm'][i] + ']';
	$('#status').append('<br/><b>Algorithm:</b><br/>' + algorithmText);

	if (answerDict['questions']) {
		qList = answerDict['questions'];
		$('#status').append('<br/><b>Questions:</b><br/>' + qList);
	}
}