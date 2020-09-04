import React from 'react'

import { ReactMic } from 'react-mic'
import { makeStyles } from '@material-ui/core/styles';
import { 
    Button,
    Box } from '@material-ui/core'

import { socket } from '../../components/Socket'

import {
    Container,
} from 'reactstrap'

class Record extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            record: false,
            token: '',
        }
        this.onStop = this.onStop.bind(this)
    }

    getData = (data) => {
        if (typeof (data) === 'string') {
            alert(data)
            window.location.href = '/auth'
        }
        else {
            const blob = new Blob([data], { type: 'audio/wav' })
            const url = URL.createObjectURL(blob)
            const container = document.getElementById('output_container')
            const audioElement = document.createElement('audio');
            audioElement.setAttribute('controls', true);
            audioElement.setAttribute('id', 'player_in')
            container.appendChild(audioElement);
            const sourceElement = document.createElement('source');
            audioElement.appendChild(sourceElement);
            sourceElement.src = url;
            sourceElement.type = 'audio/wav';
        }
    }

    componentDidMount() {
        socket.on("receive", this.getData)
        var item = localStorage.getItem('gridToken')
        this.setState({
            ...this.state.record,
            token: item
        })
    }

    componentWillUnmount() {
        socket.off("receive")
    }

    styles = makeStyles(theme => ({

    }));

    handleRecording = () => {
        this.setState({ record: !this.state.record });
        const player_in = document.getElementById('player_in')
        if (player_in) {
            player_in.parentNode.removeChild(player_in)
        }
        const player_out = document.getElementById('player_out')
        if (player_out) {
            player_out.parentNode.removeChild(player_out)
        }
    }

    onData(recordedBlob) {
        console.log('Recording')
    }

    onStop(recordedBlob) {
        try {
            recordedBlob['token'] = this.state.token
            socket.emit('send', recordedBlob)
            const blob = new Blob([recordedBlob['blob']], { type: 'audio/wav' })
            const url = URL.createObjectURL(blob)
            const container = document.getElementById('input_container')
            const audioElement = document.createElement('audio');
            audioElement.setAttribute('controls', true);
            audioElement.setAttribute('id', 'player_out')
            container.appendChild(audioElement);
            const sourceElement = document.createElement('source');
            audioElement.appendChild(sourceElement);
            sourceElement.src = url;
            sourceElement.type = 'audio/wav';
        }
        catch (err) {
            console.log(err)
        }
    }

    render() {
        return (
            <div>
                <br />
                <h3 style={{
                    fontFamily: 'Riona Sans,sans-serif',
                    fontWeight: 'bold',
                    textAlign: 'center'
                }}>
                    Welcome to our Denoiser!
                </h3>
                <br />
                <Container style={{
                    marginBottom: '50px',
                    justifyContent: 'center',
                    alignItems: 'center'
                }}>
                    <div style={{ textAlign: 'center' }}>
                        <ReactMic
                            record={this.state.record}
                            className="sound-wave"
                            mimeType="audio/wav"
                            onStop={this.onStop}
                            onData={this.onData}
                            strokeColor="white"
                            backgroundColor="#047BD5"
                            noiseSuppression="true"
                            echoCancellation="true"
                        />
                        <br />
                        <Button style={{ marginTop: '15px', marginBottom: '20px' }} variant="contained" color="secondary" onClick={this.handleRecording} >Start / Stop</Button>
                        <br />
                        <Box display="flex" justifyContent="center" flexDirection="row">
                            <Box p={1} mx="auto">
                                <h5 style={{
                                    fontFamily: 'Riona Sans,sans-serif'
                                }}>
                                    Input Audio :
                                </h5>
                                <div id="input_container" />
                            </Box>
                            <Box p={1} mx="auto">
                                <h5 style={{
                                    fontFamily: 'Riona Sans,sans-serif'
                                }}>
                                    Denoised Audio :
                                </h5>
                                <div id="output_container" />
                            </Box>                           
                        </Box>
                    </div>
                </Container>
            </div>
        )
    }
}

export default Record