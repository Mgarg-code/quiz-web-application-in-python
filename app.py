from flask import Flask,request,render_template,session,redirect,jsonify
from datetime import timedelta
import random 
import json 

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

correct_questions = []
attempted_questions = []

with open('question_bank.db') as f : 
        data = json.load(f)
        f.close() 
questions =[ 
        { 'question': d, 'options': data[d][0],'answer':data[d][1] } for d in data 
        ]
random.shuffle(questions)
#questions = questions[:50]

total_ques = len(questions)


@app.route('/')
def index():
    if 'username' in session and 'ques' in session :
            return render_template('quiz.html',name=session['username'],course=session['course'])
    global correct_questions,attempted_questions
    correct_questions = []
    attempted_questions = []

    return render_template('index.html')
    
@app.route('/startquiz/',methods=['GET','POST'])
def startquiz():
    if request.method == 'POST' : 
        fname = request.form['fname']
        lname = request.form['lname']
        email = request.form['email']
        course = request.form['course']
        session['username'] = fname.capitalize()+" "+lname.capitalize()
        session['course'] = course.upper()
        session['ques'] = 0
        return render_template('quiz.html',name=session['username'],course=session['course'])
    #return "Invalid Form Method We Only Accept POST Methods"
    elif 'username' in session :#and 'ques' in session :
            return render_template('quiz.html',name=session['username'],course=session['course'])
    else : 
        return redirect("/", code=302)


@app.route('/logout/')
def logout():
    session.pop('username',None)
    session.pop('course',None)
    #session.pop('ques',None)
    return redirect("/", code=302)


@app.route('/question/<int:ques>')
def question(ques=None):
    if ques < len(questions):
        session['ques'] = ques 
        new_ques = { 'question': questions[ques]['question'],'options':questions[ques]['options'],'total_questions':total_ques}
        return jsonify(new_ques)
    else : 
        return jsonify(None)


@app.route('/check_question/',methods=['POST','GET'])
def check():
    ques = request.form['ques']
    ans = request.form['answer']
    print(ques,ans)
    if int(ques) not in attempted_questions : 
        attempted_questions.append(int(ques))
    if str(questions[int(ques)]['answer']).strip().lower() == str(ans).strip().lower() :
        if int(ques) not in correct_questions : 
                correct_questions.append(int(ques))
        return jsonify({'data':True,'correct':correct_questions,'attempted':attempted_questions})
    else : 
        if int(ques) in correct_questions : 
                correct_questions.remove(int(ques))
        return jsonify({'data': False, 'correct': correct_questions, 'attempted': attempted_questions})


if __name__ == "__main__": 
    #app.run(debug=True)
    app.run('localhost',5000,debug=True)
