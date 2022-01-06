from flask import Flask,render_template,request
from DBConnection import Db
import datetime

app = Flask(__name__)

syspath=r"C:\Users\akhil\PycharmProject\flaskProject5\static\kisan\\"

@app.route('/',methods=['GET','POST'])
def login():
    if request.method=="POST":
        uname=request.form['username']
        password=request.form['password']

        db = Db()
        res = db.selectOne("select * from login where user_name = '"+uname+"' and password = '"+password+"' ")
        print(res)

        if res is not None:
            if res['user_type'] == 'admin':
                return render_template('admin/admin home.html')
            elif res['user_type'] == 'center':
                return render_template('center/center_home.html')
            elif res['user_type'] == 'user':
                return render_template('center/center_home.html')

            else:
                return "invalid user type"
        else:
            return "user not found"






    else:
        return render_template("login.html")



@app.route('/view_approved_center')
def view_approved_center():
    qry = "select *from center"
    obj = Db()
    res = obj.select(qry)
    return render_template("admin/Approve Center.html",res=res)

@app.route('/approved_center_view')
def approved_center_view():
    qry = "select *from center"
    obj = Db()
    res = obj.select(qry)
    return render_template("admin/Approved Center View.html",res=res)

@app.route('/booking_master')
def booking_master():
    qry = "select * from booking_master,user where booking_master.user_id=user.user_id;"
    obj = Db()
    res = obj.select(qry)
    return render_template("admin/View Booking Master.html",res=res)

@app.route('/booking_master_report/<b_id>',methods=['GET','POST'])
def booking_master_report(b_id):
    if request.method=="POST":
        rprt=request.files['fileField']
        d=datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        rprt.save(syspath+d+'.pdf')
        path='/static/kisan/'+d+'.pdf'
        db = Db()
        db.update("update booking_master set report = '"+path+"' where master_id='" +str( b_id) + "' ")
        return "OK"

    else:
        return render_template("admin/Booking Master Report.html")

@app.route('/complaint')
def complaint():
    qry = "select * from complaint,user where complaint.user_id=user.user_id;"
    obj = Db()
    res = obj.select(qry)
    return render_template("admin/View Complaint.html",res=res)

@app.route('/complaint_replay/<c_id>',methods=['GET','POST'])
def complaint_replay(c_id):
    if request.method=="POST":
        reply=request.form['textarea']
        db = Db()
        db.update("update complaint set reply = '"+reply+"', reply_date=curdate() where compaint_id = '"+c_id+"'")
        return ''' <script> alert("Send Sucessfully");window.location = "/complaint"  </script>'''
    else:
        return render_template("admin/Complaint Replay.html")

@app.route('/feedback')
def feedback():
    qry = "select *from feedback"
    obj = Db()
    res = obj.select(qry)
    return render_template("admin/View feedback.html",res=res)

@app.route('/rating')
def rating():
    qry = "SELECT rating.user_id ,rating.rating,user.user_name FROM rating INNER JOIN user ON rating.user_id=user.user_id;"
    obj = Db()
    res = obj.select(qry)
    print(res)
    return render_template("admin/view _rating.html",data=res)

@app.route('/product')
def product():
    qry = "select * from product"
    obj = Db()
    res = obj.select(qry)
    return render_template("admin/View Product.html",res=res)

@app.route('/booking')
def booking():
    qry = " select * from booking,product,user where booking.product_id=product.product_id and booking.user_id=user.user_id;"
    obj = Db()
    res = obj.select(qry)
    return render_template("admin/View BOOKING.HTML",res=res)

@app.route('/payment')
def payment():
    qry = "select * from user,payment where user.user_id=payment.user_id; "
    obj = Db()
    res = obj.select(qry)
    return render_template("admin/View Payment.html",res=res)

@app.route('/user')
def user():
    qry= "select *from user"
    obj=Db()
    res=obj.select(qry)
    return render_template("admin/View User.html", res=res)

@app.route('/home')
def home():
    return render_template("admin/admin home.html")



@app.route('/approve_center/<center_id>')
def approve_center(center_id):
    db = Db()
    db.update("update login set user_type = 'center' where login_id='"+center_id+"' ")
    return "OK"
    # return render_template("admin/admin home.html")
@app.route('/reject_center/<center_id>')
def reject_center(center_id):
    db = Db()
    db.delete("DELETE FROM center where center_id ='"+center_id+"' ")
    return "OK"



if __name__ == '__main__':
    app.run()
