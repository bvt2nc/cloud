#!/usr/bin/env python
import os
import subprocess

from flask import Flask, render_template, request
from werkzeug import secure_filename
import sys

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.getcwd()

@app.route('/upload')
def upload_file():
	return render_template('upload.html')
	
@app.route('/uploader', methods = ['GET', 'POST'])
def save_upload_file():
	if request.method == 'POST':
		
		ret = ''		

		f = request.files['file']
		filename = secure_filename(f.filename)
		f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

		subprocess.call("rm -f ./a.out", shell=True)
		retcode = subprocess.call("/usr/bin/g++ " + app.config['UPLOAD_FOLDER'] +  "/walk.cc", shell=True)
		if retcode:
			return 'failed to compile walk.cc'

		subprocess.call("rm -f ./output", shell=True)
		
		tmpoutput = subprocess.call("echo -e freddy '\n' susan | ./a.out", shell=True)
		correct = 0
		
		output = subprocess.call("echo $tmpoutput | grep -q 'freddy'", shell=True)
		output1 = subprocess.call("echo $?", shell=True)		

		if output1 == 0:
			correct = correct + 1
		
		output = subprocess.call("echo $tmpoutput | grep -q 'susan'", shell=True)
		output1 = subprocess.call("echo $?", shell=True)		
		if output1 == 0:
			correct = correct + 1	
	
		ret = ret + "Score: " + str(correct) + " out of 2 correct. <br>"
		ret = ret + "*************Original submission************* <br>"
		with open(app.config['UPLOAD_FOLDER'] + '/walk.cc','r') as fs:
			ret = ret + fs.read() + "<br>"

#		return 'file uploaded successfully'
		return ret
		
if __name__ == '__main__':
	app.run(host="0.0.0.0", debug = True)
