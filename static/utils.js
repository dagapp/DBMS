function I(element_id) {
	return document.getElementById(element_id);
}

function ajax(options) {
	let xhr = new XMLHttpRequest();
	xhr.onreadystatechange = function() {
		if (xhr.readyState != 4) {
			return;
		}
		let error_text = xhr.statusTest;
		if (xhr.status == 200) {
			try {
				options.on_success(xhr.responseText);
				return;
			} catch (e) {
				error_text = String(e);
			}
		}
		(options.on_error || console.log)(error_text);
	};
	xhr.open(options.method || 'GET', options.url, true);
	xhr.setRequestHeader('Content-Type', options.data_type || 'application/json');
	xhr.send(options.data || null);
}

function delete_entry(delete_button, entry_id) {
	let table_row = delete_button.parentElement.parentElement;
	if (!confirm("Do you really want to delete a row with id=" + entry_id + "?")) {
		return;
	}
	ajax({
		method: 'POST',
		url: '/del/' + entry_id,
		on_success: function (response) {
			table_row.remove();
		}
	});	
}
