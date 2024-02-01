from flask import Flask, render_template, request, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey


app = Flask(__name__)

app.debug = False

app.config['SECRET_KEY'] = 'porsche'

toolbar = DebugToolbarExtension(app)

responses = []

@app.route('/', methods=['GET', 'POST'])
def start_survey():
    """Starting the survey"""
    if request.method == 'POST':
        session['responses'] = []
        return redirect('/questions/0')
    
    return render_template('start.html', survey=satisfaction_survey)


@app.route('/questions/<int:question_id>')
def show_question(question_id):
    """Check if the question_id is valid, if not redirect to the correct URL"""
    responses = session.get('responses', [])
    if question_id < len(responses):
        return redirect(f"/questions/{len(responses)}")
    
    if question_id == len(responses):
        if question_id < len(satisfaction_survey.questions):
            current_question = satisfaction_survey.questions[question_id]
            return render_template('question.html', question=current_question, question_id=question_id)
        else:
            return redirect("/thankyou")
    flash("Invalid question access. Please answer questions in order")
    return redirect(f"/questions/{len(responses)}")

@app.route('/answer', methods=["POST"])
def handle_answer():
    """Handling answer submission"""
    answer = request.form.get("answer")

    responses = session.get('responses', [])

    responses.append(answer)

    session['responses'] = responses

    if len(responses) == len(satisfaction_survey.questions):
        return redirect("/thankyou")
    
    else:
        return redirect(f"/questions/{len(responses)}")
    

@app.route('/thankyou')
def thank_you():
    """Display thank you with surevey responses"""
    survey_responses = zip(satisfaction_survey.questions, session['responses'])
    return render_template("thankyou.html", survey_responses=survey_responses)