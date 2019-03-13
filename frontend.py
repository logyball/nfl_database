from flask import Flask, render_template, request
from os import environ
import frontend_sql_helpers as fsh

# setup
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/coachArea')
def coachArea():
    tms = fsh.getTeams()
    return render_template('coachArea.html', teams=tms)

@app.route('/fanArea')
def fanArea():
    tms = fsh.getTeams()
    return render_template('fanArea.html', teams=tms)

@app.route('/coachQuestions', methods=['POST'])
def coachQuestions():
    questions = dict(request.form)
    splitTeam = questions['selectTeam'].split(',')
    questions['selectTeam'] = splitTeam[0]
    ans = fsh.answerCoachQuestions(questions)
    ans['team'] = splitTeam[1]
    return render_template('coachAnswers.html', answers=ans)

@app.route('/fanPlayerQuestions', methods=['POST'])
def fanPlayerQuestions():
    return "not yet implemented"

@app.route('/fanTeamQuestions', methods=['POST'])
def fanTeamQuestions():
    return "not yet implemented"