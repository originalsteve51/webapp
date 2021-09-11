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
    pathname = '/home/pi/mycode/webapp/feedtail.out'    
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
    pathname = '/home/pi/mycode/webapp/feedtail.out'    

    content = ''
    
    j_file = builtins.open(pathname, 'r')
    j_data = json.load(j_file)

    for key in j_data['entries'].keys():
        entry = j_data['entries'][key]
        content = content + key + '\n'
        for key_2 in entry.keys():
            content = content + f'\t{key_2}: {entry[key_2]}\n'
    print(content)
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