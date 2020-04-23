import React from 'react';

function Navbar(props){
    var sites = populateSites();      
      return (
        <div>
            <div>
                {createNavBar(sites)}                  
            </div>              
        </div>
    );
}

function createNavBar(items){
    var content = [];    
    for(var i=0 ; i < items.length; i++){
        content.push(
            <div>
                <a href={items[i].link}>{items[i].name}</a>                
            </div>
        );
    };
    return content
}

function populateSites(){
    return [
        new Site("Home", "/"), 
        new Site("Weather", "/weather"),
        new Site("Consuption", "/consuption"),
        new Site("API", "/api"),
        new Site("Test","/test"),
        ];
}

class Site {
    constructor(name, link) {
        this.name = name;
        this.link = link;    
    }
}

export default Navbar;