from flask import Flask, render_template, request, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey


app = Flask(__name__)

app.debug = False

app.config['SECRET_KEY'] = 'porsche'

toolbar = DebugToolbarExtension(app)

responses = []

@app.route('/')
def start_survey():
    """Starting the survey"""
    return render_template('start.html', survey=satisfaction_survey)


@app.route('/questions/<int:question_id>')
def show_question(question_id):
    """Check if the question_id is valid, if not redirect to the correct URL"""
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
    responses.append(answer)

    if len(responses) == len(satisfaction_survey.questions):
        return redirect("/thankyou")
    
    else:
        return redirect(f"/questions/{len(responses)}")
    

@app.route('/thankyou')
def thank_you():
    """Basic Thank you"""
    return "Thank you"