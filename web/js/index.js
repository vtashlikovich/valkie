function processForm() {
	if ($("#phrase").val())
		$.post('/api/say',
			{ phrase: $("#phrase").val() },
			function(data, status, jqXHR) {
				// console.log(data);
				$('#status').html(JSON.stringify(data));
				outputAnswer($("#phrase").val(), data.answer);
				$("#phrase").val('');
			},
			'json');
}

var currentLineIndex = 0;
var MAX_OUTPUT_LINES = 5;
var spanMark = '<span id="silentone"></span>';

function outputAnswer(question, answerDict) {

	answer = answerDict['phrase'] + '<br/>'

	answer += '<span style="color:darkgray; font-size:0.8em">'
	for (index in answerDict['tagged_phrase']) {
		answerDict['tagged_phrase'][index][1] = '<b>' + answerDict['tagged_phrase'][index][1] + '</b>'
		answer += '[' + answerDict['tagged_phrase'][index].slice(1) + '] '
	}
	answer += '</span>'
	answer += '<br/>'
	answer += (answerDict['devsao_detected']?'<span style="color:green">':'') + answerDict['sao'] +
		(answerDict['devsao_detected']?'</span>':'') + '<br/>'

	$('#output').append('<span style="color: cornflowerblue">&gt; ' + question + '</span><br/>' + answer + '<br/>' + spanMark);
	currentLineIndex++;

	// remove first line if there are too many lines already
	if (currentLineIndex > MAX_OUTPUT_LINES) {
		var text = $('#output').html();
		var i = text.indexOf(spanMark);
		if (i > 0) $('#output').html(text.substring(i + spanMark.length));
	}
}