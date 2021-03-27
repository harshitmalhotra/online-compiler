from flask import Flask,render_template,request
import subprocess,os
from subprocess import PIPE

app = Flask(__name__)

#route for the main page.
@app.route('/')
def Compiler():
	check=''
	return render_template('home.html',check=check)

app = Flask(_name_)

@app.route('/run', methods=['POST'])
def run():
    if request.method == 'POST':
        data = request.form.to_dict()
        lang = data['language']
        code = data['sourceCode']
        inp = data['customInput']
        chk = data.get('checkbox')

        if chk == 'false':
            inp = ''
            chk = '0'
            check = ''
        else:
            chk = '1'
            check = 'checked'

        if lang == 'c':
            output = c_complier_output(code, inp, chk)
        elif lang == 'cpp':
            output = cpp_complier_output(code, inp, chk)
        elif lang == 'java':
            output = java_complier_output(code, inp, chk)
        elif lang == 'python':
            output = python_complier_output(code, inp, chk)
        return output
    else:
        return render_template('index.html')

def c_complier_output(code, inp, chk):
    if not os.path.exists('main.c'):
        os.open('main.c', os.O_CREAT)
    fd = os.open("main.c", os.O_WRONLY)
    os.truncate(fd, 0)
    fileadd = str.encode(code)
    os.write(fd, fileadd)
    os.close(fd)
    s = subprocess.run(['gcc', '--sysroot=/app/.apt', 'main.c', '-lm'], stderr=PIPE, )
    check = s.returncode
    if check == 0:
        if chk == '1':
            r = subprocess.run(["./a.out"], input=inp.encode(), stdout=PIPE)
        else:
            r = subprocess.run(["./a.out"], stdout=PIPE)
        return r.stdout.decode("utf-8")
    else:
        return s.stderr.decode("utf-8")

def cpp_complier_output(code, inp, chk):
    if not os.path.exists('main.cpp'):
        os.open('main.cpp', os.O_CREAT)
    fd = os.open("main.cpp", os.O_WRONLY)
    os.truncate(fd, 0)
    fileadd = str.encode(code)
    os.write(fd, fileadd)
    os.close(fd)
    s = subprocess.run(['g++-10', '--sysroot=/app/.apt', 'main.cpp'], stderr=PIPE, )
    check = s.returncode
    if check == 0:
        if chk == '1':
            r = subprocess.run(["./a.out"], input=inp.encode(), stdout=PIPE)
        else:
            r = subprocess.run(["./a.out"], stdout=PIPE)
        return r.stdout.decode("utf-8")
    else:
        return s.stderr.decode("utf-8")

def java_complier_output(code, inp, chk):
    if not os.path.exists('Main.java'):
        os.open('Main.java', os.O_CREAT)
    fd = os.open("Main.java", os.O_WRONLY)
    os.truncate(fd, 0)
    fileadd = str.encode(code)
    os.write(fd, fileadd)
    os.close(fd)
    s = subprocess.run(['javac', 'Main.java'], stderr=PIPE, )
    check = s.returncode
    if check == 0:
        if chk == '1':
            r = subprocess.run(['java', 'Main'], input=inp.encode(), stdout=PIPE)
        else:
            r = subprocess.run(['java', 'Main'], stdout=PIPE)
        return r.stdout.decode("utf-8")
    else:
        return s.stderr.decode("utf-8")

def python_complier_output(code, inp, chk):
    if not os.path.exists('program.py'):
        os.open('program.py', os.O_CREAT)
    fd = os.open("program.py", os.O_WRONLY)
    os.truncate(fd, 0)
    fileadd = str.encode(code)
    os.write(fd, fileadd)
    os.close(fd)
    if chk == '1':
        r = subprocess.run(['python', 'program.py'], input=inp.encode(), stdout=PIPE, stderr=PIPE,)
    else:
        r = subprocess.run(['python', 'program.py'], stdout=PIPE, stderr=PIPE,)
    check = r.returncode
    if check == 0:
        return r.stdout.decode("utf-8")
    else:
        return r.stderr.decode("utf-8")

#route for the submit page to show the output/error of the c program.
@app.route('/submit',methods=['GET','POST'])
def submit():
	if request.method=='POST':

		#Getting input(code and input for program) and checkbox value from the form.
		code=request.form['code']
		inp=request.form['input']
		chk=request.form.get('check')

		#Checking if the checkbox is checked or not.
		if  not chk=='1':
			#If checkbox was not ckecked then the input field will be empty and checkbox will be unchecked. 
			inp=""
			check=''
		else:
			##If checkbox was ckecked then the input field will stay the same and checkbox will be checked.
			check='checked'	

		#calling the function to compile and execute the c program.	
		output=complier_output(code,inp,chk)
	#return render_tempelate to 	
	return render_template('home.html',code=code,input=inp,output=output,check=check)

def complier_output(code,inp,chk):
	#checking if a file already exists or not in no the create one.
	if not os.path.exists('Try.c'):
		os.open('Try.c',os.O_CREAT)
	#creating a file descriptor to write in to the file.	
	fd=os.open("Try.c",os.O_WRONLY)
	#truncate the content of the file to 0 bytes so that there is no overwriting in any way using the write operation.
	os.truncate(fd,0)
	#encode the string into bytes.
	fileadd=str.encode(code)
	#write to the file.
	os.write(fd,fileadd)
	#close the file descriptor.
	os.close(fd)
	#Compiling the c program file and retrieving the error if any. 
	s = subprocess.run(['gcc', '--sysroot=/app/.apt', 'Try.c', '-lm'], stderr=PIPE, )
	#storing the value returned by return code.
	check=s.returncode
	#checking whether program compiled succesfully or not.
	if check==0:
		#cheking whether input for program is enabled or not.
		if chk=='1':
			#executing the program with input.
			r=subprocess.run(["./a.out"],input=inp.encode(),stdout=PIPE)
		else:
			#executing the program without input.
			r=subprocess.run(["./a.out"],stdout=PIPE)
		#return the output of the program.	
		return r.stdout.decode("utf-8")
	else:
		#return the error if the program did not compile successfully
		return s.stderr.decode("utf-8")

