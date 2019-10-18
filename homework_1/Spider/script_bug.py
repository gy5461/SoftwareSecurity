from flask import Flask, request, render_template_string, render_template, redirect
import pymysql
localRes = ['']
app = Flask(__name__)
@app.route('/')
def login():
    if request.args.get('username') and request.args.get('password'):
        username = request.args.get('username')
        password = request.args.get('password')

        db = pymysql.connect('localhost', 'root', '584034912', 'NetShop')
        cursor = db.cursor()
        try:
            sql = "select password from user where name ='%s'" % username
            cursor.execute(sql)
            password_in_db = cursor.fetchone()

            if(password == password_in_db[0]):
                return redirect('/commodities')
            else:
                return render_template('404.html')
        except:
            return render_template('404.html')

    return render_template("login.html")

@app.route('/commodities')
def commodities():
    db = pymysql.connect('localhost', 'root', '584034912', 'NetShop')
    cursor = db.cursor()
    try:
        sql = "select * from commodity"
        cursor.execute(sql)
        res = cursor.fetchall()

    except:
        print('error')

    return render_template("commodities.html", res=res)

@app.route('/<commodity_id>/reviews')
def review(commodity_id):
    db = pymysql.connect('localhost', 'root', '584034912', 'NetShop')
    cursor = db.cursor()
    res = localRes[0]
    try:
        sql = "select * from review where commodity_id = %d" % int(commodity_id)
        cursor.execute(sql)
        res = cursor.fetchall()
        print(res)
        res = list(res)
        for index in range(len(res)):
            res[index] = list(res[index])
            user_id = res[index][1]
            sql = "select name from user where id = %d" % int(user_id)
            cursor.execute(sql)
            user_name = cursor.fetchone()
            res[index][1] = user_name[0]

        localRes[0]=res
    except:
        print('error')
    script = "javascript:alert('unsafe!!!');"
    if request.args.get('script'):
        script = request.args.get(
            'script') + 'document.write(\'<div id=\"back\"><a href=\"http://127.0.0.1:5000/commodity_id/reviews\"><button type=\"button\">回到评论区</button></a></div>\')'
    return render_template('review.html', script=script, res=res)
if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, debug=True)