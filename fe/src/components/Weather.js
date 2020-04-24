import React from 'react';
import CurrentTemp from './CurrentTemp';
import WeatherForcast from './WeatherForcast';
import WeatherSelectCity from './WeatetherSelectCity';

export default class Weather extends React.Component{
    constructor(props){
        super(props)
        this.state ={
            selectedCity: "Ostrava",
        };
    }
    
    

    changeCity(newCity){
         this.setState({
             selectedCity: newCity
         })
    }
  
    render(){
        return(
            <div class="row">
                <div class="col-md-12">
                 <h1>Weather</h1>
                <WeatherSelectCity 
                    changeCity={this.changeCity.bind(this)}
                />
                <CurrentTemp />
                <WeatherForcast 
                    selectedCity={this.state.selectedCity}
                />
                </div>
            </div>
        )
    }
    
}

