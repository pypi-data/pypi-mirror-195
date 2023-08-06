var motorSettingsExample = {
    channel: 1,
    polarity: 1, 
    minPower: 20,
    maxPower: 80,
    responseTime: 1
};

function requestSettings(){
    console.log("requesting settings");
    var msg = {outputSettings:{}};
    settingsRefreshRequested = true;
    io_send(msg);
}

function setOutputSettings(){
    console.log("set output settings");
    console.log("retrieving user input");
    var userInput = getUserSettingsInput();
    console.log(userInput);
    console.log("sending them downstream");
    io_send(userInput);
}

function setDefaultOutputSettings(){
    console.log("restore default output settings");
    var msg = {outputSettings:{dafault:true}};
    io_send(msg);
}

function saveOutputSettings(){
    console.log("save output settings");
    var msg = {outputSettings:{save:true}};
    io_send(msg);
}

function onSettings(newSettings){
    console.log("received settings")
    if(settingsRefreshRequested){
        updateOutputSettingsForms(newSettings);
        settingsRefreshRequested = false;
    }
    
}

function getUserSettingsInput(){
    var inputSettings = JSON.parse(JSON.stringify(settings));
    for( var i = 0 ; i < 4; i++){
        inputSettings.outputSettings.propulsionSystem.motors[i] = getMotorSettingsFromForm(i);
    }
    inputSettings.outputSettings.sensors = getSensorSettingsFromForm();
    inputSettings.outputSettings.battery = getBatterySettingsFromForm();
    inputSettings.outputSettings.accessories = getAccessorySettingsFromForm();
    return inputSettings;
}

function updateOutputSettingsForms(newSettings){
    console.log("updating output settings forms")
    for( var i = 0; i < 4; i++){
        updateMotorSettingsForm(newSettings.outputSettings.propulsionSystem.motors[i],i);
    }
    updateBatterySettingsForm(newSettings.outputSettings.battery);
    updateSensorSettingsForm(newSettings.outputSettings.sensors);
    updateAccessorySettingsForm(newSettings.outputSettings.accessories);
}

function getMotorSettingsFromForm(motorIdx){
    //console.log("retrieving data from form");
    var motorSettings = {};

    motorSettings.channel = parseInt(document.getElementById("motor"+motorIdx+"_channel").value);
    motorSettings.polarity = (document.getElementById("motor"+motorIdx+"_polarity").value> 0)? true:false;;
    motorSettings.minPower = parseInt(document.getElementById("motor"+motorIdx+"_minPower").value);
    motorSettings.maxPower = parseInt(document.getElementById("motor"+motorIdx+"_maxPower").value);
    motorSettings.responseTime = parseInt(document.getElementById("motor"+motorIdx+"_responseTime").value);

    //console.log(motorSettings);
    return motorSettings;
}

function updateMotorSettingsForm(motorSettings, motorIdx){
    //console.log("setting data in motor form "+motorIdx);

    document.getElementById("motor"+motorIdx+"_channel").value = motorSettings.channel;
    document.getElementById("motor"+motorIdx+"_polarity").value = motorSettings.polarity ? 1:0;
    document.getElementById("motor"+motorIdx+"_minPower").value = motorSettings.minPower;
    document.getElementById("motor"+motorIdx+"_maxPower").value = motorSettings.maxPower;
    document.getElementById("motor"+motorIdx+"_responseTime").value = motorSettings.responseTime;
}

function getBatterySettingsFromForm(){
    var batterySettings = {};

    batterySettings.minVoltage = parseFloat(document.getElementById("battery_minVoltage").value);
    batterySettings.maxVoltage = parseFloat(document.getElementById("battery_maxVoltage").value);

    return batterySettings;
}

function updateBatterySettingsForm(batterySettings){
    document.getElementById("battery_minVoltage").value = batterySettings.minVoltage;
    document.getElementById("battery_maxVoltage").value = batterySettings.maxVoltage;
}

function getSensorSettingsFromForm(){
    var sensorSettings = {};
    sensorSettings.currentFactor = parseFloat(document.getElementById("sensors_currentFactor").value);
    sensorSettings.voltageFactor = parseFloat(document.getElementById("sensors_voltageFactor").value);
    sensorSettings.updateInterval = parseInt(document.getElementById("sensors_updateInterval").value);

    return sensorSettings;
}

function updateSensorSettingsForm(sensorSettings){
    document.getElementById("sensors_currentFactor").value = sensorSettings.currentFactor;
    document.getElementById("sensors_voltageFactor").value = sensorSettings.voltageFactor;
    document.getElementById("sensors_updateInterval").value = sensorSettings.updateInterval;
}

function getAccessorySettingsFromForm(){
    var accessorySettings = {};
    accessorySettings.maxLedPower = parseInt(document.getElementById("accesories_maxLedPower").value);
    accessorySettings.ledChannel = parseInt(document.getElementById("accesories_ledChannel").value);

    return accessorySettings;
}

function updateAccessorySettingsForm(accesorySettings){
    document.getElementById("accesories_maxLedPower").value = accesorySettings.maxLedPower;
    document.getElementById("accesories_ledChannel").value = accesorySettings.ledChannel;
}

function attachMotorSettingsForm(motorSettings,motorIdx){
    console.log("Attaching motor settings form to dom");

    const propulsionSystemSettings = document.getElementById("propulsionSystemSettings");
    
    const formDiv = document.createElement("div");
    formDiv.classList.add("card");
    formDiv.classList.add("bg-light");

    const header = document.createElement("h6");
    header.innerHTML = "Motor " + motorIdx;
    header.classList.add("card-header");
    formDiv.appendChild(header);

    const form = document.createElement("form");
    form.id = "motor"+motorIdx+"_form";
    form.classList.add("card-body");
   
    var units = ["","","%","%","ms"];
    var atributes = ["channel","polarity","maxPower","minPower","responseTime"];
    var values = [motorSettings.channel,motorSettings.polarity ? 1:0,motorSettings.minPower,motorSettings.maxPower,motorSettings.responseTime]

    for( var i = 0; i < 5; i++){
        var inputId = "motor"+motorIdx+"_"+atributes[i];
        const row = document.createElement("div");
        row.classList.add("form-group");
        row.classList.add("row");
        const label = document.createElement("label");
        label.for = inputId;
        label.classList.add("col-sm-3");
        label.classList.add("col-form-label");
        label.innerHTML = atributes[i];
        row.appendChild(label);

        var input = document.createElement("input");
        input.type = "number";
        input.classList.add("col-sm-3");
        input.classList.add("form-control");
        input.id = inputId;
        input.value = values[i];
        row.appendChild(input);

        var span = document.createElement("span");
        span.style = "margin-left:10px;";
        span.innerHTML = units[i];
        row.appendChild(span);

        form.appendChild(row);
    }
    formDiv.appendChild(form);
    propulsionSystemSettings.appendChild(formDiv);
}

function settings_initForms(){
    console.log("Initializing page");
    console.log("adding motor settings forms to settings page")
    for( var i = 0; i < 4; i++){
        attachMotorSettingsForm(settings.outputSettings.propulsionSystem.motors[i],i)
    }

    updateOutputSettingsForms(settings);
}