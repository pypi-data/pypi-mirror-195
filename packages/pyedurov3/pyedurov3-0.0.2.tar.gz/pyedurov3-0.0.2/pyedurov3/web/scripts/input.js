//*** Keyboard Inputs ***//
function keyboard_init()
{
    console.log("attaching keyboard events")
    window.addEventListener("keydown", (event) => handle_keyboard_down(event.key));
    window.addEventListener("keyup",   (event) => handle_keyboard_up(event.key));
}

function handle_keyboard_down(key) {
    //console.log("key down");
    for(var i = 0; i < CHANNEL_COUNT; i++){
        if( key == inputSettings[i].forwardKey ){
            //console.log("found matching forward key" + key);
            if(inputSettings[i].toggleableInput){
                toggleInputChannels(i);
            }
            else{
                //console.log("regular input");
                outputChannels.channels[i] = inputSettings[i].activeValue;
            }
            
        }
        else if( key == inputSettings[i].reverseKey ){
            if(!inputSettings[i].toggleableInput){
                outputChannels.channels[i] = -1*inputSettings[i].activeValue;
            }
        }
    }

    if(key == "Escape"){
        switch_to_page("main-page");
    }

    if(key == 'i'){
       startMotorTest(1);
    }
    else if( key == 'o'){
        startMotorTest(2);
    }
    else if( key == 'k'){
        stopMotorTest(2);
    }
}

function startMotorTest(motors){
    if(measurementStarted){
        return;
    }
    console.log("Starting motor test");
    currentBuffer = [];
    voltageBuffer = [];
    if(motors == 1){
        console.log("Triggering 1 motor");
        outputChannels.channels[1] = inputSettings[1].activeValue;
    }
    else if(motors == 2){
        console.log("Triggering 2 motors");
        outputChannels.channels[1] = inputSettings[1].activeValue;
        outputChannels.channels[2] = inputSettings[2].activeValue;
    }
   
    measurementStarted = true;
    startTs = Date.now();
    
    window.setTimeout(intermediateMotorTest,4000,motors)
}

function intermediateMotorTest(motors){
    if(motors == 1){
        outputChannels.channels[1] = 0;
    }
    else if(motors == 2){
        outputChannels.channels[1] = 0;
        outputChannels.channels[2] = 0;
    }
    window.setTimeout(stopMotorTest,4000,motors)
}

function stopMotorTest(motors){
    outputChannels.channels[1] = 0;
    outputChannels.channels[2] = 0;
    console.log("stopping motor test");
    measurementStarted = false;

    var csvString = "Motor Current,Battery Voltage \n";
    for( var i = 0; i < currentBuffer.length; i++){
        csvString += timeStampts[i];
        csvString += ","
        csvString += currentBuffer[i];
        csvString += ","
        csvString += voltageBuffer[i];
        csvString += '\n';
    }
    console.log(csvString);
}

function handle_keyboard_up(key) {
    //console.log("key up");
    for(var j = 0; j < CHANNEL_COUNT; j++){
        if(inputSettings[j].toggleableInput == false){
            if( (key == inputSettings[j].forwardKey)||
            (key == inputSettings[j].reverseKey)){
                //console.log("Turning off");
                outputChannels.channels[j] = 0;
            } 
        }
    }
}

//*** Button Inputs ***//
function processButton(id){
    console.log("process button");
    for(var i = 0; i < CHANNEL_COUNT; i++){
        if(inputSettings[i].button){
            if(id == inputSettings[i].button){
                toggleInputChannels(i);
            }
        }
    }
}

function set_button_state(id, value)
{    
    var btn = document.getElementById(id);
    if(id == "armBtn"){
        var content = value?"Disarm":"Arm";
        btn.innerHTML = content;
        if(value){
            //btn.className += " btn-danger";
            btn.className = btn.className.replace(" btn-dark", " btn-danger");
        }
        else{
            btn.className = btn.className.replace(" btn-danger", " btn-dark");
        }
    }

    if(id == "lightBtn"){
        if(value){
            btn.className = btn.className.replace(" btn-dark", " btn-warning");
        }
        else{
            btn.className = btn.className.replace(" btn-warning", " btn-dark");
        }
    }

    if(value){
        btn.className += " active";
    }else{
        btn.className = btn.className.replace(" active", "");
    }
}
//*** Joystick Inputs ***//
var leftJoystick = null;
var rightJoystick = null;

function joystickInit(){
    leftJoystick = new JoyStick('leftJoystick');
    rightJoystick = new JoyStick('rightJoystick');
}

function updateJoystickData(){
    outputChannels.channels[1] = leftJoystick.GetY();
    outputChannels.channels[2] = leftJoystick.GetY();
    outputChannels.channels[3] = leftJoystick.GetX();
    console.log(outputChannels.channels);
}

//*** General Channel Stuff ***/
function toggleInputChannels(idx){
    console.log("toggling input channel");
    inputSettings[idx].active = !inputSettings[idx].active;
    if(inputSettings[idx].active){
        outputChannels.channels[idx] = inputSettings[idx].activeValue;
    }
    else{
        outputChannels.channels[idx] = 0;
    }
    set_button_state(inputSettings[idx].button,inputSettings[idx].active);
}