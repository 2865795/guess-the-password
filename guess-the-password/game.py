from flask import Flask, render_template, request
import random


app = Flask(__name__)


number = list(range(10))
code = random.sample(number, 4)

counters = [0, 0, 0, 0]
result = []
move_counter = 6


def check_code(list_answer):
    new_list = []
    n = 0
    global move_counter
    move_counter-=1
    for i in list_answer:
        if i in code:
            if i == code[n]:
                new_list.append({"class": "green", "value": i})
            else:
                new_list.append({"class": "orange", "value": i})
        else:
            new_list.append({"class": "red", "value": i})
        n += 1
    result.append(new_list)
    return result, move_counter


def reset():
    global counters
    counters = [0, 0, 0, 0]
    global result
    result = []
    global move_counter
    move_counter = 6
    return counters, result, move_counter


@app.route('/', methods=['POST', 'GET'])
def index():
    return render_template('index.html')

@app.route('/start', methods=['POST', 'GET'])
def start():
    if request.method == 'POST':
        reset()
        return render_template('start.html',answer=result, counters=counters, move=move_counter)


@app.route('/increment/<int:counter_id>')
def increment(counter_id):
    counters[counter_id] = (counters[counter_id] + 1) % 10
    return render_template('start.html',answer=result, counters=counters, move=move_counter)


@app.route('/decrement/<int:counter_id>')
def decrement(counter_id):
    counters[counter_id] = (counters[counter_id] - 1) % 10
    return render_template('start.html',answer=result, counters=counters, move=move_counter)


@app.route('/result', methods=['POST', 'GET'])
def result_user():
    if request.method == 'POST':
        if move_counter>=2:
            if code!=counters:
                check_code(counters)
                return render_template('start.html', answer=result, counters=counters, move=move_counter)
            else:
                return render_template('win.html')
        else:
            if code==counters:
                return render_template('win.html')
            else:
                return render_template('over.html')

app.run(debug=True)

