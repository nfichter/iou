$(document).ready(function() {
	$('#reveal-if-yes').hide();
	$('#reveal-if-no').hide();
	
	$('input[type="radio"]').click(function() {
		if($(this).attr('id') == 'yes') {
			$('#reveal-if-yes').show();           
		}
		if($(this).attr('id') == 'no') {
			$('#reveal-if-no').show();   
		}
	});
});