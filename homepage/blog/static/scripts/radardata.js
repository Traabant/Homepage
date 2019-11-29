
const apiURL = "http://traabant.pythonanywhere.com/weather/get-images";
// const apiURL = "http://127.0.0.1:8000/weather/get-images";
const getJsonData = new XMLHttpRequest();
const getIMG = new XMLHttpRequest();

var response;
var imageData;
var images = new Array;

var backgroudImage = document.getElementById("backgroundImage");
var citiesLayer = document.getElementById("citiesLayer");

var radarID = document.getElementById("radar-img");


getJsonData.open("GET", apiURL);
getJsonData.send();

window.addEventListener("resize", resizeAnamationBox);


function writeOut(){
  

  for(let i =0; i < Object.keys(imageData.data).length ; i++){
    images[i] = document.createElement("img");
    images[i].src = imageData['data'][i];
    images[i].style.visibility = 'hidden';
    images[i].className = 'overlayImages';    
    radarID.appendChild(images[i]);
    }
  images = images.reverse();
  resizeAnamationBox();
  cycle(); 
}

getJsonData.onreadystatechange = (e) => {    
  if(getJsonData.readyState == 4 && getJsonData.status == 200){
    response = getJsonData.responseText;
    imageData = JSON.parse(response);
    writeOut(); 
  }   
}

async function cycle(){
  while(true){
    for(let i =0; i < Object.keys(imageData.data).length ; i++){
      images[i].style.visibility = 'visible';
      await sleep(300)
      images[i].style.visibility = 'hidden';
    }
  }  
}

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

function getWidthAnimationBox(){
  let parrent = document.getElementById("radar-img");
  let parrentWidht = parrent.offsetWidth;
  console.log(parrentWidht);
  return parrentWidht;
}

function getHeightAnimationBox(){
  let parrent = document.getElementById("backgroundImage");
  let parrentHeight = parrent.height;
  return parrentHeight;

}

function resizeAnamationBox(){
  var widthToSet = getWidthAnimationBox();
  backgroudImage.width = widthToSet;
  citiesLayer.width = widthToSet;
  var heightToSet = getHeightAnimationBox();
  radarID.style.minHeight = heightToSet + "px";
  for(let i =0; i < Object.keys(imageData.data).length ; i++){
    images[i].width = widthToSet;
  }
}

