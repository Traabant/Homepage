import React from 'react';

export default class Weather extends React.Component{
    state = {
        loading: true,
        data: null,
    }
  
    async componentDidMount(){
        const URL = "http://api.openweathermap.org/data/2.5/forecast?q=ostrava&appid=f38cd70321c379afac4b55fb00a3be7a";

        const response = await fetch(URL);
        const data = await response.json();
        console.log(data);
        this.setState({data: data});
        
        }

    convert_from_K(kelvin) {
        return (kelvin - 273.15)
    }

    render(){
        return(
            <div>               
                {!this.state.data ? ( 
                    <div>loading...</div>
                ) : (
                    <div> {this.convert_from_K(this.state.data.list[0].main.temp)}</div>
                )
                }
            </div>
        )
    }    

    
}