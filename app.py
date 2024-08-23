from flask import Flask,render_template,request
import sqlite3
import pickle

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/contact',methods = ["GET","POST"])
def contactus():
    if request.method=="POST":
        fname = request.form.get("name")
        pno = request.form.get("phone")
        email = request.form.get("email")
        addr = request.form.get("address")
        msg = request.form.get("message")
        conn = sqlite3.connect('ytdatabase.db')
        cur=conn.cursor()
        cur.execute(f'''
                    INSERT INTO CONTACT VALUES("{fname}","{pno}","{email}","{addr}","{msg}")
                    ''')
        conn.commit()
        return render_template('message.html')
    else:
        return render_template('contactus.html')
    
@app.route("/analytics")
def analytics():
    return render_template("analytics.html")

@app.route("/predictor",methods = ['GET','POST'])
def predict():
    if request.method=='POST':
        views=request.form.get('views')
        dislikes=request.form.get('dislikes')
        comments=request.form.get('comments')
        genre=request.form.get('genre')
        with open("model_pickle",'rb')as mod:
            model=pickle.load(mod)
        pred = model.predict([[float(views),float(dislikes),float(comments),float(genre)]])
        return render_template('result.html',pred=str(round(pred[0])))
    else:
        return render_template("likepredict.html")
        



if __name__=='__main__':
    app.run()


