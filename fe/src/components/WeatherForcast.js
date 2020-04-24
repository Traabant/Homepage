import React from 'react';

import WeatherDeatil from './WeatherDetail';

import '../Weather.css'

export default class Weather extends React.Component{
    
    constructor(props){
        super(props);
        this.state = {
            loading: true,
            raw_data: null,
            data: [],
            selectedCity: props.selectedCity,
            city: null, 
            URL: null
        }
    }
    
    componentDidUpdate(prevProps){       
        if (prevProps.selectedCity !== this.props.selectedCity){
            this.setState({
                selectedCity: this.props.selectedCity,
            })
            ;
            this.downloadData(this.props.selectedCity);
        }
        
    }

    async downloadData(cityName){
        var URL = "http://api.openweathermap.org/data/2.5/forecast?q=" + cityName +"&appid=f38cd70321c379afac4b55fb00a3be7a";
        this.setState({URL: URL})
        // console.log(URL)
        var response = await fetch(URL);
        var data = await response.json();
        // console.log(data);
        this.setState({raw_data: data});
        this.setState({city: this.state.raw_data.city.name}) 
        
        const listItems = this.state.raw_data.list.map((item) =>
            <WeatherDeatil weather={item} />
        );        
        this.setState({data: listItems})
        }


    
    componentDidMount(){
        this.downloadData(this.state.selectedCity);
    }
        

    convert_from_K(kelvin) {
        return (kelvin - 273.15)
    }


    render(){
        return(            
            <div class="col-md-12" >  
                <div class="wraper">
                    <div class="Weather-forecast"> 
                    <div>{this.state.city}</div>
                        {this.state.data.length === 0 ? ( 
                            <div>loading...</div>
                        ) : (
                            
                            <div class="card-deck mb-3 text-center"> 
                                {this.state.data}
                            </div>
                        )
                        }
                    </div>
                </div>
            </div>
        )
    }    

    
}