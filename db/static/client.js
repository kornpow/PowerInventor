$(document).ready(function() {
	alert("SHITS");
	$("#toggle-relay").click(function(e) {
		$("#debug_string").html("Clicked");
		alert("test")
		console.log($('#set_num').val())
		$.get("/SetRelay", data={"relay": $('#set_num').val() },"html")
		.done(function(string) {
		// $("#the-string input").val(string);
		$('#debug_string').text("Finished");
		});
		// e.preventDefault();
	});
});