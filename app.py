import random
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

            elif res['user_type'] == 'seller':
                session["lid"] = res['login_id']
                return redirect('/seller_home')

            elif res['user_type'] == 'user':
                session["lid"] = res['login_id']
                return redirect('/user_home')

            else:
                return '''<script>alert('invalid type');window.location="/"</script>'''
        else:
            return  '''<script>alert('invalid user name or password');window.location="/"</script>'''
    else:
        return render_template("login.html")

#####################################################################ADMIN##########################################

@app.route('/home')
def home():
    return render_template("admin/admin home.html")

@app.route('/add_employee',methods=['get','post'])
def add_employee():
    if request.method=="POST":
        db=Db()
        name = request.form['abc']
        street=request.form['str']
        locality=request.form['local']
        district=request.form['district']
        phn=request.form['ph']
        email=request.form['eml']
        db.insert(
            "insert into employee VALUE ('','" + name + "','" + street + "','" + locality + "','" + district + "','" + phn + "','" + email + "')")
        return '''<script>alert('successfull');window.location="/add_employee"</script>'''
    else:
        return render_template('admin/employee_registration.html')

@app.route('/view_employee')
def view_employee():
    db=Db()
    res=db.select("select * from employee  ")
    return render_template('admin/view_employee.html',data=res)


@app.route('/edit_employee/<e_id>',methods=['GET','POST'])
def edit_employee(e_id):
    if request.method=="POST":
        db = Db()
        name = request.form['abc']
        street = request.form['str']
        locality = request.form['local']
        district = request.form['district']
        phn = request.form['ph']
        email=request.form['eml']
        db.update("update employee set name = '" + name + "',street = '" + street + "',locality = '" + locality + "', district = '" + district + "', phone_no='" + phn + "',email='"+email+"'  where employee_id ='" +e_id + "'")

        return ''' <script> alert("Update Sucessfully");window.location = "/view_employee"  </script>'''

    else:
        db=Db()
        emp=db.selectOne("select * from employee where employee_id='"+e_id+"'")
        return render_template('admin/edit employee.html', res=emp)

@app.route('/delete_employee/<e_id>')
def delete_employee(e_id):
    db=Db()
    db.delete("delete from employee where employee_id='"+e_id+"'")
    return '''<script>alert('success');window.location="/view_employee"</script>'''



@app.route('/soil_report')
def soil_report():
        obj = Db()
        qry = "select * from soil_report,user where soil_report.user_id=user.user_id and soil_report.status='booked'"

        res = obj.select(qry)
        return render_template("admin/View Booking Master.html",res=res)

@app.route('/allocate_soil_emp/<b>')
def allocate_soil_emp(b):
    print(b)
    db=Db()
    r = db.select("select * from soil_report,allocate where soil_report.soilreport_id=allocate.request_id")
    print(r)
    if len(r) >0:
        return '''<script>alert('Already Assigned');window.location="/soil_report"</script>'''
    else:
        qry=db.select("select * from employee")
        return render_template("admin/allocation emp view.html", qry=qry,data=b)

@app.route('/assign_emp/<b>/<c>',methods=['get','post'])
def assign_emp(b,c):
    print(b)
    # r_id=request.form['textfield']
    # print(r_id)
    db=Db()
    db.insert("insert into allocate values('','"+str(c)+"','"+b+"','soil')")
    return '''<script>alert('success');window.location="/soil_report"</script>'''


    qry = "select * from soil_report,user where soil_report.user_id=user.user_id and soil_report.status='booked'"
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
        db.update("update soil_report set status = '"+path+"' where soilreport_id='" +str( b_id) + "' ")

        return '''<script>alert('report added');window.location="/home"</script>'''

        return "OK"


    else:
        return render_template("admin/Booking Master Report.html")


@app.route('/complaint')
def complaint():
    qry = "select * from complaint,user,seller where complaint.user_id=user.user_id "
    obj = Db()
    res = obj.select(qry)
    return render_template("admin/View Complaint.html",res=res)

@app.route('/seller_complaint_admin')
def seller_complaint_admin():
    qry = "select * from complaint,seller where complaint.user_id=seller.seller_id "
    obj = Db()
    res = obj.select(qry)
    return render_template("admin/View Complaint_seller.html",res=res)


@app.route('/seller_complaint_replay/<c_id>',methods=['GET','POST'])
def seller_complaint_replay(c_id):
    if request.method=="POST":
        reply=request.form['textarea']
        db = Db()
        db.update("update complaint set reply = '"+reply+"', reply_date=curdate() where compaint_id = '"+c_id+"'")
        return ''' <script> alert("Send Sucessfully");window.location = "/seller_complaint_admin"  </script>'''
    else:
        return render_template("admin/Complaint Replay.html")


@app.route('/feedback')
def feedback():
    qry = "select * from feedback,user where feedback.user_id=user.user_id"
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
    qry = "select * from product,user where product.user_id=user.user_id"
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

@app.route('/notification',methods=['GET','POST'])
def notification():
    if request.method == 'POST':
        db=Db()
        noet=request.form['textarea']
        db.insert("insert into notification VALUE('','" + noet +"',curdate(),curtime())")
        return ''' <script> alert("Send Sucessfully");window.location = "/notification"  </script>'''

    else:
        return render_template("admin/notification.html")


@app.route('/view_seller_request')
def view_seller_request():
    db=Db()
    prd=db.select("select * from seller,product_request where seller.seller_id=product_request.seller_id and status='pending'")
    return render_template("admin/view_seller_request.html",res=prd)


@app.route('/accept_seller/<s_id>')
def accept_seller(s_id):
    db=Db()
    db.update("update product_request set status='accepted' where request_id='"+s_id+"'")
    return ''' <script> alert("Accepted");window.location = "/view_seller_request"  </script>'''

@app.route('/reject_seller/<s_id>')
def reject_seller(s_id):
    db=Db()
    db.delete("delete from product_request where request_id='"+s_id+"'")
    return ''' <script> alert("Deleted");window.location = "/view_seller_request"  </script>'''



@app.route('/view_accepted_seller')
def view_accepted_seller():
    db=Db()
    res=db.select("select * from seller,product_request where seller.seller_id=product_request.seller_id and status='accepted'")
    return render_template("admin/view_accepted_seller.html",res=res)



@app.route('/allocate_emp_seller/<b>')
def allocate_emp_seller(b):
    print(b)
    db=Db()
    res = db.select("select * from product_request,allocate where product_request.request_id=allocate.request_id and type='collect'")
    print(res)
    if len(res) >0:
        return '''<script>alert('Already Assigned');window.location="/view_accepted_seller"</script>'''
    else:
        qry=db.select("select * from employee")
        return render_template("admin/allocation emp view_seller.html", qry=qry,data=b)

@app.route('/assign_emp_seller/<b>/<c>', methods=['get', 'post'])
def assign_emp_seller(b, c):
    print(b)
    # r_id=request.form['textfield']
    # print(r_id)

    db = Db()
    db.insert("insert into allocate values('','" + str(c) + "','" + b + "','collect')")
    return '''<script>alert('success');window.location="/view_accepted_seller"</script>'''


####################################################seller

@app.route('/seller_registration',methods=['GET','POST'])
def seller_registration():
    if request.method=='POST':
        name=request.form['abc']
        street=request.form['str']
        locality=request.form['local']
        district=request.form['district']
        phn=request.form['ph']
        email=request.form['eml']
        passw= request.form['pas']
        db=Db()
        db.insert("insert into seller VALUE ('','"+name+"','"+street+"','"+locality+"','"+district+"','"+phn+"','"+email+"')")
        db.insert("insert into login VALUE('','"+name+"','"+passw+"','seller')")
        return ''' <script> alert("Registered Sucessfully");window.location = "/"  </script>'''
    else:
        return render_template('seller/seller_registraction.html')


@app.route('/seller_view_profile')
def seller_view_profile():
    obj=Db()
    print(session["lid"])
    qry="select * from seller where seller_id= '"+str(session["lid"])+"'"
    res = obj.selectOne(qry)
    return render_template('seller/seller profile view.html', res=res)


@app.route('/edit_seller',methods=['GET','POST'])
def edit_seller():
    if request.method=="POST":
        db = Db()
        name = request.form['abc']
        street = request.form['str']
        locality = request.form['local']
        district = request.form['district']
        phn = request.form['ph']
        email=request.form['eml']
        db.update("update seller set name = '" + name + "',street = '" + street + "',locality = '" + locality + "', district = '" + district + "', phoneno='" + phn + "',email='"+email+"'  where seller_id ='"+str(session["lid"])+"'")
        db.update("update login set user_name='" + name + "'  where login_id ='"+str(session["lid"])+"'")
        return ''' <script> alert("Update Sucessfully");window.location = "/seller_view_profile"  </script>'''
    else:
        db=Db()
        emp=db.selectOne("select * from seller where seller_id='"+str(session["lid"])+"'")
        return render_template('seller/update seller.html', res=emp)



@app.route('/seller_home')
def center_home():
    return render_template("seller/seller home.html")


#
@app.route('/seller_complaint',methods=['GET','POST'])
def seller_complaint():
    if request.method == "POST":
        reply = request.form['textarea']
        db = Db()
        db.insert("insert into complaint VALUE('','" + reply + "', curdate(),'" + str(session["lid"]) + "','pending','pending','seller')")
        return ''' <script> alert("Send Sucessfully");window.location = "/seller_home"  </script>'''
    else:
        return render_template('seller/complaint.html')


@app.route('/seller_soil_request',methods=['GET','POST'])
def seller_soil_request():
    db=Db()
    obj=db.selectOne("select * from seller where seller_id='"+str(session["lid"])+"'")
    if request.method == 'POST':
        db=Db()
        amnt=500
        res = db.insert("insert into soil_report VALUE('', '"+str(session["lid"])+"','"+str(amnt)+"',curdate(),'pending')")
        session['soil_id']=res
        return ''' <script> alert("Send Sucessfully");window.location = "/seller_soil_payment"  </script>'''
    else:
        return render_template("seller/sent soil request seller.html",res=obj)


@app.route('/seller_soil_payment',methods=['GET','POST'])
def seller_soil_payment():

    if request.method == 'POST':
        db = Db()
        acc = request.form['abc']
        # car = request.form['efg']
        # mon = request.form['ijk']
        # yr = request.form['lmn']
        # cvv = request.form['hjk']
        res=db.selectOne("select * from payment WHERE account_no='"+acc+"' and user_id='"+str(session["lid"])+"'")
        amount1 = int(res['amount'])
        if res is not None:
            if amount1 >500:
                db.update("update soil_report set status='booked' where soilreport_id='" + str(session['soil_id']) + "' ")
                db.update("update payment set amount='"+str(amount1-500)+"' where user_id='" + str(session["lid"]) + "' and account_no='"+acc+"' ")
                db.update("update payment set amount=amount+500 where user_id=1  ")
                return ''' <script> alert("Booked Successfully");window.location = "/seller_home"  </script>'''
            else:
                return ''' <script> alert("insufficient Balance");window.location = "/soil_payment"  </script>'''
        else:
            return ''' <script> alert("Enter Correct Account Number");window.location = "/soil_payment"  </script>'''
        # et = db.selectOne("select amount from payment WHERE user_id='" + str(session["lid"]) + "'")
        # print(ed,et,acc)
        # if ed==str(acc):
        #     if et>=500:
        #         db.update("update soil_report set status='booked' where user_id='" + str(session["lid"]) + "' ")
        #         db.update("update payment set amount=amount-500 where user_id='" + str(session["lid"]) + "'")
        #         return ''' <script> alert("Send Sucessfully");window.location = "/"  </script>'''
        #     else:
        #         return ''' <script> alert("insufficient Balance");window.location = "/soil_payment"  </script>'''
        # else:
        #     return ''' <script> alert("Enter Correct Account Number");window.location = "/soil_payment"  </script>'''


    else:
        return render_template("seller/seller soil payment.html" )



#@app.route('/view_soil_booking')
# def view_soil_booking():
#         qry = "select * from soil_report where user_id='"+str(session["lid"])+"';"
#         obj = Db()
#         res = obj.select(qry)
#         return render_template("user/view soil report.html", res=res)



@app.route('/view_soil_report_seller')
def view_soil_report_seller():
    qry=select("select * from soil_report where ")



@app.route('/add_product')
def add_product():
    qry = "select * from ,user where query.user_id=user.user_id;"
#     obj = Db()
#     res = obj.select(qry)
#     return render_template("seller/Query view.html",res=res)
#
# @app.route('/query_reply/<Q_id>',methods=['GET','POST'])
# def query_reply(Q_id):
#     if request.method=="POST":
#         reply=request.form['textarea']
#         db = Db()
#         db.update("update query set reply = '"+reply+"', reply_date=curdate() where q_id = '"+Q_id+"'")
#         return ''' <script> alert("Send Sucessfully");window.location = "/query"  </script>'''
#     else:
#         return render_template("seller/Query reply.html")
#
#
#
# @app.route('/view_center_bookings')
# def view_center_bookings():
#     qry = "select * from delvery,seller where delvery.statuse='pending' AND seller.locality=delvery.locality AND seller.c_id='"+str(session["lid"])+"'"
#     obj = Db()
#
#     res = obj.select(qry)
#     print(res)
#     return render_template("seller/view booking.html", res=res)


#@app.route('/qu_reply/<Q_id>',methods=['GET','POST'])
#def query_reply(Q_id):
    #return render_template("seller/Query reply.html")

# @app.route('/center_update/<c_id>',methods=['GET','POST'])
# def center_update(c_id):
#     db = Db()
#     qry = "select * from seller where c_id=c_id"
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
        # db.update("update seller set c_name = '" + name + "',street = '"+street+"',locality = '"+locality+"', district = '"+district+"', phone_no='"+phn+"',email='"+email+"'  where c_id ='"+c_id+"'")
        # db.update("update login set user_name='" + name + "',password='"+passw+"' where login_id='"+c_id+"'")
        # return ''' <script> alert("Send Sucessfully");window.location = "/center_view/<c_id>"  </script>'''
    # else:
    #
    #     return render_template('seller/update_'
    #                            seller.html',res=res)


# @app.route('/view_booking_center'/<u_id>',methods=['GET','POST'])
# def view_booking_center(u_id):
#     db = Db()
#     qry = "select * from booking,seller,user where booking.street =seller.street"
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
#         return render_template('seller/update_center.html',res=res)




#############################################USER##################################

@app.route('/user_home')
def user_home():
    return render_template("user/user_home.html")




@app.route('/add_user',methods=['get','post'])
def add_user():
    if request.method=="POST":
        db=Db()
        name=request.form['textfield2']
        photo=request.files['fileField']
        date=datetime.datetime.now().strftime("%y%m%d-%H%M%S")
        photo.save=(r"C:\flaskProject5\static\images/"+date+'.jpg')
        path=("static/images/"+date+'.jpg')
        gender=request.form['radio']
        street=request.form['textfield3']
        Locality=request.form['textfield4']
        district=request.form['district']
        phoneno=request.form['textfield5']
        email=request.form['textfield6']
        password=request.form['textfield7']
        confirmpassword=request.form['textfield8']
        db.insert("insert into login values ('','"+email+"','"+str(confirmpassword)+"','user')")
        db.insert ("insert into user values ('','"+name+"','"+street+"','"+phoneno+"','"+gender+"','"+Locality+"','"+district+"','"+str(path)+"','"+email+"')")
        return '''<script>alert('register successfull');window.location="/user_home"</script>'''
    else:
        return render_template('user/user_registration.html')


@app.route('/user_view_profile')
def user_view_profile():
    obj=Db()
    print(session["lid"])
    res = obj.selectOne("select * from user where user_id= '"+str(session["lid"])+"'")
    print(res)
    return render_template('user/user profile view.html', res=res)



@app.route('/user_update/<c_id>',methods=['GET','POST'])
def center_update(c_id):
    db = Db()
    qry = "select * from user where user_id='"+str(session["lid"])+"'"
    res=db.selectOne(qry)
    if request.method=='POST':
       db=Db()
       name=request.form['abc']
       street=request.form['str']
       locality=request.form['local']
       district=request.form['district']
       phn=request.form['ph']
       # email=request.form['eml']
       passw= request.form['pas']
       db.update("update user set user_name = '" + name + "',street = '"+street+"',locality = '"+locality+"', district = '"+district+"', phone_number='"+phn+"'  where user_id ='"+str(session['lid'])+"'")
       db.update("update login set user_name='" + name + "',password='"+passw+"' where login_id='"+str(session["lid"])+"'")
       return ''' <script> alert("Send Sucessfully");window.location = "/center_view/<c_id>"  </script>'''
    else:
         return render_template('user/update user.html',res=res)


# @app.route('/insert/<u_id>',methods=['GET','POST'])
# def update_user(u_id):
#      db = Db()
#      qry = "select * from booking,seller,user where booking.street =seller.street"
#      res=db.select(qry)
#      if request.method=='POST':
#          db=Db()
#          noet=request.form['textarea']
#
#          db.insert("insert into notification VALUE('','"+noet+"','" + u_id + "',curdate(),datetime.now())")
#          return ''' <script> alert("Send Sucessfully");window.location = "/center_view/<c_id>"  </script>'''#
#      else:
#
#         return render_template('seller/update_center.html',res=res)

@app.route('/cart')
def cart():
    return render_template("user/cart view.html")


@app.route('/user_feedback',methods=['GET','POST'])
def user_feedback():
    if request.method == 'POST':
        db=Db()
        noet=request.form['textarea']
        db.insert("insert into feedback VALUE('','" + noet +"', '"+str(session["lid"])+"',curdate(),curtime())")
        return ''' <script> alert("Send Sucessfully");window.location = "/user_feedback"  </script>'''

    else:
        return render_template("user/feedback.html")@app.route('/user_feedback',methods=['GET','POST'])
def user_feedback():
    if request.method == 'POST':
        db=Db()
        noet=request.form['textarea']
        db.insert("insert into feedback VALUE('','" + noet +"', '"+str(session["lid"])+"',curdate(),curtime())")
        return ''' <script> alert("Send Sucessfully");window.location = "/center_view/<c_id>"  </script>'''
    else:
        return render_template("user/feedback.html")


# @app.route('/user_feedback',methods=['GET','POST'])
# def user_feedback():
#     if request.method == 'POST':
#         db=Db()
#         noet=request.form['textarea']
#         db.insert("insert into feedback VALUE('','" + noet +"', '"+str(session["lid"])+"',curdate(),curtime())")
#         return ''' <script> alert("Send Sucessfully");window.location = "/center_view/<c_id>"  </script>'''
#     else:
#         return render_template("user/feedback.html")


@app.route('/soil_request',methods=['GET','POST'])
def soil_request():
    db=Db()
    obj=db.selectOne("select * from user where user_id='"+str(session["lid"])+"'")
    if request.method == 'POST':
        db=Db()


        name = request.form['abc']
        street = request.form['def']
        locality = request.form['jkl']
        phn= request.form['mno']

        amnt=500
        res = db.insert("insert into soil_report VALUE('', '"+str(session["lid"])+"','"+str(amnt)+"',curdate(),'pending')")
        session['soil_id']=res
        return ''' <script> alert("Send Sucessfully");window.location = "/soil_payment"  </script>'''
    else:
        return render_template("user/sent soil report.html",res=obj)

@app.route('/view_booking')
def view_booking():
    db=Db()
    obj=db.selectOne("select * from delvery where user_id='"+str(session["lid"])+"'")

    return render_template("user/view booking.html", res=obj)



@app.route('/soil_payment',methods=['GET','POST'])
def soil_payment():


    if request.method == 'POST':
        db = Db()
        acc = request.form['abc']
        # car = request.form['efg']
        # mon = request.form['ijk']
        # yr = request.form['lmn']
        # cvv = request.form['hjk']
        res=db.selectOne("select * from payment WHERE account_no='"+acc+"' and user_id='"+str(session["lid"])+"'")
        amount1 = int(res['amount'])
        if res is not None:
            if amount1 >=500:
                db.update("update soil_report set status='booked' where soilreport_id='" + str(session['soil_id']) + "' ")
                db.update("update payment set amount='"+str(amount1-500)+"' where user_id='" + str(session["lid"]) + "' and account_no='"+acc+"' ")
                return ''' <script> alert("Booked Successfully");window.location = "/soil_payment"  </script>'''
            else:
                return ''' <script> alert("insufficient Balance");window.location = "/soil_payment"  </script>'''

        else:
            return ''' <script> alert("Enter Correct Account Number");window.location = "/soil_payment"  </script>'''
        # et = db.selectOne("select amount from payment WHERE user_id='" + str(session["lid"]) + "'")
        # print(ed,et,acc)
        # if ed==str(acc):
        #     if et>=500:
        #         db.update("update soil_report set status='booked' where user_id='" + str(session["lid"]) + "' ")
        #         db.update("update payment set amount=amount-500 where user_id='" + str(session["lid"]) + "'")
        #         return ''' <script> alert("Send Sucessfully");window.location = "/"  </script>'''
        #     else:
        #         return ''' <script> alert("insufficient Balance");window.location = "/soil_payment"  </script>'''
        # else:
        #     return ''' <script> alert("Enter Correct Account Number");window.location = "/soil_payment"  </script>'''


    else:
        return render_template("user/soil payment.html" )



@app.route('/view_soil_booking')
def view_soil_booking():
        qry = "select * from soil_report where user_id='"+str(session["lid"])+"';"
        obj = Db()
        res = obj.select(qry)
        return render_template("user/view soil report.html", res=res)


@app.route('/user_complaint')
def user_complaint():
    if request.method == 'POST':
        db=Db()
        noet=request.form['textarea']
        db.insert("insert into complaint VALUE('','" + noet +"', '"+str(session["lid"])+"',curdate(),curtime())")
        return ''' <script> alert("Send Sucessfully");window.location = "/center_view/<c_id>"  </script>'''
    else:
        return render_template("user/feedback.html")

if __name__ == '__main__':
    app.run()
