import React from 'react';

function Navbar(props){
    var sites = populateSites();      
      return (
        <nav class="navbar navbar-expand-md navbar-dark bg-dark mb-4">
            <a class="navbar-brand mr-4" href="/">Traabant's Homepage</a>
            <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarToggle" aria-controls="navbarToggle" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarToggle">
                <div class="collapse navbar-collapse" id="navbarToggle">
                    <div class="navbar-nav mr-auto">
                        {createNavBar(sites)}                  
                    </div>                        
                </div>
            </div>                     
        </nav >

    );
}

function createNavBar(items){
    var content = [];    
    for(var i=0 ; i < items.length; i++){
        content.push(
            <a href={items[i].link} class="nav-link">{items[i].name}</a>
                        
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