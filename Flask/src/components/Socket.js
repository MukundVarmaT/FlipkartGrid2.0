import socketIOClient from 'socket.io-client'

export var socket = socketIOClient('http://localhost:5000/')
