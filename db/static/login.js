
var atoken = 0;
var logged_in = false;
var deviceid = 0;

var new_dev = true;

var selectedname;

var particle = new Particle();

var red = "rgb(255, 0, 0)";
var green = "rgb(0, 128, 0)";
var blue = "rgb(20, 23, 204)";

function ParticleLogin() {
	// Uncomment to allow using the uer interface inputs
	// var user = $("#particle_user").val();
	// var pass = $("#particle_pass").val();
	//DELETE THIS
	var user = "korn94sam@gmail.com";
	var pass = "sksk9494??";

	console.log("Inside particle login");
	$("#online").css("background-color","red");
	// console.log("username: " +username);
	// console.log("password: " + pass);

	var at = atoken;
	console.log("access token: " + at);

	// if(at > 0) {
	// 	console.log("returning particlelogin");
	// 	return at;
	// }
	if( logged_in == true) {
		console.log("already logged in")
		$("#online").css("background-color","green");
		return at;
	}

	particle.login({username: user, password: pass}).then(function(data) {
  			at = data.body.access_token;
  			console.log("Access token from login: " + at);
  			if(at != 0) {
  			console.log("Login Successful");
  			console.log("Access Token: " + at);
  			atoken = at; //set static variable to new access token
  			$("#online").css("background-color","green");
 			logged_in = true;
  			ShowDevices(at,true);
  	}
	}, //end login function
		function(err) {
		console.log("Login Failed: login.js");
	}); //end login err


	// if(at == -1) {
	// 	console.log("Before login!");
		
	// } //end if
	// else 
	if (at != 0) {
		console.log("Already Logged in");
  		console.log("Access Token: " + at);
  		$("#online").css("background-color","green");
	} //end else if
	return at;
} //end function

function ChooseDevice(token) {
	console.log("Inside ChooseDevice");
	var did = deviceid;

	if(new_dev == false) {
		console.log("Already had device id: " + did);
		return did;
	}

	var devicesPr = particle.listDevices({ auth: atoken }).then( function(devices){
		console.log("Looking up new device id");
    	console.log('Devices: ', devices);
    	for(var dev in devices.body) {
    		if(devices.body[dev].name == selectedname ) {
    			console.log("found id in list");
    			console.log("device name: " + devices.body[dev].name);
    			console.log("device id:" + devices.body[dev].id);
        		did = devices.body[dev].id;
        		new_dev = false;
        		deviceid = did; //Set global deviceid 
       		} //end if device =
    	} //end for
   	}); //end list devices

   	return did;
}


function ShowDevices(token,timeout) {
	var devicesPr = particle.listDevices({ auth: token }).then( function(devices){

		$("#devlist").empty(); //Delete device list so it doesnt get recreated
					//Flush list after data is already loaded
		for(var dev in devices.body) {

			console.log("In ShowDevices");
			var item = document.createElement("div");
			item.setAttribute("id",devices.body[dev].name);
			item.setAttribute("class","device");
			item.innerHTML = devices.body[dev].name;


			if(devices.body[dev].connected == true) {
				console.log(devices.body[dev].name +" is online!");
				$("#devlist").append(function() {

					return item
				});
				$("#devlist").append(document.createElement("br") );
			}
		}
		var numdev = devices.body.length;
		console.log("Number of devices: " + numdev);
		//Hack to hopefully keep correct dev count
	});

	
}



function SelectDevice() {
	console.log("inside setdevice");

	var targetdev = $("#devlist").children().css("background-color","green").attr("id");
	console.log("From Select device: target dev:" + targetdev);
} //end selectdevice

	

function Toggle(button_id,dir) {

	// var uname = 'korn94sam@gmail.com'
	// var pass = "sksk9494??"

	console.log("button press id: " + button_id);

	var relay_target = 0
	var payload = 0;

	var atoken = 0; //Access token
	var deviceid = 0; //Device id

	console.log("toggler!");

	// if($("#"+button_id).css("background-color"))
	console.log( $("#"+ button_id).css("background-color") );

	relay_target = parseInt(button_id[button_id.search(/\d/)]); //get the location of the first digit regex 
	console.log("The relay target is: ", relay_target);

	payload = relay_target + (10*dir); //1,2,3,4 turns on... 11,12,13,14 turns off

	console.log("Get ready to turn relay: " + relay_target+ " with payload: " + payload);

	var atoken = ParticleLogin();
		if(atoken == -1) {
		console.log("Returned bad access token: abort!");
		}
		


		console.log("Received Access Token:"+ atoken);

	deviceid = ChooseDevice(atoken);
    if(deviceid == -1) {
      console.log("Returned bad device id: abort!");
    }
    console.log("Received Device Id:"+ deviceid);
    console.log("Before SET CALL");


	var fnPr = particle.callFunction({ deviceId:  deviceid, name: 'set', argument: payload.toString(), auth: atoken });

	fnPr.then(
		function(data) {
    		console.log('Function called succesfully:', data);
		}, function(err) {
		console.log('An error occurred:', err);
		}); //close function call

	GetRelayStatus(false);

} //end function

function GetRelayStatus(timeout) {
	//Log into the particle cloud

	// console.log("Before set timeout");
	if(timeout) {
		setTimeout(function() { GetRelayStatus(true); }, 3000);
	}

    console.log("Relay_status");
  	var atoken = ParticleLogin();
  	if(atoken == -1) {
    	console.log("Returned bad access token: abort!")
  	}

    deviceid = ChooseDevice(atoken);
    if(deviceid == -1) {
        console.log("Returned bad device id: abort!");
    }
    console.log("Received Device Id:"+ deviceid);
    console.log("Before get variable");

    // particle.getVariable({ deviceId: devices.body[dev].id, name: 'rpack', auth: atoken }).then(function(data) {
    particle.getVariable({ deviceId: deviceid, name: 'rpack', auth: atoken }).then(function(data) {
        console.log('Device variable retrieved successfully:', data.body.name,data.body.result);
        var docid = data.body.name;
        var result = data.body.result;
        var bit;
        for (var i = 1; i < 5; i++) {
            var bit = result & (1 << (i-1) )
            if (bit > 0) {
            	$("#relay"+i).css("background-color",green);
            }
            if (bit == 0) {
            	$("#relay"+i).css("background-color",red);
            }
        } //end for
   	});  // end getvariable
}//end function

function UpdateWeather(timeout) {

    console.log("DHT22 start!");
		
	var atoken = 0; //Access token
	var deviceid = 0; //Device id

	//If timeout flag is there allow function to be repeated in a loop
	if(timeout) {
	  setTimeout(function() { UpdateWeather(true); }, 5000);
	}

	var atoken = ParticleLogin();
	
  	console.log("DHT22 is alive!");
  	
	deviceid = ChooseDevice(atoken);
	// console.log("dht22: Access Token: ", atoken);
	// console.log("DHT22: Device Id: ", deviceid);

	particle.getVariable({ deviceId: deviceid, name: 'tempf', auth: atoken }).then(function(data) {
	// console.log('Device variable retrieved successfully:', data);
			$("#tempf").text(data.body.result);
	}, 
	function(err) {
		  console.log('An error occurred while getting tempf:', err);
	}); //end getvariable
	particle.getVariable({ deviceId: deviceid, name: 'humidity', auth: atoken }).then(function(data) {
		  // console.log('Device variable retrieved successfully:', data);
		  	$("#humidity").text(data.body.result);
	}, function(err) {
		  	console.log('An error occurred while getting humdity:', err);
	}); //End getvariable
	particle.getVariable({ deviceId: deviceid, name: 'light', auth: atoken }).then(function(data) {
		  // console.log('Device variable retrieved successfully:', data);
		  	$("#light").text(data.body.result);
	}, function(err) {
		  	console.log('An error occurred while getting light:', err);
	}); //End getvariable
			
}; //end functions


$(document).on('click','#login',function() {
	console.log("CLicked login!");
	var access_token = ParticleLogin();
	ShowDevices(access_token,false);
})


$(document).on('click','.device',function() { 
	$(".device").css("background-color","red"); 
	$(this).css("background-color","green");
	selectedname = $(this).attr("id");
	console.log("clicked " + selectedname);
	new_dev = true;
	// $(".status").css("background-color","blue");
	GetRelayStatus(false);
	UpdateWeather(false);
});

$(document).on('click',".status", function() {
	// ToggleClick();
	console.log("Relay Click");
	console.log("Clicked color is: " + $(this).css("background-color") );

	if(	$(this).css("background-color") === red )
	{
		console.log("Turn on!");
		// Toggle($(this).attr("id").search(/\d/), 1); //send button id to toggler function
		Toggle($(this).attr("id"), 0); //send button id to toggler function
	}
	else  if($(this).css("background-color") === green) {
		console.log("Turn off!");
		Toggle($(this).attr("id"), 1); //send button id to toggler function	
	}
	console.log("Toggle toggle toggle");
	// Toggle($(this).attr("id") ); //send button id to toggler function
	GetRelayStatus(false);
	UpdateWeather(false);

});


$(document).ready(function() {
  GetRelayStatus(true);
  UpdateWeather(true);
});
