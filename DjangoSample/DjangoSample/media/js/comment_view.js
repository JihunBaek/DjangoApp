var toggle_comment_box = function(url, entry_id) {
	var csrf = $('input[name=csrfmiddlewaretoken]').val();
	$.post(url, "csrfmiddlewaretoken=" + csrf , function(data)
	{
		$('#comment_box_'+entry_id).html(data);
		if($('#comment_box_'+entry_id).is(':visible')){
			$('#comment_box_'+entry_id).hide();
		}
		else{
			$('#comment_box_'+entry_id).show();
		}			
	})
}
$(document).ready(function(){
	toggle_comment_box();
});

