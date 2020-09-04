import React from 'react';
import { makeStyles } from '@material-ui/core/styles';

import './Home.css';

class Home extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            record: false
        }
    }

    componentDidMount() {
        var i = 0;
        var txt = 'Team Comrades '; /* The text */
        var speed = 125; /* The speed/duration of the effect in milliseconds */

        function typeWriter() {
            if (i < txt.length) {
                document.getElementById("typewriter").innerHTML += txt.charAt(i);
                i++;
                setTimeout(typeWriter, speed);
            }
        }

        typeWriter()
    }

    styles = makeStyles(theme => ({

    }));

    render() {
        return (
            <div style={{
                fontFamily: 'Riona Sans,sans-serif',
                fontWeight: 'bolder',
                fontSize: '200%',
                fontStyle: 'italic',
                color: '#047BD5',
                margin: 'auto',
                display: 'flex',
                height: '40vh',
                justifyContent: 'center',
                alignItems: 'center'
            }} >
                <div id="typewriter" />
            </div>
        )
    }
}

export default Home