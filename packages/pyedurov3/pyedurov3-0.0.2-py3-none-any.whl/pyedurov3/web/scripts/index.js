function sendOutputChannels(){
    //console.log("Sending channel data");
    //console.log(outputChannels.channels);
    io_send(outputChannels);
}

function processUplink(uplinkMsg){

    if("sensors" in uplinkMsg){
        document.getElementById("batteryVoltage").innerHTML = uplinkMsg.sensors.batteryVoltage;
        document.getElementById("motorCurrent").innerHTML = uplinkMsg.sensors.motorCurrent;
        if(measurementStarted){
            timeStampts.push(Date.now()-startTs);
            currentBuffer.push(uplinkMsg.sensors.motorCurrent);
            voltageBuffer.push(uplinkMsg.sensors.batteryVoltage);
        }
    }
    else if("outputSettings" in uplinkMsg){
        console.log("Received settings from server")
        console.log(uplinkMsg);
        onSettings(uplinkMsg);
    }
    else{
        //console.log("Received unknown message")
        //console.log(uplinkMsg)
    }
}

function start()
{
    console.log("starting webapp");
    page_update_size();
    settings_initForms();

    address = window.location.hostname
    console.log("Got address " + address);

    if(address){
        video_init(`ws://${address}`);

        io_open(
            `ws://${address}`, 
            (event) => { processUplink(JSON.parse(event.data)); },
            (event) => { requestSettings();},
            () =>      { }
        );
    } 

    keyboard_init();
    //joystickInit();
    
    //window.setInterval(updateJoystickData,100);
    window.setInterval(sendOutputChannels,100);
    window.addEventListener("resize", video_update_size);
    window.addEventListener("resize", page_update_size);
}
