import React from "react";
import {Route} from 'react-router-dom';

import Weather from './Weather';
import API from './API';
import Comsuption from './Comsuption';

const BaseRouter = () => (
    <div>
        <Route exact  path='/' component= {Weather} />
        <Route exact path='/weather' component= {Weather} />
        <Route exact path='/consuption' component= {Comsuption} />
        <Route exact path='/api' component= { API } />
    </div>
);

export default BaseRouter;