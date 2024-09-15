from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

@app.route('/')
def home():
    # Get the referer header to know where the request dey come from
    referer_url = request.headers.get('Referer')

    if referer_url:
        message = f'Redirect came from: {referer_url}'
    else:
        message = 'No redirection detected'

    # Send the referer URL to the frontend (or empty if not found)
    return render_template('index.html', referer_url=referer_url or "None")

# HTML route where you go use to display the referer
@app.route('/get-referer')
def get_referer():
    referer_url = request.headers.get('Referer')
    return jsonify(referer_url=referer_url or "None")


app.run(host='0.0.0.0', port=8080,debug=True)
