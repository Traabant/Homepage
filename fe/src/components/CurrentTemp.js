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
            <div class="col-md-4">
                <div class="card-header">
                    Current Temp
                </div>
               
                    {!this.state.curTemp ? ( 
                        <div class="card-body">loading...</div>
                    ) : (
                        <div class="card-body"> {this.state.curTemp} C</div>
                    )
                    }
                
            </div>
        )
    }    
}

