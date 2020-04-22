import React from 'react';


export default class CurrentTemp extends React.Component{
    
    state = {
        curTemp: null,
    };

    async componentDidMount(){
        const end_point = "http://127.0.0.1:8000/api/weather/get-temps"

        const response = await fetch(end_point);
        const data = await response.json();
        console.log(data);
        this.setState({curTemp: data.temps[(data.temps.length -1)]});
    }
    
    render(){
        return(
            <div>
                <h1>Weather</h1>
                {!this.state.curTemp ? ( 
                    <div>loading...</div>
                ) : (
                    <div> Current temp is {this.state.curTemp} C</div>
                )
                }
            </div>
        )
    }    
}

