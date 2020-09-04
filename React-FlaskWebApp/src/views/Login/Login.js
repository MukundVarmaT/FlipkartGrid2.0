import React, { useState } from "react";
import axios from "axios";
import {
    FormGroup,
    FormControl,
    InputLabel,
    Input,
    Container,
    Button
} from "@material-ui/core";

export default function Login() {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");

    function handleSubmit() {
        var btn = document.getElementById('submitbtn')
        btn.disabled = true

        if (username.length > 0 && password.length > 0) {
            var formdata = new FormData()
            formdata.set('username', username)
            formdata.set('password', password)

            var headers = {
                headers: {
                    'Access-Control-Allow-Origin': '*',
                    'Content-Type': 'multipart/form-data'
                }
            }

            axios.post('http://localhost:5000/token', formdata, headers)
                .then((res) => {
                    var data = res.data
                    switch (data.substring(0, 3)) {
                        case '404':
                        case '405':
                        case '500':
                            alert(data)
                            window.location.href = "/auth"
                            break;
                        default:
                            localStorage.setItem('gridToken', data)
                            alert('Token has been saved')
                            window.location.href = '/denoise'
                    }
                })
        }
        else{
            alert('Empty Username / Password')
            window.location.href = '/auth'
        }
    }

    function handleName(e) {
        setUsername(e.target.value)
    }
    function handlePasswd(e) {
        setPassword(e.target.value)
    }

    return (
        <div style={{ width: '30%', margin: 'auto', textAlign: 'center' }}>
            <Container>
                <br />
                <div style={{
                    fontFamily: 'Riona Sans,sans-serif',
                    fontWeight: 'bolder',
                    fontSize: '200%',
                    fontStyle: 'italic',
                    color: '#047BD5',
                    display: 'flex',
                    justifyContent: 'center',
                    alignItems: 'center'
                }} >
                    Retrieve your token
                </div>
                <br />
                <form>
                    <FormGroup>
                        <FormControl>
                            <InputLabel>Username</InputLabel>
                            <Input id="input1" onChange={handleName} />
                        </FormControl>
                    </FormGroup>
                    <br />
                    <FormGroup>
                        <FormControl>
                            <InputLabel>Password</InputLabel>
                            <Input id="input2" type="password" onChange={handlePasswd} />
                        </FormControl>
                    </FormGroup>
                </form>
                <br />
                <Button id="submitbtn" onClick={handleSubmit}>
                    Login
                </Button>
                <br />
            </Container>
            <br />
        </div>
    );
}