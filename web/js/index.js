function processForm() {
	if ($("#phrase").val())
		$.post('/api/say',
			{ phrase: $("#phrase").val() },
			function(data, status, jqXHR) {
				// console.log(data);
				$('#status').html(JSON.stringify(data));
				outputAnswer(data.answer);
				$("#phrase").val('');
			},
			'json');
}

var currentLineIndex = 0;
var MAX_OUTPUT_LINES = 10;
var spanMark = '<span id="silentone"></span>';

function outputAnswer(answer) {
	$('#output').append(answer + '<br/>' + spanMark);
	currentLineIndex++;

	// remove first line if there are too many lines already
	if (currentLineIndex > MAX_OUTPUT_LINES) {
		var text = $('#output').html();
		var i = text.indexOf(spanMark);
		if (i > 0) $('#output').html(text.substring(i + spanMark.length));
	}
}