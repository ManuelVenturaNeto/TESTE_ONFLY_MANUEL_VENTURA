from flask import Flask, send_from_directory

app = Flask(__name__)


@app.route("/download/<filename>")
def download_file(filename):
    return send_from_directory("/app/outputs", filename)
