app = Flask(__name__)

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
        return render_template('{{ output }}')

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
