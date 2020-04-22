import React from 'react';

function Navbar(){
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
        new Site("Home", ""), 
        new Site("Weather", ""),
        new Site("Consuption", ""),
        new Site("API", ""),
        new Site("Test",""),
        ];
}

class Site {
    constructor(name, link) {
        this.name = name;
        this.link = link;    
    }
}

export default Navbar;