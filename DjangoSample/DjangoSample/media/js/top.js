var toggle_comment_box = function(url, entry_id) {
	var el = $('comment_box_'+entry_id);

	if ( el.visible() == true ) {
		el.hide();
	}
	else {
		var ajax = new Ajax.Updater(el, url);
		el.show();
	}
}