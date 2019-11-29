
const apiURL = "http://127.0.0.1:8000/weather/get-images";
const getJsonData = new XMLHttpRequest();
const getIMG = new XMLHttpRequest();

var response;
var imageData;
var images = new Array;


getJsonData.open("GET", apiURL);
getJsonData.send();


function writeOut(){
  let radarID = document.getElementById("radar-img");
  for(let i =0; i < Object.keys(imageData.data).length ; i++){
    images[i] = document.createElement("img");
    images[i].src = imageData['data'][i];
    images[i].style.visibility = 'hidden';
    images[i].className = 'overlayImages';
    radarID.appendChild(images[i]);
    console.log(images[i].attributes.src)
    }

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
