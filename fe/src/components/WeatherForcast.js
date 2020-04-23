import React from 'react';

import WeatherDeatil from './WeatherDetail';

export default class Weather extends React.Component{
    state = {
        loading: true,
        raw_data: null,
        data: [],
    }
  
    async componentDidMount(){
        const URL = "http://api.openweathermap.org/data/2.5/forecast?q=ostrava&appid=f38cd70321c379afac4b55fb00a3be7a";

        const response = await fetch(URL);
        const data = await response.json();
        console.log(data);
        this.setState({raw_data: data});
        
        const listItems = this.state.raw_data.list.map((item) =>
            <WeatherDeatil weather={item} />
        );        
        this.setState({data: listItems})
        }

        

    convert_from_K(kelvin) {
        return (kelvin - 273.15)
    }


    render(){
        return(
            <div class="col-md-12">    
                {this.state.data.length === 0 ? ( 
                    <div>loading...</div>
                ) : (
                    <div class="card-deck mb-3 text-center"> 
                        {this.state.data}
                    </div>
                )
                }
            </div>
        )
    }    

    
}