const CHANNEL_COUNT = 8;

//inputSettings is an intermediate buffer containing information on the events and buttons that are connected to this channel
//These input channel data also has to be stored later on
var inputSettings= [
    { //Channel 0
        forwardKey: "x",
        reverseKey: "",
        activeValue: 1,
        toggleableInput: true,
        active: false,
        button: "armBtn"
    },
    { //Channel 1
        forwardKey: "q",
        reverseKey: "a",
        activeValue: 100,
        toggleableInput: false
    },
    { //Channel 2
        forwardKey: "e",
        reverseKey: "d",
        activeValue: 100,
        toggleableInput: false
    },
    { //Channel 3
        forwardKey: "w",
        reverseKey: "s",
        activeValue: 100,
        toggleableInput: false
    },
    { //Channel 4
        forwardKey: "l",
        reverseKey: "",
        activeValue: 100,
        toggleableInput: true,
        active: false,
        button: "lightBtn"
    },
    { //Channel 5
        forwardKey: "",
        reverseKey: "",
        activeValue: 0,
        toggleableInput: false
    },
    { //Channel 6
        forwardKey: "",
        reverseKey: "",
        activeValue: 0,
        toggleableInput: false
    },
    { //Channel 7
        forwardKey: "",
        reverseKey: "",
        activeValue: 0,
        toggleableInput: false
    }
];

// The outputChannels is a buffer that is supposed to be decoupled from UI and OutputDevices
// The final data buffer and the information that actually gets send down to the eduROV

var timeStampts = [];
var currentBuffer = [1.2,4.5,5.3];
var voltageBuffer = [];
var startTs = 0;
var measurementStarted = false;

var outputChannels = {channels:[0,0,0,0,0,0,0,0]}


var settingsRefreshRequested = false;
var settings={
    outputSettings:{
        propulsionSystem:{
            armChannel: 0,
            motors:[
                {
                    channel: 1,
                    polarity: true, 
                    minPower: 20,
                    maxPower: 80,
                    responseTime: 1000
                },
                {
                    channel: 2,
                    polarity: true, 
                    minPower: 20,
                    maxPower: 80,
                    responseTime: 1000
                },
                {
                    channel: 3,
                    polarity: true, 
                    minPower: 20,
                    maxPower: 80,
                    responseTime: 1000
                },
                {
                    channel: 3,
                    polarity: true, 
                    minPower: 20,
                    maxPower: 80,
                    responseTime: 1000
                }
            ]
        },
        battery:{
            maxVoltage: 12.6,
            minVoltage: 6.2
        },
        sensors:{
            updateInterval: 100,
            currentFactor: 0.3,
            voltageFactor: 0.2
        },
        accessories:{
            ledChannel: 4,
            maxLedPower: 75
        }
    }
}