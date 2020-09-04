# Flipkart Grid 2.0 : Team COMRADES - SDE - Noise Cancellation

React + Flask WebApp for interacting with a modified ConvTasNet developed by us. 

### How to Run

```bash
cd flask
pip3 install -r requirements.txt
python3 server.py
```

Flags : --prod
To switch configs like MySQL connection configs, secrets, etc.

Now, this WebApp is ready for interacting with you at http://localhost:5000/

### How this stuff works

The whole architecture is a Stateless one. Retrieve a JWT and send it everytime you want to denoise an audio

This WebApp is based on Flask and Flask-SocketIO. We have production-built the React WebApp and serve it using Flask itself. The socket communication occurs via two events : send and receive. When the recording is stopped, a callback is called and the recorded __NOISY__ audio along with JWT is sent to the socket via socket.emit(...) ; 

There comes the magic part!!! Once Flask validates the JWT signature, it writes the audio blob to a file. A random string of a fixed length is generated to be appended to the file name. This file is processed by inference scripts. Finally, an __ENHANCED__ version of the noisy audio is saved as file in a sub directory named output/.

Flask now converts enhanced audio to bytestream, deletes the files created and emits the bytestream.

### Left-out Improvements

+ SQL-Alchemy
+ Dockerfile
+ NGINX Configs
