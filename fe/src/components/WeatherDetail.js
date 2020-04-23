import React from 'react';

export default class Weather extends React.Component{
    state={

    }

    convert_from_K(kelvin) {
        return (kelvin - 273.15)
    }

    render(){
        return(
            // <div class="card mb-8 shadow-sm">
            <div class="col-md-4"> 
                {/* {this.props.weather} */}
                {/* <div class="media content-section"> */}
                    <div class="card-header">
                        {this.props.weather.dt_txt}
                    </div> 
                    <div class="card-body">
                        <div class="my-0 font-weight-normal">
                            {this.props.weather.weather[0].main}
                        </div>
                        <div class="my-0 font-weight-normal">
                            temp is {this.convert_from_K(this.props.weather.main.temp).toFixed(1)}
                        </div>
                    </div>
                    
                {/* </div> */}
            </div>
        )
    }
}
