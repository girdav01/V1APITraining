# Web hook simulator using Flask. We added an authentication token to make this demo a little more safer
# to test just like this with your verification token  http://192.168.1.52:5000/webhook?verify_token=73822aee4a3ec56d2659c92024c644da48e6cb9258d6a93f
# change your ip that the end of the script
# you may prefer to run in VS Code as admin instead of pyCharm
import os
from flask import Flask, request, abort, jsonify

def temp_token():
    import binascii
    temp_token = binascii.hexlify(os.urandom(24))
    return temp_token.decode('utf-8')

WEBHOOK_VERIFY_TOKEN = os.getenv('WEBHOOK_VERIFY_TOKEN')

app = Flask(__name__)

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    print(WEBHOOK_VERIFY_TOKEN)
    # GET is only provided to make a quick test using a browser
    if request.method == 'GET':
        verify_token = request.args.get('verify_token')
        if verify_token == WEBHOOK_VERIFY_TOKEN:
            return jsonify({'status':'success'}), 200
        else:
            return jsonify({'status':'bad token'}), 401

    elif request.method == 'POST':  # this is the web simulator
        client = request.remote_addr
        print(client)
        verify_token = request.args.get('verify_token')
        if verify_token == WEBHOOK_VERIFY_TOKEN:
            print(request.json)
            return jsonify({'status':'success'}), 200
        else:
            return jsonify({'status':'bad token'}), 401
    else:
        abort(400)

if __name__ == '__main__':
    print(WEBHOOK_VERIFY_TOKEN)
    if WEBHOOK_VERIFY_TOKEN is None:
        print('WEBHOOK_VERIFY_TOKEN has not been set in the environment.\nGenerating random token...')
        token = temp_token()
        print('Token: %s' % token)
        WEBHOOK_VERIFY_TOKEN = token
    else:
        print(WEBHOOK_VERIFY_TOKEN)
    # change your ip
    app.run(host='192.168.1.52')