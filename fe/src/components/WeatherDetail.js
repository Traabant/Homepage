import React from 'react';

export default class Weather extends React.Component{
    state={

    }

    convert_from_K(kelvin) {
        return (kelvin - 273.15)
    }

    render(){
        return(
            <div>
                {/* {this.props.weather} */}
                <div>
                    <div>
                        {this.props.weather.weather[0].main}
                    </div>
                    <div>
                        temp is {this.convert_from_K(this.props.weather.main.temp).toFixed(1)}
                    </div>
                    <div>
                        for time {this.props.weather.dt_txt}
                    </div> 
                </div>
            </div>
        )
    }
}
