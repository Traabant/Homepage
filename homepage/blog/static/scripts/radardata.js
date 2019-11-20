// alert("hello word");

const url = "http://127.0.0.1:8000/weather/get-images";
const HTTP = new XMLHttpRequest();

HTTP.open("GET", url);
HTTP.send();

var response;
var obj;

// alert("hello word");

function writeOut(){
  // console.log(response);
  // console.log(Object.keys(obj.data))

  var img = document.createElement("img");
  // var div = document.createElement("div")

  for(let i =0; i < Object.keys(obj.data).length ; i++){
    console.log(obj['data'][i])
    img.src = obj['data'][i]
    let radarID = document.getElementById("radar-img");
    radarID.appendChild(img);
  }
}

HTTP.onreadystatechange = (e) => {    
  if(HTTP.readyState == 4 && HTTP.status == 200){
    response = HTTP.responseText;
    obj = JSON.parse(response);
    writeOut(); 
  }   
}

  


  

  
 
