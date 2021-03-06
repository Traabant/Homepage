var tempsApiURL = '/api/weather/get-temps';
const getJsonData = new XMLHttpRequest();

getJsonData.open("GET", tempsApiURL);
getJsonData.send();

var tempsData;


getJsonData.onreadystatechange = (e) => {    
    if(getJsonData.readyState == 4 && getJsonData.status == 200){
      response = getJsonData.responseText;
      tempsData = JSON.parse(response);
      makeGraf();
    }   
  }
function makeGraf(){
    var ctx = document.getElementById('myChart').getContext('2d');
    var myChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: tempsData.timestamps,
            datasets: [{
                label: 'Temp',
                data: tempsData.temps,
                fill: false,
                pointRadius: 1,
                pointBackgroundColor:'rgba(255, 99, 132, 0.2)',
                pointBorderColor:'rgba(255, 99, 132, 0.2)',
                backgroundColor:'rgba(255, 99, 132, 0.2)',          
                
                borderColor: [
                    'rgb(75, 192, 192)',                   
                ],
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: true
                    }
                }],
                xAxes:[{
                    ticks:{
                        maxTicksLimit:6
                    }                    
                }]
                
            }
        }
    });
}