from flask import Flask, render_template, request, redirect

app=Flask(__name__)

# temporary in-memory list to store tasks
tasks= []

@app.route("/")
def home():
    # this renders the HTML page and passes current tasks to it
    return render_template('index.html', tasks = tasks)

@app.route('/add',methods=['POST'])
def addTask():
    head=request.form.get('head')
    body=request.form.get('body')

    # store it in list (temporary, will later connect to DB)
    if head and body:
        tasks.append({"head":head,"body":body})
        
    return redirect('/')


if __name__=="__main__":
    app.run(debug=True)