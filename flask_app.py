from flask import Flask, url_for, render_template, make_response, request
import mqtt_pub
import urllib
import os.path, time

import datetime
import json
import builtins

app = Flask(__name__)
mqtt_client = mqtt_pub.run()

@app.route("/")
def main():
    now = datetime.datetime.now()
    timeString = now.strftime("%Y-%m-%d %H:%M")
    templateData = {
      'title' : 'Cat Station',
      'time': timeString
      }
    response = make_response(render_template('main.html', **templateData))
    return response
    
@app.route('/feedcw/', methods=["POST"])
def feedcw():
    global mqtt_client
    if request.method == "POST":
        mqtt_pub.publish_one(mqtt_client, '/python/stepper', 'pan-left')
        return 'ok'

@app.route('/light/', methods=["POST"])
def light():
    global mqtt_client
    if request.method == "POST":
        mqtt_pub.publish_one(mqtt_client, '/python/stepper', 'pan-home')
        return 'ok'

@app.route('/feedccw/', methods=["POST"])
def feedccw():
    global mqtt_client
    if request.method == "POST":
        mqtt_pub.publish_one(mqtt_client, '/python/stepper', 'pan-right')
        return 'ok'
        
@app.route('/open', methods=['GET', 'POST'])
def open():
    pathname = '/home/pi/mycode/webapp/status.json'    
    modtime = time.ctime(os.path.getmtime(pathname))
    createtime = time.ctime(os.path.getctime(pathname))
    
    file = urllib.request.urlopen('file://'+pathname)
    content = file.read()
    now = datetime.datetime.now()
    timeString = now.strftime("%Y-%m-%d %H:%M")
    templateData = {
      'title' : 'Feeder Status',
      'time': timeString,
      'content': content.decode('utf8'),
      'modtime': modtime,
      'createtime': createtime
      }
    response = make_response(render_template('feeder.html', **templateData))
    return response

@app.route('/json_status', methods=['GET', 'POST'])
def json_status():
    pathname = '/home/pi/mycode/webapp/status.json'    

    content = '<tbody>'
    
    j_file = builtins.open(pathname, 'r')
    j_data = json.load(j_file)

    # Since we run on Python 3.7.3, dicts preserve order. This
    # means we can reverse the order that the keys are used
    # by first making a list of the keys and using the
    # builtin reversed function. 
    # Reverse order presents the most recent data at the top
    # of the list, which is what I want.
    # Also, limit the size of this table to 100 rows.
    count = 0
    for key in reversed( list(j_data['entries'].keys() ) ):
        count += 1
        if count > 100:
            break
        content = content + '<tr>'
        entry = j_data['entries'][key]
        content = content + '<th scope="row">'+key+'</th>'
        
        start_weight = entry.get('start_weight')
        stable_weight = entry.get('stable_weight')
        amt_dispensed = float(stable_weight) - float(start_weight)
        amt_dispensed_fmt = format(amt_dispensed, '.3f')
        content = content + f'<td>{amt_dispensed_fmt}</td>'
        details = entry.get('details')
        pulse_count = len(details)
        if pulse_count == 0:
            amt_per_pulse_fmt = 'N/A'
        else:
            amt_per_pulse = amt_dispensed/pulse_count
            amt_per_pulse_fmt = format(amt_per_pulse, '.3f')
        content = content + f'<td>{amt_per_pulse_fmt}</td>'
        content = f'{content}</tr>'
    
    content = f'{content}</tbody>'

    now = datetime.datetime.now()
    timeString = now.strftime("%Y-%m-%d %H:%M")
    templateData = {
      'title' : 'Recent Feeder Status',
      'time': timeString,
      'content' : content
      }

    response = make_response(render_template('recent_status.html', **templateData))
    return response


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8082, debug=True)