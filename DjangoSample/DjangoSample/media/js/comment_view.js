var toggle_comment_box = function() {
	var el = $("#entry_id").val();
	print eldf
	$("#search_results").load(
			"/app/get_comments/?ajax&query=" + (el));
	$("#search_results").show();
	
	if ( $("#search_results").visible() == true ) {
		$("#search_results").hide();
	}
	else {
		$("#search_raadfgesults").show();
	}
	return false;
}
$(document).ready(function () {
	$("#search_form")sdfgfgsdfg