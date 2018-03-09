# This sample demonstrates a bare-bones implementation of the Square Connect OAuth flow:
#
# 1. A merchant clicks the authorization link served by the root path (http://localhost:8080/)  
# 2. The merchant signs in to Square and submits the Permissions form. Note that if the merchant
#    is already signed in to Square, and if the merchant has already authorized your application,
#    the OAuth flow automatically proceeds to the next step without presenting the Permissions form.
# 3. Square sends a request to your application's Redirect URL
#    (which should be set to http://localhost:8080/callback on your application dashboard)
# 4. The server extracts the authorization code provided in Square's request and passes it
#    along to the Obtain Token endpoint.
# 5. The Obtain Token endpoint returns an access token your application can use in subsequent requests
#    to the Connect API.
from flask import Flask, request
from bottle import get, static_file, run
import http.client, json
import requests
app = Flask(__name__)

# Your application's ID and secret, available from your application dashboard.
# application_id = 'sq0idp-bAHi1yTdB2xO5Hu6DbJFIA'
# application_secret = 'sq0csp-S5CnHqAcvV6Nm4sLuOxI3sF36tnH8QwrILR1Vl0QOVk'

application_id = 'sq0idp-jIC-SZibUADmo2L1gLk03A'
application_secret = 'sq0csp-9E5UxkFwGvzf01GrFtEU3TFZqL1TLOq5vzNHLBTL6lE'



# Headers to provide to OAuth API endpoints
oauth_request_headers = { 'Authorization': 'Client ' + application_secret,
                          'Accept': 'application/json',
                          'Content-Type': 'application/json'}

# Serves the link that merchants click to authorize your application
@app.route('/')
def authorize():
  # return '''<a href="https://connect.squareup.com/oauth2/authorize?client_id={0}&scope=PAYMENTS_WRITE%20PAYMENTS_READ%20ITEMS_READ%20ORDERS_READ%20TIMECARDS_READ%20ORDERS_WRITE">Click here</a>
  #           to authorize the application.'''.format(application_id)
  return '''<a href="https://connect.squareup.com/oauth2/authorize?client_id={0}&scope=MERCHANT_PROFILE_READ%20SETTLEMENTS_READ%20PAYMENTS_WRITE%20PAYMENTS_READ%20ITEMS_READ%20ORDERS_READ%20TIMECARDS_READ%20ORDERS_WRITE%20PAYMENTS_WRITE_ADDITIONAL_RECIPIENTS%20EMPLOYEES_WRITE">Click here</a>
            to authorize the application.'''.format(application_id)


# @app.route('authorization')
# def authorize():
#   # return '''<a href="https://connect.squareup.com/oauth2/authorize?client_id={0}&scope=PAYMENTS_WRITE%20PAYMENTS_READ%20ITEMS_READ%20ORDERS_READ%20TIMECARDS_READ%20ORDERS_WRITE">Click here</a>
#   #           to authorize the application.'''.format(application_id)
#   return '''<a href="https://connect.squareup.com/oauth2/authorize?client_id={0}&scope=PAYMENTS_WRITE%20PAYMENTS_READ%20ITEMS_READ%20ORDERS_READ%20TIMECARDS_READ%20ORDERS_WRITE%20PAYMENTS_WRITE_ADDITIONAL_RECIPIENTS%20EMPLOYEES_WRITE">Click here</a>
#             to authorize the application.'''.format(application_id)


# Serves requsts from Square to your application's redirect URL
# Note that you need to set your application's Redirect URL to
# http://localhost:8080/callback from your application dashboard
#@get('/callback')
@app.route('/callback')
def callback():

  # Extract the returned authorization code from the URL
  #return request.args.get('code');
  authorization_code = request.args.get('code')
  if authorization_code:

    # Provide the code in a request to the Obtain Token endpoint
    oauth_request_body = {
      'client_id': application_id,
      'client_secret': application_secret,
      'code': authorization_code,
      'redirect_uri':'https://boiling-peak-36818.herokuapp.com/callback'
    }
    connection = http.client.HTTPSConnection('connect.squareup.com')
    connection.request('POST', '/oauth2/token', json.dumps(oauth_request_body), oauth_request_headers)

    # Extract the returned access token from the response body
    oauth_response_body = json.loads(connection.getresponse().read())
    if oauth_response_body['access_token']:

      # Here, instead of printing the access token, your application server should store it securely
      # and use it in subsequent requests to the Connect API on behalf of the merchant.
      #return '''<a href="tappsquare://squaretoken.com?token={0}">Click here</a>
          # to authorize the application.'''.format(application_id)
      # print 'Access token: ' + oauth_response_body['access_token']
      #return 'Authorization succeeded!'
      print( "Location: tappsquare://token.com?token=" + oauth_response_body['access_token']); 
      return oauth_response_body['access_token'];
      #print(( "Location: tappsquare://token.com?token=" + oauth_response_body['access_token']));
      #print "Location: tappsquare://token.com?token=" + {};
      

    # The response from the Obtain Token endpoint did not include an access token. Something went wrong.
    else:
      return 'Code exchange failed!'

  # The request to the Redirect URL did not include an authorization code. Something went wrong.
  else:
    return 'Authorization failed!'

# Start up the server
if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
#run(host='localhost', port=8080)