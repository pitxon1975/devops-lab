from flask import Flask
import platform
import socket
import getpass

app = Flask(__name__)

@app.route('/')
def hello_world():
    return f"""
    <h1>ESTADO DEL NODO DEVOPS</h1>
    <p><b>SO:</b> {platform.system()} {platform.release()}</p>
    <p><b>Hostname:</b> {socket.gethostname()}</p>
    <p><b>Usuario Container:</b> {getpass.getuser()}</p>
    """

if __name__ == '__main__':
    # Escuchar en 0.0.0.0 es VITAL para Docker. 
    # Si usas 127.0.0.1, el contenedor se bloquea a sí mismo.
    app.run(host='0.0.0.0', port=5000)
