from flask import Flask, request, render_template, redirect, session
import json

import simulation

users=json.load(open('users.bak'))

app = Flask(__name__)
app.secret_key = 'BAD_SECRET_KEY'


@app.route('/', methods=['GET','POST'])
def index():
    if request.method=='GET':
        return render_template('index.html', alert=None)
    elif request.method=='POST':
        username=request.form.get('username')
        password=request.form.get('password')
        
        for user in users:
            if user["username"]==username and user["password"]==password:
                session["isLoggedIn"]=True
                session["role"]=user["role"]
                if session["role"]=="head":
                    return redirect("/dashboard")
                else:
                    return redirect("/machine")
        return render_template('index.html', alert="Wrong username or password")

machines=[]
machineNames=[]
@app.route('/machine', methods=['GET','POST'])
def machine():
    global machines
    if session["isLoggedIn"]==False:
        return redirect("/")
    if request.method=='GET':
        return render_template('machine.html', machines=machines)
    elif request.method=='POST':
        machineName=request.form.get('machineName')
        MTTF=request.form.get('MTTF')
        repairTime=request.form.get('repairTime')
        quantity=request.form.get('quantity')

        machine={}
        machine["machineName"]=machineName
        machine["MTTF"]=int(MTTF)
        machine["repairTime"]=int(repairTime)
        machine["quantity"]=int(quantity)
        machineNames.append(machineName)
        machines.append(machine)
        return render_template('machine.html', machines=machines)

adjusters=[]
@app.route('/adjuster', methods=['GET','POST'])
def adjuster():
    global adjusters
    global machineNames
    if session["isLoggedIn"]==False:
        return redirect("/")
    if request.method=='GET':
        return render_template('adjuster.html', machinesNames=machineNames, adjusters=adjusters)
    elif request.method=='POST':
        adjusterType=request.form.get('adjusterType')
        expertise=request.form.getlist('expertise')
        numberOfAdjusters=request.form.get('numberOfAdjusters')

        adjuster={}
        adjuster["adjusterType"]=adjusterType
        adjuster["expertise"]=expertise
        adjuster["numberOfAdjusters"]=int(numberOfAdjusters)

        adjusters.append(adjuster)
        return render_template('adjuster.html', machinesNames=machineNames, adjusters=adjusters)

@app.route('/simulate', methods=['POST'])
def simulate():
    if session["isLoggedIn"]==False:
        return redirect("/")

    if request.method=='POST':
        numberOfYears=int(request.form.get('numberOfYears'))
        statistics=simulation.simulate(adjusters,machines,numberOfYears)
        return render_template('simulation.html', statistics=statistics)

@app.route('/deleteadjuster', methods=['POST'])
def deleteadjuster():
    global adjusters
    if session["isLoggedIn"]==False:
        return redirect("/")
    if request.method=='POST':
        type=request.form.get('type')
        for adjuster in adjusters:
            if adjuster["adjusterType"]==type:
                adjusters.remove(adjuster)
                break
    if session["role"]=="head":
        return redirect("/dashboard")
    else:
        return redirect("/adjuster")

@app.route('/deletemachine', methods=['POST'])
def deletemachine():
    global machines
    if session["isLoggedIn"]==False:
        return redirect("/")

    if request.method=='POST':
        name=request.form.get('name')
        for machine in machines:
            if machine["machineName"]==name:
                machines.remove(machine)
                break
        for machinename in machineNames:
            if machinename==name:
                machineNames.remove(name)
                break
    if session["role"]=="head":
        return redirect("/dashboard")
    else:
        return redirect("/machine")

@app.route('/logout',methods=['GET'])
def logout():
    session["isLoggedIn"]=False
    session["role"]=None
    return redirect("/")

@app.route('/dashboard',methods=['GET'])
def dashboard():
    global machines
    global adjusters
    global machineNames
    if session["isLoggedIn"]==False:
        return redirect("/")
    if session["role"]!="head":
        return redirect("/")
    flag=1
    if len(machines)>0 and len(adjusters)>0:
        flag=0
    return render_template('dashboard.html', machinesNames=machineNames, adjusters=adjusters, machines=machines, show=flag) 
