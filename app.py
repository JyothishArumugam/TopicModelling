from flask import Flask, render_template,request,jsonify
import subprocess
import json
import generate_response

app=Flask(__name__)

@app.route('/send', methods=['GET','POST'])
def send():
	if request.method=='POST':
		search_term=request.form['age']
		print(search_term)
		subprocess.call(['bash','process1.sh',search_term])
		response=generate_response.responseGen(search_term)
		#response=dummy.setter(search_term)
		subprocess.call(['bash','process2.sh',search_term])
		#return json.dumps(response)
		##json_string=json.dumps(response)
		##print(type(json.loads(json_string)))
		##return jsonify(response)
		##return render_template('ldaplots.html',graph=json.loads(json_string))
		##return render_template('testplot.html',output=jsonify(response))
		##return render_template('age.html',age=response)
		return render_template('ldatest.html',jsondata=response)
	return render_template('index.html')

if __name__=="__main__":
	app.run()
