from flask import Flask,jsonify

app=Flask(__name__)

@app.route('/',methods=['GET'])

def output():
    return jsonify({"Name":"Kundan","Id":125})

if __name__== "__main__":
    app.run(debug=True)
