from flask import Flask

app = Flask(__name__)


@app.route("/")
def hello_world():
    return """
                <H2 style='text-align:center;'>This is a CICD example increment the number then push</H2>
                <H1 style='text-align:center;'>
                5
                </H1>
            """
