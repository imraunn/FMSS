from flask import Flask, request, render_template
import simulation
app = Flask(__name__)


machines=[]
@app.route('/', methods=['GET','POST'])
def index():
    return render_template('index.html')

machines=[]
machineNames=[]
@app.route('/machine', methods=['GET','POST'])
def machine():
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
    global adjusters
    global machineNames
    print(adjusters)
    # print(machineNames)
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
    # global adjusters
    # global machines
    if request.method=='POST':
        numberOfYears=int(request.form.get('numberOfYears'))
        statistics=simulation.simulate(adjusters,machines,numberOfYears)
        return render_template('simulation.html', statistics=statistics)
