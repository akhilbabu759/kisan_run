from flask import Flask, render_template, request, redirect, session
from DBConnection import Db
import datetime

app = Flask(__name__)
app.secret_key = "abc"

syspath=r"C:\Users\akhil\PycharmProject\flaskProject5\static\kisan\\"

@app.route('/',methods=['GET','POST'])
def login():
    if request.method=="POST":
        uname=request.form['username']
        password=request.form['password']

        db = Db()
        res = db.selectOne("select * from login where user_name = '"+uname+"' and password = '"+password+"' ")


        if res is not None:
            if res['user_type'] == 'admin':
                return redirect('/home')

            elif res['user_type'] == 'center':
                session["lid"] = res['login_id']
                return redirect('/center_home')

            # elif res['user_type'] == 'user':
            #     return render_template('center/center_home.html')

            else:
                return "invalid user type"
        else:
            return "user not found"






    else:
        return render_template("login.html")



@app.route('/view_approved_center')
def view_approved_center():
    qry = "select *from center where status='pending'"
    obj = Db()
    res = obj.select(qry)
    return render_template("admin/Approve Center.html", res=res)

@app.route('/approved_center_view')########################################
def approved_center_view():
    qry = "select *from center where status='approved'"
    obj = Db()
    res = obj.select(qry)
    return render_template("admin/Approved Center View.html",res=res)

@app.route('/soil_report')
def soil_report():
    qry = "select * from soil_report,user where soil_report.user_id=user.user_id;"
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
        db.update("update soil_report set report = '"+path+"' where soilreport_id='" +str( b_id) + "' ")
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
    qry = " select * from booking_master,user where  booking_master.user_id=user.user_id and booking_master.status='booked'"
    obj = Db()
    res = obj.select(qry)
    return render_template("admin/View BOOKING.HTML",res=res)

@app.route('/view_booked_products/<mid>')
def view_booked_products(mid):
    qry = " select  booking.*,product.*,booking.quantity*product.price as sum from booking,product where  booking.product_id=product.product_id and booking.master_id='"+mid+"'"
    obj = Db()
    res = obj.select(qry)
    return render_template("admin/View booked products.HTML",res=res)

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
    ##db.update("update center set status = 'center' where c_id='"+center_id+"' ")
    db.update("update center set status = 'approved' where c_id='" + center_id + "' ")

    return 'ok'
    # return render_template("admin/admin home.html")
@app.route('/reject_center/<center_id>')
def reject_center(center_id):
    db = Db()
    db.delete("DELETE FROM center where c_id ='"+center_id+"' ")
    return "OK"

##CENTER


@app.route('/center_registration',methods=['GET','POST'])
def center_registration():
    if request.method=='POST':
        name=request.form['abc']
        street=request.form['str']
        locality=request.form['local']
        district=request.form['district']
        phn=request.form['ph']
        email=request.form['eml']
        passw= request.form['pas']
        db=Db()
        pen="pending"
        ce="center"
        db.insert("insert into center VALUE ('','"+name+"','"+street+"','"+locality+"','"+district+"','"+phn+"','"+email+"','"+pen+"')")
        db.insert("insert into login VALUE('','"+name+"','"+passw+"','"+ce+"')")
        return ''' <script> alert("Send Sucessfully");window.location = "/"  </script>'''


    else:
        return render_template('center/center_registraction.html')


@app.route('/center_view_profile')
def center_view_profile():
    obj=Db()
    print(session["lid"])
    qry="select * from center where c_id= '"+str(session["lid"])+"'"
    res = obj.selectOne(qry)
    return render_template('center/center profile view.html', res=res)



@app.route('/center_home')
def center_home():
    return render_template("center/center home.html")



@app.route('/notification')#####################################################
def notification():
    if request.method == "POST":
        reply = request.form['textarea']
        db = Db()
        db.update(
            "update complaint set reply = '" + reply + "', reply_date=curdate() where compaint_id = '" + c_id + "'")
        return ''' <script> alert("Send Sucessfully");window.location = "/complaint"  </script>'''
    else:
        return render_template('center/notification.html')



@app.route('/query')
def query():
    qry = "select * from query,user where query.user_id=user.user_id;"
    obj = Db()
    res = obj.select(qry)
    return render_template("center/Query view.html",res=res)

@app.route('/query_reply/<Q_id>',methods=['GET','POST'])
def query_reply(Q_id):

    if request.method=="POST":
        reply=request.form['textarea']
        db = Db()
        db.update("update query set reply = '"+reply+"', reply_date=curdate() where q_id = '"+Q_id+"'")
        return ''' <script> alert("Send Sucessfully");window.location = "/query"  </script>'''
    else:
        return render_template("center/Query reply.html")

@app.route('/view_center_bookings')
def view_center_bookings():
    qry = "select * from query,user where query.user_id=user.user_id;"
    obj = Db()
    res = obj.select(qry)
    return render_template("center/Query view.html", res=res)


#@app.route('/qu_reply/<Q_id>',methods=['GET','POST'])
#def query_reply(Q_id):
    #return render_template("center/Query reply.html")

# @app.route('/center_update/<c_id>',methods=['GET','POST'])
# def center_update(c_id):
#     db = Db()
#     qry = "select * from center where c_id=c_id"
#     res=db.selectOne(qry)
#     if request.method=='POST':
#         db=Db()
#         name=request.form['abc']
#         street=request.form['str']
#         locality=request.form['local']
#         district=request.form['district']
# +       phn=request.form['ph']
        # email=request.form['eml']
        # passw= request.form['pas']
        # db=Db()
        # db.update("update center set c_name = '" + name + "',street = '"+street+"',locality = '"+locality+"', district = '"+district+"', phone_no='"+phn+"',email='"+email+"'  where c_id ='"+c_id+"'")
        # db.update("update login set user_name='" + name + "',password='"+passw+"' where login_id='"+c_id+"'")
        # return ''' <script> alert("Send Sucessfully");window.location = "/center_view/<c_id>"  </script>'''
    # else:
    #
    #     return render_template('center/update_'
    #                            center.html',res=res)


# @app.route('/view_booking_center'/<u_id>',methods=['GET','POST'])
# def view_booking_center(u_id):
#     db = Db()
#     qry = "select * from booking,center,user where booking.street =center.street"
#     res=db.select(qry)
#     if request.method=='POST':
#         db=Db()
#         noet=request.form['textarea']
#
#         db.insert("insert into notification VALUE('','"+noet+"','" + u_id + "','"+curdate()+"','" + curtime()+ "')")
#         return ''' <script> alert("Send Sucessfully");window.location = "/center_view/<c_id>"  </script>'''
#
#
#     else:
#
#         return render_template('center/update_center.html',res=res)

if __name__ == '__main__':
    app.run()
