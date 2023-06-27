from flask import Flask, render_template, request, redirect, url_for, session
import db, string, random
from datetime import timedelta

app = Flask(__name__)
app.secret_key = ''.join(random.choices(string.ascii_letters, k=256))


@app.route('/', methods=['GET'])
def top():
    msg = request.args.get('msg')
    
    if msg == None:
        return render_template('index.html')
    else:
        return render_template('index.html', msg=msg)
    
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    user_name = request.form.get('username')
    email = request.form.get('email')
    address = request.form.get('address')
    password = request.form.get('password')
    
    if db.login(user_name, email, address, password):
        session['user'] = True
        session.permanent = True
        app.permanent_session_lifetime = timedelta(minutes=30)
        return redirect(url_for('mypage'))
    else:
        error = 'ログインに失敗しました。'
        
        input_data = {'user_name':user_name}
        return render_template('login.html', error=error, data=input_data)
    
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login.html'))

@app.route('/mypage', methods=['GET'])
def mypage():
    if 'user' in session:
        return render_template('mypage.html')
    else:
        return redirect(url_for('index'))
    
@app.route('/register')
def register_form():
    return render_template('register.html')

@app.route('/register_exe', methods=['POST'])
def register_exe():
    user_name = request.form.get('user_name')
    email = request.form.get('email')
    address = request.form.get('address')
    password = request.form.get('password')
    
    if user_name == '':
        error = 'ユーザー名が入力されてません。'
        return render_template('register.html', error=error)
    if password == '':
        error = 'パスワードが入力されてません。'
        return render_template('register.html', error=error)
    
    count = db.insert_user(user_name, email, address, password)
    
    if count == 1:
        msg = '登録が完了しました。'
        return redirect(url_for('index.html', msg=msg))
    else:
        error = '登録に失敗しました。'
        return render_template('register.html', error=error)
           
@app.route('/history')
def history():
    return render_template('history.html')

@app.route('/basket')
def basket():
    return render_template('basket.html')







if __name__ == '__main__':
    app.run(debug=True)