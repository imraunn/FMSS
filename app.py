from flask import Flask, request, render_template, redirect
# from flask_session import Session

import simulation

import json


users=json.load(open('users.bak'))
isLoggedIn=False
role=None

app = Flask(__name__)
# app.config["SESSION_PERMANENT"] = False
# app.config["SESSION_TYPE"] = "filesystem"
# Session(app)


machines=[]
@app.route('/', methods=['GET','POST'])
def index():
    global isLoggedIn
    global role
    if request.method=='GET':
        return render_template('index.html', alert=None)
    elif request.method=='POST':
        username=request.form.get('username')
        password=request.form.get('password')
        
        for user in users:
            if user["username"]==username and user["password"]==password:
                isLoggedIn=True
                role=user["role"]
                if role=="head":
                    return redirect("/dashboard")
                else:
                    return redirect("/machine")
        return render_template('index.html', alert="Wrong username or password")

machines=[]
machineNames=[]
@app.route('/machine', methods=['GET','POST'])
def machine():
    global isLoggedIn
    if isLoggedIn==False:
        return redirect("/")
    global machines
    print(machines)
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
    global isLoggedIn
    if isLoggedIn==False:
        return redirect("/")
    global adjusters
    global machineNames
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
    global isLoggedIn
    if isLoggedIn==False:
        return redirect("/")
    # global adjusters
    # global machines
    if request.method=='POST':
        numberOfYears=int(request.form.get('numberOfYears'))
        statistics=simulation.simulate(adjusters,machines,numberOfYears)
        return render_template('simulation.html', statistics=statistics)

@app.route('/deleteadjuster', methods=['POST'])
def deleteadjuster():
    global isLoggedIn
    if isLoggedIn==False:
        return redirect("/")
    global adjusters
    if request.method=='POST':
        type=request.form.get('type')
        for adjuster in adjusters:
            if adjuster["adjusterType"]==type:
                adjusters.remove(adjuster)
                break
    return redirect("/adjuster")

@app.route('/deletemachine', methods=['POST'])
def deletemachine():
    global isLoggedIn
    if isLoggedIn==False:
        return redirect("/")
    global machines
    if request.method=='POST':
        name=request.form.get('name')
        for machine in machines:
            if machine["machineName"]==name:
                machines.remove(machine)
                break
    return redirect("/machine")

@app.route('/logout',methods=['GET'])
def logout():
    global isLoggedIn
    isLoggedIn=False
    role=None
    return redirect("/")

@app.route('/dashboard',methods=['GET'])
def dashboard():
    global isLoggedIn
    global role
    if isLoggedIn==False:
        return redirect("/")
    if role!="head":
        return redirect("/")
    global machines
    global adjusters
    global machineNames

    flag=1
    if len(machines)>0 and len(adjusters)>0:
        flag=0
    return render_template('dashboard.html', machinesNames=machineNames, adjusters=adjusters, machines=machines, show=flag) 
