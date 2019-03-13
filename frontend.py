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
    yrs = fsh.getYears()
    return render_template('coachArea.html', teams=tms, years=yrs)

@app.route('/fanArea')
def fanArea():
    tms = fsh.getTeams()
    conf = fsh.getConf()
    div = fsh.getDivs()
    yrs = fsh.getYears()
    return render_template('fanArea.html', teams=tms, divs=div, confs=conf, years=yrs)

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
    questions = dict(request.form)
    ans = fsh.answerFanPlayerQuestions(questions)
    return render_template('fanPlayerAnswers.html', answers=ans)

@app.route('/fanTeamQuestions', methods=['POST'])
def fanTeamQuestions():
    questions = dict(request.form)
    splitTeam = questions['selectTeam'].split(',')
    questions['selectTeam'] = splitTeam[0]
    ans = fsh.answerFanTeamQuestions(questions)
    ans['team'] = splitTeam[1]
    return render_template('fanTeamAnswers.html', answers=ans)