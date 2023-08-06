errorDictionary = {
        "E1":{
            "id":"E1",
            "name":"Tether Error",
            "short_description":"no network connection",
            "long_description":"The system does not have an active network connection via LAN or WLAN.",
            "help": "Make sure the network cable is properly connected.",
            "icon":"networkError.png"
        },
        "E2":{
            "id":"E2",
            "name":"Camera Error",
            "short_description":"camera not detected",
            "long_description":"The pi camera could not be started",
            "help": "Check the camera connection. Make sure the cable is inserted correctly",
            "icon":"cameraError.png"
        },
        "E3":{
            "id":"E3",
            "name":"Autopilot Board Error",
            "short_description":"microcontroller not detected",
            "long_description":"No serial device was found. The port could not be opened.",
            "help": "Make sure the microcontroller is properly connected and has power",
            "icon":"microcontrollerError.png"
        },
        "E6":{
            "id":"E6",
            "name":"Battery Error",
            "short_description":"battery empty",
            "long_description":"The battery voltage is lower than it should be.",
            "help": "Charge the battery.",
            "icon":"batteryError.png"
        }
    }