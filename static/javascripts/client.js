var red = "rgb(255, 0, 0)";
var green = "rgb(0, 128, 0)";
var blue = "rgb(20, 23, 204)";

function GetRelayStatus() {
	setTimeout(function() {GetRelayStatus(); }, 2000);

	dataToSend = {};
			urlToSend = "/GetRelayStatus";
			$.ajax({ 
				type: "GET",
				url: urlToSend,
				data: dataToSend,
				dataType: "json"
			}).done(function(data) {
				$('#debug_string').text("Finished");
				// alert("relay1: " + data["relay1"] + " relay2: " + data["relay2"] + " relay3" + data["relay3"] + " relay4: " + data["relay4"]);
				if(data["relay1"] == 1) {
					$('.status#relay1').css('background-color',green);
				}
				else {
					$('.status#relay1').css('background-color',red);
				}
				if(data["relay2"] == 1) {
					$('.status#relay2').css('background-color',green);
				}
				else {
					$('.status#relay2').css('background-color',red);
				}
				if(data["relay3"] == 1) {
					$('.status#relay3').css('background-color',green);
				}
				else {
					$('.status#relay3').css('background-color',red);
				}
				if(data["relay4"] == 1) {
					$('.status#relay4').css('background-color',green);
				}
				else {
					$('.status#relay4').css('background-color',red);
				}
			});
}

$(document).ready(function() {
	GetRelayStatus();

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
			// alert("fuck! " + data );
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
			// console.log("fuck")
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
			// alert("fuck! " + data["0"] );
			// console.log("fuck")
			$('#schedule-list').empty();
			$('#debug_string').text("Finished");
			$.each(data,function(key,val){
				$('#schedule-list').append("<p>"+val+"</p>")
			})
			
		});
		// e.preventDefault();
	});
	$("#get-status").click(function(e) {
		GetRelayStatus();
	});
});