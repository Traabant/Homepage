const consuptionApiURL = '/api/weather/get-consuption';
const getConsuptionData = new XMLHttpRequest();

getConsuptionData.open("GET", consuptionApiURL);
getConsuptionData.send();

var consuptionData;

getConsuptionData.onreadystatechange = (e) => {
    getConsuptionData.onreadystatechange = (e) => {    
        if(getConsuptionData.readyState == 4 && getConsuptionData.status == 200){
          response = getConsuptionData.responseText;
          consuptionData = JSON.parse(response);
          makeGraf();
        }   
      }
}

function makeGraf(){
    var ctx = document.getElementById('myChart').getContext('2d');
    var myChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: consuptionData.dates,
            datasets: [{
                label: 'consuption',
                data: consuptionData.consuption,
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
                        beginAtZero: false
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