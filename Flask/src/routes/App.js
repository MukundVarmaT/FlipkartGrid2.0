import React from 'react';
import { Router, Route, Switch } from 'react-router-dom'
import { createBrowserHistory } from 'history'

import NavBar from '../components/NavBar'

import Home from '../views/Home/Home'
import Record from '../views/Record/Record';
import CardGrid from '../components/CardGrid';
import Login from '../views/Login/Login';

var hist = createBrowserHistory();

var routes = [
    { path: "/", component: Home },
    { path: "/denoise", component: Record },
    { path: "/auth", component: Login}
];

export default class App extends React.Component {

    render() {
        return (
            <div>
                <NavBar />
                <Router history={hist}>
                    <Switch>
                        {
                            routes.map((prop, key) => {
                                return <Route exact path={prop.path} key={key} component={prop.component} />;
                            })
                        }
                    </Switch>
                </Router>
                <CardGrid />
            </div>
        )
    }
}