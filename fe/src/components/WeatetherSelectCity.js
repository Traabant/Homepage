import React from 'react';

export default class Weather extends React.Component{
    constructor(props){
        super(props)
        this.state = {
            value: "",
        };

        this.handleChange = this.handleChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
    }

    handleChange(event){
        this.setState({value: event.target.value})        
    }

    handleSubmit(event) {
        this.props.changeCity(this.state.value)
        event.preventDefault();
      }

    render(){
        return(
            <div>
                <form onSubmit={this.handleSubmit}>
                    <input type="text" value={this.state.value} onChange={this.handleChange}></input>
                    <button type="button" class="btn btn-primary" type="submit" >Submit</button>
                </form>
            </div>
        )
    }
}