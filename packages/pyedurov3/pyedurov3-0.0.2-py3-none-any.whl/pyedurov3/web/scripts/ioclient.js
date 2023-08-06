var client = null;

function io_send(data) {
    if(data.outputSettings != null){
        console.log("Sending")
        console.log(JSON.stringify(data));
        if (!(client && client.readyState == 1))
        {
            console.log("websocket connection inactive");
        }
    }

    if (client && client.readyState == 1)
    {

        client.send(JSON.stringify(data));
    }
}

function io_close(){
    if (client)
    {
        client.close();
    }
}

function io_open(address, message_handler, open_handler, close_handler) {

    console.log("Starting I/O server client");
    
    // Create WebSocket connection.
    client = new WebSocket(address + ":8082");
    
    client.addEventListener(
        'open', 
        ()  =>
        {
            console.log("I/O server Connection made");
            client.send("Start");
            open_handler();
        }
    );            
    client.addEventListener('message', message_handler);
    client.addEventListener(
        'close', 
        () => 
        {
            console.log("I/O server connection closed"); 
            close_handler();
            client = null;
        }
    );
}