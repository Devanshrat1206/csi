from flask import Flask, render_template, request, redirect, url_for
import uuid
app = Flask(__name__)
quizzes = {}
@app.route('/')
def index():
    return render_template('quiz.html')
@app.route('/create', methods=['POST'])
def create_quiz():
    quiz_title = request.form['quiz-title']
    questions = []
    question_num = 1
    while f'question{question_num}' in request.form:
        question = request.form[f'question{question_num}']
        choices = [request.form[f'choices{choice}{question_num}'] for choice in ['A', 'B', 'C', 'D']]
        questions.append({'question': question, 'choices': choices})
        question_num += 1
    quiz_id = str(uuid.uuid4())
    quizzes[quiz_id] = {'title': quiz_title, 'questions': questions}
    return redirect(url_for('quiz_link', quiz_id=quiz_id))
@app.route('/quiz/<quiz_id>')
def quiz_link(quiz_id):
    return f'To take the quiz,use this link:<a href="/take/{quiz_id}">/take/{quiz_id}</a>'
@app.route('/take/<quiz_id>', methods=['GET', 'POST'])
def take_quiz(quiz_id):
    if request.method == 'GET':
        if quiz_id in quizzes:
            return render_template('takequiz.html', quiz_id=quiz_id, quiz=quizzes[quiz_id])
        else:
            return 'Quiz not found!'
    elif request.method == 'POST':
        return 'Quiz submitted!'
if __name__ == '__main__':
    app.run(debug=True)