$(document).ready(function () {
  $('#add').click(function() {
    var particle = new Particle();

    //var uname = 'korn94sam@gmail.com'
    //var pass = 'sksk9494??'

    // var uname = 'korn94sam@gmail.com'
    // var pass = "sksk9494??"

    // var targetdev = 'GrowerApp'
    var targetdev = 'SmartSense'

    var relay_target = 0
    var onHour = 0;
    var onMinute = 0;
    var offHour = 0;
    var offMinute = 0;
    var payload = 0;

    var atoken = 0; //Access token
    var deviceid = 0; //Device id

    relay_target = $('#relaynum').val();
    onHour = $('#hon').val();
    onMinute = $('#mon').val();
    offHour =$('#hoff').val();
    offMinute =$('#moff').val();

    payload = relay_target + ':' + onHour + ':' + onMinute + ':' + offHour + ':' + offMinute;


    particle.login({username: uname, password: pass}).then(function(data) {
      atoken = data.body.access_token


    //List devices
    var devicesPr = particle.listDevices({ auth: atoken });
    devicesPr.then(
      function(devices){
        for(var dev in devices.body) {
        if(devices.body[dev].name == targetdev) {
          console.log("Using device: ",devices.body[dev].name );
          deviceid = devices.body[dev].id;
        }
      }
      console.log("Scheduler Go!");
      console.log("Access Token: ", atoken);
      console.log("Device Id: ", deviceid);
      console.log("Payload: ", payload);  

      var fnPr = particle.callFunction({ deviceId:  deviceid, name: 'schedule', argument: payload.toString(), auth: atoken });

      fnPr.then(
        function(data) {
            console.log("Schedule event added!");
            console.log('Function called succesfully:', data);
          }, function(err) {
            console.log('An error occurred:', err);
        }); //close function call
    }); //Close list



    

  }) //close login
  }) //close onclick
}); //close document.onready  