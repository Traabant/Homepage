import React from 'react';
import {BrowserRouter as Router } from 'react-router-dom';
import BaseRouter from './components/Routs'
import Navbar from './components/Navbar';



function App() {
  return (
    <div className="App">
      
        <Router>
          <Navbar />
          <div class="container">
            <BaseRouter />
          </div>
        </Router>
     
    </div>
  );
}

export default App;
