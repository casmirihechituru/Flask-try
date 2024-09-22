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


@app.route('/check_subscription/<subscription_code>', methods=['GET'])
def check_subscription(subscription_code):
    url = f"https://api.paystack.co/subscription/{subscription_code}"
    headers = {
        "Authorization": "Bearer sk_test_9db0fe12af0a5cd5d29b29471888d5057b813522"  # Replace with your own secret key
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:  # Check if Paystack API call is successful
        data = response.json()
        if data['status']:  # Check if the request was successful
            subscription_status = data['data']['status']  # Subscription status
            # You can check the status and return a message accordingly
            if subscription_status == 'active':
                return jsonify({"message": "Subscription is active"}), 200
            elif subscription_status == 'complete':
                return jsonify({"message": "Subscription has been completed"}), 200
            elif subscription_status == 'cancelled':
                return jsonify({"message": "Subscription has been cancelled"}), 200
            elif subscription_status == 'expired':
                return jsonify({"message": "Subscription has expired"}), 200
            else:
                return jsonify({"message": "Unknown subscription status"}), 400
        else:
            return jsonify({"message": "Failed to retrieve subscription status"}), 400
    else:
        return jsonify({"message": "Error connecting to Paystack API"}), 500
app.run(host='0.0.0.0', port=8080,debug=True)
