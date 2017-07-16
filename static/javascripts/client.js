$(document).ready(function() {
	$("#toggle-relay").click(function(e) {
		$("#debug_string").html("Clicked");
		console.log($('#in_relay_set').val())
		console.log($('#in_val_set').val())
		dataToSend = {'relay': $('#in_relay_set').val(), 'val': $("#in_val_set").val() };
		urlToSend = "/SetRelay";
		alert("alive")
		$.ajax({ 
			type: "GET",
			url: urlToSend,
			data: dataToSend,
			dataType: "json"
		}).done(function(data) {
			alert("fuck! " + data );
			console.log("fuck")
			$('#debug_string').text("Finished");
		});
		// e.preventDefault();
	});
	$("#add-to-schedule").click(function(e) {
		$("#debug_string").html("Clicked");
		console.log($('#in_relay_sch').val())
		console.log($('#in_val_sch').val())
		console.log($('#in_hour_sch').val())
		console.log($('#in_min_sch').val())
		dataToSend = {'relay': $('#in_relay_sch').val(), 'val': $("#in_val_sch").val(),'hour':$("#in_hour_sch").val(),'minute':$("#in_min_sch").val() };
		urlToSend = "/AddTask";
		alert("alive")
		$.ajax({ 
			type: "GET",
			url: urlToSend,
			data: dataToSend,
			dataType: "json"
		}).done(function(data) {
			console.log("fuck")
			$('#debug_string').text("Finished");
		});
		// e.preventDefault();
	});
	$("#check-schedule").click(function(e) {
		$("#debug_string").html("Clicked");

		dataToSend = {};
		urlToSend = "/PrintSchedule";
		$.ajax({ 
			type: "GET",
			url: urlToSend,
			data: dataToSend,
			dataType: "json"
		}).done(function(data) {
			alert("fuck! " + data["0"] );
			console.log("fuck")
			$('#schedule-list').empty();
			$('#debug_string').text("Finished");
			$.each(data,function(key,val){
				$('#schedule-list').append("<p>"+val+"</p>")
			})
			
		});
		// e.preventDefault();
	})
});