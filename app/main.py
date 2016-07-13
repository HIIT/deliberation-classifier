from flask import *

try:
    import git ## for versions
    repo = git.Repo("../")

    __version = str( repo.head.commit )

except:
    __version = 'no-version'

app = Flask(__name__)

@app.route("/")
def index():
    return send_from_directory( 'static' , 'index.html' )

## NEVER USE FOR REAL ANALYSIS, A TOY EXAMPLE
@app.route('/api/alpha/dqi/', methods=['POST'] )
def alpha_analyze():

    from alpha import dqi

    if 'text' not in request.form:
        return jsonify(
                    code = 400 ,
                    msg = 'Check your post request has a text attribute'
                ) , 400

    jl = dqi.predict( request.form['text'] )[0]

    jl = int(jl)

    return jsonify( { 'value' : jl , 'version' : __version } )

@app.route('/api/current/dqi/', methods=['POST'] )
def current_analysis():
    return alpha_analyze()

@app.route('/api/current/version/', methods=['GET'] )
def current_version():

    return jsonify( {'version' : __version } )


if __name__ == "__main__":
    app.run( debug = True )
