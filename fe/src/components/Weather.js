import React from 'react';
import CurrentTemp from './CurrentTemp';
import WeatherForcast from './WeatherForcast';

export default class Weather extends React.Component{
    
  
    render(){
        return(
            <div class="row">
                <div class="col-md-12">
                 <h1>Weather</h1>
                <CurrentTemp />
                <WeatherForcast />
                </div>
            </div>
        )
    }
    
}

