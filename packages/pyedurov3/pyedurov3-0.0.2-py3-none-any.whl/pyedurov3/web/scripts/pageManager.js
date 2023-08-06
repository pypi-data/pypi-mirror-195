/**
 * Handles resize event and cinema mode to create a dynamic layout
 * https://github.com/trolllabs/eduROV
 */

var MINIMUM_PANEL_WIDTH = 250;
var pad = 10;
cinema = false;
page="main"

function switch_to_page(name){

    console.log("Switching to:"+name)

    var mainPage = document.getElementsByClassName("main-page");
    var infoPage = document.getElementsByClassName("info-page");
    var settingsPage = document.getElementsByClassName("settings-page");

    var body = document.getElementsByTagName("body");

    mainPage[0].style.visibility = "hidden";
    settingsPage[0].style.visibility = "hidden";
    infoPage[0].style.visibility = "hidden";

   switch(name){
    case "settings-page": 
        settingsPage[0].style.visibility = "visible";
        body[0].style.overflow = "visible"
        break;
    case "info-page":
        infoPage[0].style.visibility = "visible";
        body[0].style.overflow = "visible"
        break;
    default:
        window.scrollTo(0,0); 
        mainPage[0].style.visibility = "visible";
        body[0].style.overflow = "hidden"
        break;
   }
   page_update_size()

}

function set_cinema(cinema_mode){
    if (!cinema_mode){
        var panels = document.getElementsByClassName("side-panel");
        panels[0].style.visibility = "visible";
        panels[1].style.visibility = "visible";
        var img = document.getElementsByClassName("center-panel")[0];
        img.style.position = "relative";
        img.style.width = "100%";
        img.style.marginLeft = "0";
    } else {
        var panels = document.getElementsByClassName("side-panel");
        panels[0].style.visibility = "hidden";
        panels[1].style.visibility = "hidden";
        var img = document.getElementsByClassName("center-panel")[0];
        img.style.position = "absolute";
    }
    cinema = cinema_mode
    set_size();
}

function page_update_size(){
    var bodW = document.body.clientWidth;
    var bodH = document.body.clientHeight;

    if(page=="main-page"){
        var main = document.getElementsByClassName("main-page")[0];
        main.style.width = `${bodW}px`;
        console.log(bodW)
        main.style.height = `${bodH}px`;
    }
    else{
        var container =  document.getElementsByClassName("main-page")[0];
        var width = 0;
        var height = 0;
        container.style.width = `${width}px`;
        container.style.height = `${height}px`;
    }
}