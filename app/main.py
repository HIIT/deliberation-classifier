from flask import *

app = Flask(__name__)

@app.route("/")
def index():
    return send_from_directory( 'static' , 'index.html' )

## NEVER USE FOR REAL ANALYSIS, A TOY EXAMPLE
@app.route('/api/alpha/dqi', methods=['POST'] )
def alpha_analyze():
    if 'text' not in request.form:
        return jsonify(
                    code = 400 ,
                    msg = 'Check your post request has a text attribute'
                ) , 400
    return request.form['text']

if __name__ == "__main__":
    app.run()
