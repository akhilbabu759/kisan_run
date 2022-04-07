import random
from flask import Flask, render_template, request, redirect, session
from DBConnection import Db
import datetime

app = Flask(__name__)
app.secret_key = "abc"

syspath=r"C:\Users\akhil\Downloads\flaskProject5\static\kisan\\"



#########################################################################

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
    return render_template("admin_side/admin home.html")

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
        bname = request.form['textfield']
        acno=request.form['textfield2']
        ifsc=request.form['textfield3']
        amount=request.form['textfield4']
        res=db.insert("insert into employee VALUE ('','" + name + "','" + street + "','" + locality + "','" + district + "','" + phn + "','" + email + "')")
        db.insert("insert into bank VALUES ('','"+str(res)+"','"+acno+"','"+ifsc+"','"+amount+"','employee')")
        return '''<script>alert('successfull');window.location="/home"</script>'''
    else:
        return render_template('admin_side/employee_registration.html')




@app.route('/view_employee')
def view_employee():
    db=Db()
    res=db.select("select * from employee  ")
    return render_template('admin_side/view_employee.html',data=res)




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
        return render_template('admin_side/edit employee.html', res=emp)

@app.route('/delete_employee/<e_id>')
def delete_employee(e_id):
    db=Db()
    db.delete("delete from employee where employee_id='"+e_id+"'")
    return redirect('/view_employee')

@app.route('/view_soil_request',methods=['get','post'])
def view_soil_request():
    if request.method=="POST":
        db=Db()
        mtype=request.form['mtype']
        if mtype=="seller":
            obj = Db()
            qry = obj.select("select * from soil_report,seller where soil_report.user_id=seller.seller_id ")
            ss = obj.selectOne("select * from allocate,employee where employee.employee_id=allocate.employee_id and allocate.status='pending'")
            print(ss)

            return render_template("admin_side/View_seller_requests.html", res=qry, data=ss)
        else:
            obj = Db()
            qry = obj.select("select * from soil_report,user where soil_report.user_id=user.user_id ")
            ss = obj.selectOne("select * from allocate,employee where employee.employee_id=allocate.employee_id and allocate.status='pending' ")
            print(ss)
            return render_template("admin_side/View Booking Master.html", res=qry, data=ss)
    else:

           return render_template('admin_side/view_soil_request.html')

@app.route('/soil_report')
def soil_report():
        obj = Db()
        qry = obj.select("select * from soil_report,seller where soil_report.user_id=seller.seller_id ")
        ss=obj.selectOne("select * from allocate,employee where employee.employee_id=allocate.employee_id and allocate.status='pending'")
        print(ss)

        return render_template("admin_side/View_seller_requests.html",res=qry,data=ss)


@app.route('/soil_report_user')
def soil_report_user():
        obj = Db()
        qry = "select * from soil_report,user where soil_report.user_id=user.user_id "
        ss = obj.selectOne("select * from allocate,employee where employee.employee_id=allocate.employee_id and allocate.status='pending' ")
        print(ss)

        res = obj.select(qry)
        return render_template("admin_side/View Booking Master.html",res=res,data=ss)

@app.route('/allocate_soil_emp/<b>')
def allocate_soil_emp(b):
    db=Db()

    r = db.select("select * from soil_report,allocate where soil_report.soilreport_id=allocate.request_id and request_id='"+b+"' ")
    if len(r) >0:
        return '''<script>alert('Already assigned');window.location="/soil_report"</script>'''
    else:

        qry=db.select("select * from employee")
        return render_template("admin_side/allocation emp view.html", qry=qry,data=b)

@app.route('/allocate_soil_emp_user/<b>')
def allocate_soil_emp_user(b):
    db=Db()

    r = db.select("select * from soil_report,allocate where soil_report.soilreport_id=allocate.request_id and request_id='"+b+"' ")
    if len(r) >0:
        return '''<script>alert('Already assigned');window.location="/soil_report_user"</script>'''
    else:

        qry=db.select("select * from employee")
        return render_template("admin_side/allocation emp view.html", qry=qry,data=b)



@app.route('/assign_emp/<b>/<c>',methods=['get','post'])
def assign_emp(b,c):
    print(b)
    db=Db()
    ss = db.select("select * from allocate,employee where allocate.employee_id=employee.employee_id and status='pending' and allocate.employee_id='"+str(b)+"'")
    print(ss)
    if len(ss)>0:
        return '''<script>alert('Employee on work');window.location="/soil_report"</script>'''
    else:
        db.insert("insert into allocate values('','"+str(c)+"','"+b+"','soil','pending',curdate())")
        return '''<script>alert('success');window.location="/soil_report"</script>'''

@app.route('/view_allocated_emp/<b>')
def view_allocated_emp(b):
    db=Db()
    ss=db.select("select * from allocate,employee where allocate.employee_id=employee.employee_id  and request_id='"+b+"'")
    return render_template('admin_side/view_employee_allocated.html',data=ss)

@app.route('/allocated_employees')
def allocated_employees():
    db=Db()
    ss=db.select("select allocate.employee_id as id,employee.*,allocate.* from employee,allocate where employee.employee_id=allocate.employee_id and status='pending'")
    return render_template('admin_side/allocated_employee.html',data=ss)

@app.route('/update_status/<b>')
def update_status(b):
    db=Db()
    db.update("update allocate set status='free' where employee_id='"+b+"'")
    return redirect('/allocated_employees')



@app.route('/send_payment_emp/<b>/<r>',methods=['get','post'])
def send_payment_emp(b,r):
    if request.method=="POST":
        db = Db()
        acc = request.form['abc']
        ifsc = request.form['efg']
        res = db.selectOne( "select * from bank WHERE account_no='" + acc + "' and ifsc='" + ifsc + "' and person_id='" + str(b) + "'")
        print(b,r)
        amount1 = int(res['amount'])
        if res is not None:

                db.update("update allocate set status='paid' where request_id='" +r+ "' and employee_id='"+b+"' ")
                db.update("update bank set amount='" + str(amount1 + 200) + "' where person_id='" + b + "' and account_no='" + acc + "' ")
                db.update("update bank set amount=amount-200 where type='admin'  ")
                return ''' <script> alert("payment updated Successfully");window.location = "/home"  </script>'''

        else:
            return ''' <script> alert("Enter Correct Account Number");window.location = "/send_payment_emp/<b>/<c>"  </script>'''

    return render_template('admin_side/update_payment.html')



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
    else:
        return render_template("admin_side/Booking Master Report.html")


@app.route('/view_payment_details',methods=['get','post'])
def view_payment_details():
    if request.method=="POST":
        db=Db()
        mtype=request.form['mtype']
        mnth=request.form['month']
        yr=request.form['person']
        print(yr)

        if mtype=='seller' :

            ss = db.select("select * from seller,product where status='accepted' and  month(`date`)='" + mnth + "' and product.seller_id=seller.seller_id")
            s = db.select("select sum(Quantity * seller_price) as total,product.*,seller.* from product,seller where status='accepted' and month(`date`)='" + mnth + "' and year(`date`)='"+ yr +"' and product.seller_id=seller.seller_id")
            print(ss)
            if len(ss)>0:
                for i in s:

                    a=float(i['Quantity'])
                    print(a*i['seller_price'])
                    p=a*i['seller_price']
                    ab=int(p)
                return render_template('admin_side/View Payment.html',data=ss,a=s)
            else:
                return redirect('/view_payment_details')
        # elif mtype=='user':

        else:
            user = db.select("select * from employee,allocate where employee.employee_id=allocate.employee_id and month(`date`)='" + mnth + "' and year(`date`)='"+yr+"'")
            print(user)
            # s = db.select("select sum(Quantity * seller_price) as total,product.*,seller.* from product,seller where status='accepted' and month(`date`)='" + mnth + "' and product.seller_id=seller.seller_id")
            # print(ss)
            return render_template('admin_side/View Payment.html', data1=user)
    else:
        db=Db()

        return render_template('admin_side/View Payment.html')

@app.route('/send_payment_employee')
def send_payment_employee():
    db=Db()
    p=db.select("select * from employee")
    if len(p)>0:
        for i in p:
            print(i['employee_id'])
            q=db.selectOne("select count(employee_id) as c from allocate where employee_id='"+str(i['employee_id'])+"' ")
            a1=q['c']
            if a1>0:
                ss=db.update("update bank set amount=amount+200 where type='employee' and person_id='"+str(i['employee_id'])+"'")
                db.update("update bank set amount=amount-200 where type='admin'")
        # return '''<script>alert('payment updated');window.location="/send_payment_employee"</script>'''
        return "<script>alert('ok');window.location='/home'</script>"

    else:
        return redirect('/view_payment_details')


@app.route('/send_payment_seller/<b>/<pr>')
def send_payment_seller(b,pr):
    db = Db()
    ss=db.selectOne("select * from seller,product where seller.seller_id=product.seller_id and product.seller_id='"+b+"' and product.status='accepted' and Product_id='"+pr+"'")
    print(ss)
    if len(ss)>0:
        p=float(ss['Quantity'])
        a=p*ss['seller_price']
        print(p,ss['seller_price'])
        # a=sum(p,ss['seller_price'])
        print(a)
        db.update("update bank set amount=amount+'"+str(a)+"' where person_id='"+b+"' and type='seller'")
        db.update("update bank set amount=amount-'"+str(a)+"' where type='admin'")
        return '''<script>alert('payment updated');window.location="/view_payment_details"</script>'''
    return redirect('/view_payment_details')
    # p = db.select("select * from seller")
    # if len(p) > 0:
    #     for i in p:
    #         print(i['seller_id'])
    #         q = db.selectOne("select count(seller_id) as c from allocate where employee_id='" + str(i['employee_id']) + "'")
    #         a1 = q['c']
    #         if a1 > 0:
    #             ss = db.update("update bank set amount=amount+200 where type='employee' and person_id='" + str(i['employee_id']) + "'")
    #             db.update("update bank set amount=amount-200 where type='admin'")
    #     # return '''<script>alert('payment updated');window.location="/send_payment_employee"</script>'''
    #     return "<script>alert('ok');window.location='/home'</script>"


@app.route('/view_booking_user')
def view_booking_user():
    db=Db()
    ss=db.select("select * from booking_master,user,product,booking where booking_master.user_id=user.user_id and booking_master.status='booked' and booking_master.master_id=booking.master_id and product.Product_id=booking.product_id")
    return render_template('admin_side/view booking_user.html',data=ss)


@app.route('/allocate_product_emp_user/<b>')
def allocate_product_emp_user(b):
    db=Db()

    r = db.select("select * from product,allocate where product.Product_id=allocate.request_id and request_id='"+b+"' ")
    if len(r) >0:
        return '''<script>alert('Already assigned');window.location="/view_booking_user"</script>'''
    else:

        qry=db.select("select * from employee")
        return render_template("admin_side/allocation emp view_product.html", qry=qry,data=b)


@app.route('/assign_emp_product/<b>/<c>',methods=['get','post'])
def assign_emp_product(b,c):
    print(b)
    db=Db()
    ss = db.select("select * from allocate,employee where allocate.employee_id=employee.employee_id and status='pending' and allocate.employee_id='"+str(b)+"'")
    print(ss)
    if len(ss)>0:
        return '''<script>alert('Employee on work');window.location="/view_booking_user"</script>'''
    else:
        db.insert("insert into allocate values('','"+str(c)+"','"+b+"','product','pending',curdate())")
        return '''<script>alert('success');window.location="/view_booking_user"</script>'''

@app.route('/view_complaint_admin',methods=['get','post'])
def view_complaint_admin():
    if request.method=="POST":
        mtype=request.form['mtype']
        if mtype=="seller":
            qry = "select * from complaint,seller where complaint.user_id=seller.seller_id "
            obj = Db()
            res = obj.select(qry)
            return render_template("admin_side/View Complaint_seller.html", res=res)
        else:
            qry = "select * from complaint,user,seller where complaint.user_id=user.user_id "
            obj = Db()
            res = obj.select(qry)
            return render_template("admin_side/View Complaint.html", res=res)



    else:
        return render_template('admin_side/view_complaint.html')

@app.route('/complaint')
def complaint():
    qry = "select * from complaint,user,seller where complaint.user_id=user.user_id "
    obj = Db()
    res = obj.select(qry)
    return render_template("admin_side/View Complaint.html",res=res)

@app.route('/seller_complaint_admin')
def seller_complaint_admin():
    qry = "select * from complaint,seller where complaint.user_id=seller.seller_id "
    obj = Db()
    res = obj.select(qry)
    return render_template("admin_side/View Complaint_seller.html",res=res)


@app.route('/seller_complaint_replay/<c_id>',methods=['GET','POST'])
def seller_complaint_replay(c_id):
    if request.method=="POST":
        reply=request.form['textarea']
        db = Db()
        db.update("update complaint set reply = '"+reply+"', reply_date=curdate() where compaint_id = '"+c_id+"'")
        return ''' <script> alert("Send Sucessfully");window.location = "/complaint"  </script>'''
    else:
        return render_template("admin_side/Complaint Replay.html")


@app.route('/user_complaint_replay/<c_id>',methods=['GET','POST'])
def user_complaint_replay(c_id):
    if request.method=="POST":
        reply=request.form['textarea']
        db = Db()
        db.update("update complaint set reply = '"+reply+"', reply_date=curdate() where compaint_id = '"+c_id+"'")
        return ''' <script> alert("Send Sucessfully");window.location = "/user_complaint_admin"  </script>'''
    else:
        return render_template("admin_side/Complaint Replay.html")


@app.route('/feedback')
def feedback():
    qry = "select * from feedback,user where feedback.user_id=user.user_id"
    obj = Db()
    res = obj.select(qry)
    return render_template("admin_side/View feedback.html",res=res)



@app.route('/rating')
def rating():
    qry = "SELECT rating.user_id ,rating.rating,user.user_name FROM rating INNER JOIN user ON rating.user_id=user.user_id;"
    obj = Db()
    res = obj.select(qry)
    print(res)
    return render_template("admin_side/view _rating.html",data=res)

@app.route('/product')
def product():
    qry = "select * from product,seller where product.seller_id=seller.seller_id"
    obj = Db()
    res = obj.select(qry)
    return render_template("admin_side/View Product.html",res=res)

@app.route('/accept_product/<b>')
def accept_product(b):
    db=Db()
    ss=db.update("update product set status='accepted' where Product_id='"+b+"'")
    return redirect('/product')

@app.route('/delete_product/<b>')
def delete_product(b):
    db=Db()
    ss=db.delete("delete from  product where Product_id='"+b+"'")
    return redirect('/product')

@app.route('/add_admin_price/<b>',methods=['get','post'])
def add_admin_price(b):
    if request.method=="POST":
        price=request.form['t1']
        print("kjhvc")
        db=Db()
        db.update("update product set admin_price='"+price+"' where Product_id='"+b+"'")
        return redirect('/product')
    else:
        db=Db()
        ss=db.selectOne("select * from product where Product_id='"+b+"'")
        return render_template('admin_side/add_admin_price.html',data=ss)

@app.route('/update_admin_price/<b>',methods=['get','post'])
def update_admin_price(b):
    if request.method=="POST":
        price=request.form['t1']
        db=Db()
        db.update("update product set admin_price='"+price+"' where Product_id='"+b+"'")
        return redirect('/product')
    else:
        db=Db()
        ss=db.selectOne("select * from product where Product_id='"+b+"'")
        return render_template('admin_side/update_admin_price.html',data=ss)



@app.route('/booking')
def booking():
    qry = " select * from booking_master,user where  booking_master.user_id=user.user_id and booking_master.status='booked'"
    obj = Db()
    res = obj.select(qry)
    return render_template("admin_side/View BOOKING.HTML",res=res)


@app.route('/view_booked_products/<mid>')
def view_booked_products(mid):
    qry = " select  booking.*,product.*,booking.quantity*product.price as sum from booking,product where  booking.product_id=product.product_id and booking.master_id='"+mid+"'"
    obj = Db()
    res = obj.select(qry)
    return render_template("admin_side/View booked products.HTML",res=res)


@app.route('/payment')
def payment():
    qry = "select * from user,payment where user.user_id=payment.user_id; "
    obj = Db()
    res = obj.select(qry)
    return render_template("admin_side/View Payment.html",res=res)


@app.route('/user')
def user():
    qry= "select *from user"
    obj=Db()
    res=obj.select(qry)
    return render_template("admin_side/View User.html", res=res)

@app.route('/notification',methods=['GET','POST'])
def notification():
    if request.method == 'POST':
        db=Db()
        noet=request.form['textarea']
        db.insert("insert into notification VALUE('','" + noet +"',curdate(),curtime())")
        return ''' <script> alert("Send Sucessfully");window.location = "/notification"  </script>'''

    else:
        return render_template("admin_side/notification.html")


@app.route('/view_seller_request')
def view_seller_request():
    db=Db()
    prd=db.select("select * from seller,product where seller.seller_id=product.seller_id and status='pending'")
    return render_template("admin_side/view_seller_request.html",res=prd)


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
    res=db.select("select * from seller,product where seller.seller_id=product.seller_id and status='accepted'")
    return render_template("admin_side/view_accepted_seller.html",res=res)




#######################################################################seller_side


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
        res=db.insert("insert into login VALUE('','"+email+"','"+passw+"','seller')")
        db.insert("insert into seller VALUE ('"+str(res)+"','"+name+"','"+street+"','"+locality+"','"+district+"','"+phn+"','"+email+"')")

        return ''' <script> alert("Registered Sucessfully");window.location = "/"  </script>'''
    else:
        return render_template('seller_side/seller_registraction.html')


@app.route('/seller_view_profile')
def seller_view_profile():
    obj=Db()
    print(session["lid"])
    qry="select * from seller where seller_id= '"+str(session["lid"])+"'"
    res = obj.selectOne(qry)
    return render_template('seller_side/seller profile view.html', res=res)


@app.route('/edit_seller',methods=['GET','POST'])
def edit_seller():
    if request.method=="POST":
        db = Db()
        name = request.form['abc']
        street = request.form['str']
        locality = request.form['local']
        district = request.form['district']
        phn = request.form['ph']

        db.update("update seller set name = '" + name + "',street = '" + street + "',locality = '" + locality + "', district = '" + district + "', phoneno='" + phn + "'  where seller_id ='"+str(session["lid"])+"'")
        # db.update("update login set user_name='" + name + "'  where login_id ='"+str(session["lid"])+"'")
        return ''' <script> alert("Update Sucessfully");window.location = "/seller_view_profile"  </script>'''
    else:
        db=Db()
        emp=db.selectOne("select * from seller where seller_id='"+str(session["lid"])+"'")
        return render_template('seller_side/update seller.html', res=emp)



@app.route('/seller_home')
def center_home():
    return render_template("seller_side/seller home.html")


#
@app.route('/seller_complaint',methods=['GET','POST'])
def seller_complaint():
    if request.method == "POST":
        reply = request.form['textarea']
        db = Db()
        db.insert("insert into complaint VALUES ('','" + reply + "', curdate(),'" + str(session["lid"]) + "','pending','pending','seller')")
        return ''' <script> alert("Send Sucessfully");window.location = "/seller_home"  </script>'''
    else:
        db=Db()
        return render_template('seller_side/complaint.html')

@app.route('/view_reply')
def view_reply():
    db=Db()
    ss=db.select("select * from complaint where user_id='"+str(session['lid'])+"'")
    return render_template('seller_side/View_reply.html',data=ss)


@app.route('/seller_soil_request',methods=['GET','POST'])
def seller_soil_request():
    db=Db()
    obj=db.selectOne("select * from seller where seller_id='"+str(session["lid"])+"'")
    print(obj)
    if request.method == 'POST':
        db=Db()
        amnt=500
        res = db.insert("insert into soil_report VALUE('', '"+str(session["lid"])+"','"+str(amnt)+"',curdate(),'pending')")
        session['soil_id']=res
        return ''' <script> alert("Send Sucessfully");window.location = "/seller_soil_payment"  </script>'''
    else:
        return render_template("seller_side/sent soil request seller.html",res=obj)


@app.route('/seller_soil_payment',methods=['GET','POST'])
def seller_soil_payment():

    if request.method == 'POST':
        db = Db()
        acc = request.form['abc']
        ifsc = request.form['efg']
        # car = request.form['efg']
        # mon = request.form['ijk']
        # yr = request.form['lmn']
        # cvv = request.form['hjk']
        print(str(session['soil_id']))
        res=db.selectOne("select * from bank WHERE account_no='"+acc+"' and ifsc='"+ifsc+"' and person_id='"+str(session["lid"])+"'")

        if res is not None:
            amount1 = int(res['amount'])
            if amount1 >500:
                db.update("update soil_report set status='booked' where soilreport_id='" + str(session['soil_id']) + "' ")
                db.update("update bank set amount='"+str(amount1-500)+"' where person_id='" + str(session["lid"]) + "' and account_no='"+acc+"' ")
                db.update("update bank set amount=amount+500 where type='admin'  ")
                return ''' <script> alert("Booked Successfully");window.location = "/seller_home"  </script>'''
            else:
                return ''' <script> alert("insufficient Balance");window.location = "/seller_soil_payment"  </script>'''
        else:
            return ''' <script> alert("Enter Correct Account Number");window.location = "/seller_soil_payment"  </script>'''
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
        return render_template("seller_side/seller soil payment.html" )



#@app.route('/view_soil_booking')
# def view_soil_booking():
#         qry = "select * from soil_report where user_id='"+str(session["lid"])+"';"
#         obj = Db()
#         res = obj.select(qry)
#         return render_template("user/view soil report.html", res=res)


#
@app.route('/view_soil_report_seller')
def view_soil_report_seller():
    db=Db()
    qry=db.select("select * from soil_report where user_id='"+str(session['lid'])+"'")
    return render_template('seller_side/View Booking_status.html',res=qry)



@app.route('/cancel_booking/<b>')
def cancel_booking(b):
    db=Db()
    db.delete("delete from soil_report where soilreport_id='"+b+"'")
    return '''<script>alert('booking cancelled');window.location="/view_soil_report_seller"</script>'''



@app.route('/add_product',methods=['get','post'])
def add_product():
    if request.method=="POST":
        pname=request.form['textfield']
        quantity=request.form['textfield2']
        details=request.form['textfield3']
        price=request.form['textfield4']
        db=Db()
        db.insert("insert into product VALUES ('','"+str(session['lid'])+"','"+pname+"','"+quantity+"','"+details+"','"+price+"',0,curdate(),'pending')")
        return '''<script>alert('product added');window.location="/seller_home"</script>'''
    else:
        return render_template('seller_side/add_product.html')

@app.route('/view_product')
def view_product():
    db=Db()
    ss=db.select("select * from product where seller_id='"+str(session['lid'])+"'")
    return render_template('seller_side/view_product.html',data=ss)

@app.route('/update_product/<b>',methods=['get','post'])
def update_product(b):
    if request.method=="POST":
        pname = request.form['textfield']
        quantity = request.form['textfield2']
        details = request.form['textfield3']
        price = request.form['textfield4']
        db = Db()
        db.update("update product set Product_name='"+pname+"',Quantity='"+quantity+"',details='"+details+"',seller_price='"+price+"' where Product_id='"+b+"'")
        return redirect('/view_product')
    else:
        db=Db()
        ss=db.selectOne("select * from product where Product_id='"+b+"'")
        return render_template('seller_side/update_product.html',data=ss)

@app.route('/delete_product_seller/<b>')
def delete_product_seller(b):
    db=Db()
    db.delete("delete from product where Product_id='"+b+"'")
    return redirect('/view_product')



@app.route('/add_bank_details',methods=['get','post'])
def add_bank_details():
    if request.method=="POST":
        bname=request.form['textfield']
        acno=request.form['textfield2']
        ifsc=request.form['textfield3']
        amount=request.form['textfield4']
        db=Db()
        ss=db.selectOne("select * from bank where account_no='"+acno+"' and ifsc='"+ifsc+"' and person_id='"+str(session['lid'])+"'")
        if ss is not None:
            db.update("update bank set account_no='"+acno+"',ifsc='"+ifsc+"',amount='"+amount+"' where person_id='"+str(session['lid'])+"'")
            return '''<script>alert('updated');window.location="/seller_home"</script>'''
        else:
            db.insert("insert into bank VALUES ('','"+str(session['lid'])+"','"+acno+"','"+ifsc+"','"+amount+"','seller')")
            return '''<script>alert('bank details added');window.location="/seller_home"</script>'''
    else:
        return render_template('seller_side/add_bank.html')

@app.route('/view_payment_seller',methods=['get','post'])
def view_payment_seller():
    if request.method=="POST":
        mnth=request.form['select']
        print(mnth)
        db=Db()
        ss=db.select("select * from product where status='accepted' and seller_id='"+str(session['lid'])+"' and month(`date`)='"+mnth+"'")
        s=db.select("select sum(Quantity * seller_price) as total,product.* from product where status='accepted' and seller_id='"+str(session['lid'])+"' and month(`date`)='"+mnth+"'")
        print(ss)

        return render_template('seller_side/payment_view.html',data=ss,a=s)
    else:
        return render_template('seller_side/payment_view.html')



############################################################################


########################################################3

    ###################################################user_side################3






@app.route('/user_home')
def user_home():
        return render_template("user_side/user_home.html")

@app.route('/add_user', methods=['get', 'post'])
def add_user():
        if request.method == "POST":
            db = Db()
            name = request.form['textfield2']
            photo = request.files['fileField']
            date = datetime.datetime.now().strftime("%y%m%d-%H%M%S")
            photo.save = (r"C:\flaskProject5\static\images/" + date + '.jpg')
            path = ("static/images/" + date + '.jpg')
            gender = request.form['radio']
            street = request.form['textfield3']
            Locality = request.form['textfield4']
            district = request.form['district']
            phoneno = request.form['textfield5']
            email = request.form['textfield6']
            password = request.form['textfield7']
            confirmpassword = request.form['textfield8']
            res = db.insert("insert into login values ('','" + email + "','" + str(password) + "','user')")
            db.insert("insert into user values ('" + str(
                res) + "','" + name + "','" + street + "','" + phoneno + "','" + gender + "','" + Locality + "','" + district + "','" + str(
                path) + "','" + email + "')")
            return '''<script>alert('register successfull');window.location="/"</script>'''
        else:
            return render_template('user_side/user_registration.html')

@app.route('/user_view_profile')
def user_view_profile():
        obj = Db()
        print(session["lid"])
        res = obj.selectOne("select * from user where user_id= '" + str(session["lid"]) + "'")
        print(res)
        return render_template('user_side/user profile view.html', res=res)

@app.route('/user_update/<c_id>', methods=['GET', 'POST'])
def center_update(c_id):
        db = Db()
        qry = "select * from user where user_id='" + str(session["lid"]) + "'"
        res = db.selectOne(qry)
        if request.method == 'POST':
            db = Db()
            name = request.form['abc']
            street = request.form['str']
            locality = request.form['local']
            district = request.form['district']
            phn = request.form['ph']
            # email=request.form['eml']
            # passw= request.form['pas']
            db.update(
                "update user set user_name = '" + name + "',street = '" + street + "',locality = '" + locality + "', district = '" + district + "', phone_number='" + phn + "'  where user_id ='" + str(
                    session['lid']) + "'")
            # db.update("update login set user_name='" + name + "',password='"+passw+"' where login_id='"+str(session["lid"])+"'")
            return ''' <script> alert("Updated Sucessfully");window.location = "/user_view_profile"  </script>'''
        else:
            return render_template('user_side/update user.html', res=res)

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



@app.route('/add_bank_user', methods=['get', 'post'])
def add_bank_user():
        if request.method == "POST":
            bname = request.form['textfield']
            acno = request.form['textfield2']
            ifsc = request.form['textfield3']
            amount = request.form['textfield4']
            db = Db()
            db.insert("insert into bank VALUES ('','" + str(
                session['lid']) + "','" + acno + "','" + ifsc + "','" + amount + "','user')")
            return '''<script>alert('bank details added');window.location="/user_home"</script>'''
        else:
            return render_template('user_side/add_bank_user.html')

@app.route('/cancel_booking_user/<b>')
def cancel_booking_user(b):
        db = Db()
        db.delete("delete from soil_report where soilreport_id='" + b + "'")
        return '''<script>alert('booking cancelled');window.location="/view_soil_booking"</script>'''

@app.route('/view_product_user')
def view_product_user():
        db = Db()
        ss = db.select("select  * from product")
        return render_template('user_side/view product.html', data=ss)

    # @app.route('/cart')
    # def cart():
    #     return render_template("user/cart view.html")

@app.route('/add_to_cart/<b>', methods=['get', 'post'])
def add_to_cart(b):
        print(b)
        if request.method == "POST":
            db = Db()
            Quantity = request.form['textfield2']
            # s=db.select("select * from product where Quantity>='"+Quantity+"' and Product_id='"+b+"'")
            # print(s)
            # if len(s)>0:
            ss = db.selectOne(
                "select  * from booking_master where user_id='" + str(session['lid']) + "' and status='add to cart'")
            s = db.selectOne("select * from product where  Product_id='" + b + "'")
            print(s['Quantity'], Quantity)
            print(ss)
            if ss is not None:
                if s['Quantity'] > Quantity:
                    p = s['Quantity'] > Quantity
                    print("oooooooooooooooo", p)
                    db.update("update booking set Quantity='" + Quantity + "' where Product_id='" + b + "'")
                    return '''<script>alert('successfully updated');window.location="/view_cart"</script>'''
                else:
                    return '''<script>alert('enter proper quantity');window.location="/view_product_user"</script>'''
            else:
                print("p")
                if s['Quantity'] > Quantity:
                    p = s['Quantity'] > Quantity
                    print("oooooooooooooooo", p)
                    res = db.insert("insert into booking_master VALUES ('','" + str(
                        session['lid']) + "',0,curdate(),'add to cart')")
                    db.insert("insert into booking VALUES ('','" + str(res) + "','" + b + "','" + Quantity + "')")
                    return '''<script>alert('successfully added');window.location="/view_cart"</script>'''
                else:
                    return '''<script>alert('enter proper quantity');window.location="/view_product_user"</script>'''
                    # else:
                    #     return '''<script>alert('insufficient quantity');window.location="/view_product_user"</script>'''
                    # else:
                    #
        else:
            db = Db()
            ss = db.selectOne("select * from product where Product_id='" + b + "'")
            # print(ss)
            return render_template('user_side/add_quantity.html', data=ss)

@app.route('/view_cart')
def view_cart():
        db = Db()
        ss = db.select(
            "select sum(booking.quantity* product.admin_price) AS totalsum, product.admin_price AS h,booking.quantity AS d,booking.booking_id AS b ,product.*,booking.*,booking_master.* from booking,booking_master,product where booking.master_id=booking_master.master_id and booking.product_id=product.Product_id  and booking_master.user_id='" + str(
                session['lid']) + "' and booking_master.status='add to cart' ")
        v = db.select(
            "select sum(booking.quantity* product.admin_price) AS totalsum,booking.*,product.* from booking,product where booking.product_id=product.Product_id")
        return render_template('user_side/cart view.html', a=ss, data=v)

@app.route('/book_mode/<mid>', methods=['get', 'post'])
def book_mode(mid):
        if request.method == "POST":
            mode = request.form['RadioGroup1']
            amount = request.form['text']
            print(mode)
            if mode == 'offline':
                db = Db()
                db.update("update booking_master set status='cash on delivery' where master_id='" + mid + "' ")
                return '''<script>alert('THANK YOU !!cash on delivery');window.location="/user_home"</script>'''
            else:
                db = Db()

                v = db.select(
                    "select sum(booking.quantity* product.admin_price) AS totalsum,booking.quantity as q,booking.*,product.* from booking,product where booking.product_id=product.Product_id")
                db.update("update booking_master set amount='" + amount + "' where master_id='" + mid + "'")
                return render_template('user_side/add_payment_user.html', a=v, data=mid)
        else:
            db = Db()
            ss = db.select(
                "select product.admin_price AS h,booking.quantity AS d,booking.booking_id AS b ,product.*,booking.*,booking_master.* from booking,booking_master,product where booking.master_id=booking_master.master_id and booking.product_id=product.Product_id  and booking_master.user_id='" + str(
                    session['lid']) + "' ")
            v = db.select(
                "select sum(booking.quantity* product.admin_price) AS totalsum,booking.*,product.* from booking,product where booking.product_id=product.Product_id")

            return render_template('user_side/book_radio.html', a=ss, data=v)

@app.route('/add_payment', methods=['get', 'post'])
def add_payment():
        if request.method == "POST":
            db = Db()
            acc = request.form['abc']
            ifsc = request.form['efg']
            totalsum = request.form['t1']
            quantity = request.form['t3']
            pid = request.form['t2']
            print("sdfbgn", quantity, pid)
            res = db.selectOne(
                "select * from bank WHERE account_no='" + acc + "' and ifsc='" + ifsc + "' and person_id='" + str(
                    session["lid"]) + "'")
            b = db.selectOne("select quantity from product where ")
            if res is not None:
                # p= int(res['amount'])
                # print(p,totalsum)
                a = float(totalsum)
                s = int(res['amount']) - float(totalsum)
                print(s, a)

                db.update("update booking_master set status='booked'  where user_id='" + str(session['lid']) + "' ")

                db.update("update bank set amount='" + str(s) + "' where person_id='" + str(
                    session["lid"]) + "' and account_no='" + acc + "' ")
                db.update("update bank set amount=amount+'" + str(a) + "' where type='admin'  ")
                return ''' <script> alert("Booked Successfully");window.location = "/user_home"  </script>'''

            else:
                return ''' <script> alert("Enter Correct Account Number");window.location = "/view_cart"  </script>'''
        else:
            db = Db()
            ss = db.select(
                "select product.admin_price AS h,booking.quantity AS d,booking.booking_id AS b ,product.*,booking.*,booking_master.* from booking,booking_master,product where booking.master_id=booking_master.master_id and booking.product_id=product.Product_id  and booking_master.user_id='" + str(
                    session['lid']) + "' ")
            v = db.select(
                "select sum(booking.quantity* product.admin_price) AS totalsum,booking.*,product.* from booking,product where booking.product_id=product.Product_id")

            return render_template('user_side/add_payment_user.html', a=v)

@app.route('/user_feedback', methods=['GET', 'POST'])
def user_feedback():
        if request.method == 'POST':
            db = Db()
            noet = request.form['textarea']
            db.insert(
                "insert into feedback VALUES ('','" + noet + "', '" + str(session["lid"]) + "',curdate(),curtime())")
            return ''' <script> alert("Send Sucessfully");window.location = "/user_home"  </script>'''

        else:
            return render_template("user_side/feedback.html")

    # @app.route('/user_feedback',methods=['GET','POST'])
    # def user_feedback():
    #     if request.method == 'POST':
    #         db=Db()
    #         noet=request.form['textarea']
    #         db.insert("insert into feedback VALUE('','" + noet +"', '"+str(session["lid"])+"',curdate(),curtime())")
    #         return ''' <script> alert("Send Sucessfully");window.location = "/center_view/<c_id>"  </script>'''
    #     else:
    #         return render_template("user/feedback.html")


@app.route('/soil_request', methods=['GET', 'POST'])
def soil_request():
        db = Db()
        obj = db.selectOne("select * from user where user_id='" + str(session["lid"]) + "'")
        print(obj, str(session['lid']))
        if request.method == 'POST':
            db = Db()
            amnt = 500
            res = db.insert("insert into soil_report VALUE('', '" + str(session["lid"]) + "','" + str(
                amnt) + "',curdate(),'pending')")
            session['soil_id'] = res
            return ''' <script> alert("Send Sucessfully");window.location = "/soil_payment"  </script>'''
        else:
            return render_template("user_side/sent soil report.html", res=obj)

@app.route('/view_booking')
def view_booking():
        db = Db()
        obj = db.selectOne("select * from booking_master,product,booking where user_id='" + str(session[
                                                                                                    "lid"]) + "' and  booking_master.master_id=booking.master_id and booking.Product_id=product.Product_id")

        return render_template("user_side/view booking.html", res=obj)

@app.route('/soil_payment', methods=['GET', 'POST'])
def soil_payment():

        if request.method == 'POST':
            db = Db()
            acc = request.form['abc']
            ifsc = request.form['efg']
            # car = request.form['efg']
            # mon = request.form['ijk']
            # yr = request.form['lmn']
            # cvv = request.form['hjk']
            res = db.selectOne(
                "select * from bank WHERE account_no='" + acc + "' and ifsc='" + ifsc + "' and person_id='" + str(
                    session["lid"]) + "'")

            if res is not None:
                amount1 = int(res['amount'])
                if amount1 >= 500:
                    db.update(
                        "update soil_report set status='booked' where soilreport_id='" + str(session['soil_id']) + "' ")
                    db.update("update bank set amount='" + str(amount1 - 500) + "' where person_id='" + str(
                        session["lid"]) + "' and account_no='" + acc + "' ")
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
            return render_template("user_side/soil payment.html")

@app.route('/view_soil_booking')
def view_soil_booking():
        qry = "select * from soil_report where user_id='" + str(session["lid"]) + "';"
        obj = Db()
        res = obj.select(qry)
        return render_template("user_side/view soil report.html", res=res)

@app.route('/user_complaint', methods=['get', 'post'])
def user_complaint():
        if request.method == 'POST':
            db = Db()
            noet = request.form['textarea']
            db.insert("insert into complaint VALUES ('','" + noet + "',curdate(), '" + str(
                session["lid"]) + "','pending','pending','user')")
            return ''' <script> alert("Send Sucessfully");window.location = "/user_home"  </script>'''
        else:
            return render_template("user_side/complaint.html")

@app.route('/view_reply_user')
def view_reply_user():
        qry = "select * from complaint where user_id='" + str(session["lid"]) + "';"
        obj = Db()
        res = obj.select(qry)
        return render_template("user_side/View_reply_user.html", data=res)




    #####################################################################################################3
# @app.route('/',methods=['GET','POST'])
# def login():
#     if request.method=="POST":
#         uname=request.form['username']
#         password=request.form['password']
#         db = Db()
#         res = db.selectOne("select * from login where user_name = '"+uname+"' and password = '"+password+"' ")
#
#         if res is not None:
#             if res['user_type'] == 'admin':
#                 return redirect('/home')
#
#             elif res['user_type'] == 'seller':
#                 session["lid"] = res['login_id']
#                 return redirect('/seller_home')
#
#             elif res['user_type'] == 'user':
#                 session["lid"] = res['login_id']
#                 return redirect('/user_home')
#
#             else:
#                 return '''<script>alert('invalid type');window.location="/"</script>'''
#         else:
#             return  '''<script>alert('invalid user name or password');window.location="/"</script>'''
#     else:
#         return render_template("login.html")
#
# #####################################################################ADMIN##########################################
#
# @app.route('/home')
# def home():
#
#     return render_template("admin/index.html")
#
#     return render_template("admin/admin home.html")
#
#
# @app.route('/add_employee',methods=['get','post'])
# def add_employee():
#     if request.method=="POST":
#         db=Db()
#         name = request.form['abc']
#         street=request.form['str']
#         locality=request.form['local']
#         district=request.form['district']
#         phn=request.form['ph']
#         email=request.form['eml']
#         db.insert(
#             "insert into employee VALUE ('','" + name + "','" + street + "','" + locality + "','" + district + "','" + phn + "','" + email + "')")
#         return '''<script>alert('successfull');window.location="/add_employee"</script>'''
#     else:
#         return render_template('admin/employee_registration.html')
#
# @app.route('/view_employee')
# def view_employee():
#     db=Db()
#     res=db.select("select * from employee  ")
#     return render_template('admin/view_employee.html',data=res)
#
#
# @app.route('/edit_employee/<e_id>',methods=['GET','POST'])
# def edit_employee(e_id):
#     if request.method=="POST":
#         db = Db()
#         name = request.form['abc']
#         street = request.form['str']
#         locality = request.form['local']
#         district = request.form['district']
#         phn = request.form['ph']
#         email=request.form['eml']
#         db.update("update employee set name = '" + name + "',street = '" + street + "',locality = '" + locality + "', district = '" + district + "', phone_no='" + phn + "',email='"+email+"'  where employee_id ='" +e_id + "'")
#
#         return ''' <script> alert("Update Sucessfully");window.location = "/view_employee"  </script>'''
#
#     else:
#         db=Db()
#         emp=db.selectOne("select * from employee where employee_id='"+e_id+"'")
#         return render_template('admin/edit employee.html', res=emp)
#
# @app.route('/delete_employee/<e_id>')
# def delete_employee(e_id):
#     db=Db()
#     db.delete("delete from employee where employee_id='"+e_id+"'")
#     return '''<script>alert('success');window.location="/view_employee"</script>'''
#
#
#
# @app.route('/soil_report')
# def soil_report():
#         obj = Db()
#         qry = "select * from soil_report,user where soil_report.user_id=user.user_id and soil_report.status='booked'"
#
#         res = obj.select(qry)
#         return render_template("admin/View Booking Master.html",res=res)
#
# @app.route('/allocate_soil_emp/<b>')
# def allocate_soil_emp(b):
#     print(b)
#     db=Db()
#     r = db.select("select * from soil_report,allocate where soil_report.soilreport_id=allocate.request_id")
#     print(r)
#     if len(r) >0:
#         return '''<script>alert('Already Assigned');window.location="/soil_report"</script>'''
#     else:
#         qry=db.select("select * from employee")
#         return render_template("admin/allocation emp view.html", qry=qry,data=b)
#
# @app.route('/assign_emp/<b>/<c>',methods=['get','post'])
# def assign_emp(b,c):
#     print(b)
#     # r_id=request.form['textfield']
#     # print(r_id)
#     db=Db()
#     db.insert("insert into allocate values('','"+str(c)+"','"+b+"','soil')")
#     return '''<script>alert('success');window.location="/soil_report"</script>'''
#
#
#
#     qry = "select * from soil_report,user where soil_report.user_id=user.user_id and soil_report.status='booked'"
#     obj = Db()
#     res = obj.select(qry)
#     return render_template("admin/View Booking Master.html",res=res)
#
#
#
# @app.route('/booking_master_report/<b_id>',methods=['GET','POST'])
# def booking_master_report(b_id):
#     if request.method=="POST":
#         rprt=request.files['fileField']
#         d=datetime.datetime.now().strftime("%Y%m%d%H%M%S")
#         rprt.save(syspath+d+'.pdf')
#         path='/static/kisan/'+d+'.pdf'
#         db = Db()
#         db.update("update soil_report set status = '"+path+"' where soilreport_id='" +str( b_id) + "' ")
#
#         return '''<script>alert('report added');window.location="/home"</script>'''
#
#
#         return '''<script>alert('report added');window.location="/home"</script>'''
#
#         return "OK"
#
#
#
#     else:
#         return render_template("admin/Booking Master Report.html")
#
#
# @app.route('/complaint')
# def complaint():
#     qry = "select * from complaint,user,seller where complaint.user_id=user.user_id "
#     obj = Db()
#     res = obj.select(qry)
#     return render_template("admin/View Complaint.html",res=res)
#
# @app.route('/seller_complaint_admin')
# def seller_complaint_admin():
#     qry = "select * from complaint,seller where complaint.user_id=seller.seller_id "
#     obj = Db()
#     res = obj.select(qry)
#     return render_template("admin/View Complaint_seller.html",res=res)
#
#
# @app.route('/seller_complaint_replay/<c_id>',methods=['GET','POST'])
# def seller_complaint_replay(c_id):
#     if request.method=="POST":
#         reply=request.form['textarea']
#         db = Db()
#         db.update("update complaint set reply = '"+reply+"', reply_date=curdate() where compaint_id = '"+c_id+"'")
#
#         return ''' <script> alert("Send Sucessfully");window.location = "/complaint_admin"  </script>'''
#     else:
#         return render_template("admin/Complaint Replay.html")
#
# # @app.route('/seller_complaint_admin')
# # def seller_complaint_admin():
# #     qry = "select * from complaint,seller where complaint.user_id=seller.seller_id "
# #     obj = Db()
# #     res = obj.select(qry)
# #     return render_template("admin/View Complaint_seller.html",res=res)
#
#
# # @app.route('/seller_complaint_replay/<c_id>',methods=['GET','POST'])
# # def seller_complaint_replay(c_id):
# #     if request.method=="POST":
# #         reply=request.form['textarea']
# #         db = Db()
# #         db.update("update complaint set reply = '"+reply+"', reply_date=curdate() where compaint_id = '"+c_id+"'")
# #
# #         return ''' <script> alert("Send Sucessfully");window.location = "/seller_complaint_admin"  </script>'''
# #     else:
# #         return render_template("admin/Complaint Replay.html")
#
#
# @app.route('/feedback')
# def feedback():
#     qry = "select * from feedback,user where feedback.user_id=user.user_id"
#     obj = Db()
#     res = obj.select(qry)
#     return render_template("admin/View feedback.html",res=res)
#
#
#
# @app.route('/rating')
# def rating():
#     qry = "SELECT rating.user_id ,rating.rating,user.user_name FROM rating INNER JOIN user ON rating.user_id=user.user_id;"
#     obj = Db()
#     res = obj.select(qry)
#     print(res)
#     return render_template("admin/view _rating.html",data=res)
#
# @app.route('/product')
# def product():
#     qry = "select * from product,user where product.user_id=user.user_id"
#     obj = Db()
#     res = obj.select(qry)
#     return render_template("admin/View Product.html",res=res)
#
#
# @app.route('/booking')
# def booking():
#     qry = " select * from booking_master,user where  booking_master.user_id=user.user_id and booking_master.status='booked'"
#     obj = Db()
#     res = obj.select(qry)
#     return render_template("admin/View BOOKING.HTML",res=res)
#
#
# @app.route('/view_booked_products/<mid>')
# def view_booked_products(mid):
#     print(mid)
#     qry = " select  * from booking,product,booking_master where  booking.product_id=product.product_id and booking.master_id='"+mid+"' and booking_master.master_id=booking.master_id"
#     obj = Db()
#     res = obj.select(qry)
#
#     return render_template("admin/View booked products.HTML",res=res)
#
#
# @app.route('/payment')
# def payment():
#     qry = "select * from user,payment where user.user_id=payment.user_id; "
#     obj = Db()
#     res = obj.select(qry)
#     return render_template("admin/View Payment.html",res=res)
#
#
# @app.route('/user')
# def user():
#     qry= "select *from user"
#     obj=Db()
#     res=obj.select(qry)
#     return render_template("admin/View User.html", res=res)
#
# @app.route('/notification',methods=['GET','POST'])
# def notification():
#     if request.method == 'POST':
#         db=Db()
#         noet=request.form['textarea']
#         db.insert("insert into notification VALUE('','" + noet +"',curdate(),curtime())")
#         return ''' <script> alert("Send Sucessfully");window.location = "/notification"  </script>'''
#
#     else:
#         return render_template("admin/notification.html")
#
#
# @app.route('/view_seller_request')
# def view_seller_request():
#     db=Db()
#
#     prd=db.select("select * from seller,product where seller.seller_id=product.seller_id and status='pending'")
#
#     # prd=db.select("select * from seller,product_request where seller.seller_id=product_request.seller_id and status='pending'")
#
#     return render_template("admin/view_seller_request.html",res=prd)
#
#
# @app.route('/accept_seller/<s_id>')
# def accept_seller(s_id):
#     db=Db()
#
#     db.update("update product set status='accepted' where Product_id='"+s_id+"'")
#
#     db.update("update product_request set status='accepted' where request_id='"+s_id+"'")
#
#     return ''' <script> alert("Accepted");window.location = "/view_seller_request"  </script>'''
#
# @app.route('/reject_seller/<s_id>')
# def reject_seller(s_id):
#     db=Db()
#
#     db.delete("delete from product where Product_id='"+s_id+"'")
#
#     db.delete("delete from product_request where request_id='"+s_id+"'")
#
#     return ''' <script> alert("Deleted");window.location = "/view_seller_request"  </script>'''
#
#
#
# @app.route('/view_accepted_seller')
# def view_accepted_seller():
#     db=Db()
#
#     res=db.select("select * from seller,product where seller.seller_id=product.seller_id and status='accepted'")
#
#     # res=db.select("select * from seller,product_request where seller.seller_id=product_request.seller_id and status='accepted'")
#
#     return render_template("admin/view_accepted_seller.html",res=res)
#
#
#
# @app.route('/allocate_emp_seller/<b>')
# def allocate_emp_seller(b):
#     print(b)
#     db=Db()
#
#     res = db.select("select * from product,allocate where product.Product_id=allocate.request_id and type='collect'")
#
#     # res = db.select("select * from product_request,allocate where product_request.request_id=allocate.request_id and type='collect'")
#
#     print(res)
#     if len(res) >0:
#         return '''<script>alert('Already Assigned');window.location="/view_accepted_seller"</script>'''
#     else:
#         qry=db.select("select * from employee")
#         return render_template("admin/allocation emp view_seller.html", qry=qry,data=b)
#
# @app.route('/assign_emp_seller/<b>/<c>', methods=['get', 'post'])
# def assign_emp_seller(b, c):
#     print(b)
#     # r_id=request.form['textfield']
#     # print(r_id)
#
#     db = Db()
#
#     db.insert("insert into allocate values('','" + str(c) + "','" + b + "','product','free',curdate())")
#
#     db.insert("insert into allocate values('','" + str(c) + "','" + b + "','collect')")
#
#     return '''<script>alert('success');window.location="/view_accepted_seller"</script>'''
#

####################################################seller

# @app.route('/seller_registration',methods=['GET','POST'])
# def seller_registration():
#     if request.method=='POST':
#         name=request.form['abc']
#         street=request.form['str']
#         locality=request.form['local']
#         district=request.form['district']
#         phn=request.form['ph']
#         email=request.form['eml']
#         passw= request.form['pas']
#         db=Db()
#         db.insert("insert into seller VALUE ('','"+name+"','"+street+"','"+locality+"','"+district+"','"+phn+"','"+email+"')")
#         db.insert("insert into login VALUE('','"+name+"','"+passw+"','seller')")
#         return ''' <script> alert("Registered Sucessfully");window.location = "/"  </script>'''
#     else:
#         return render_template('seller/seller_registraction.html')
#
#
# @app.route('/seller_view_profile')
# def seller_view_profile():
#     obj=Db()
#     print(session["lid"])
#     qry="select * from seller where seller_id= '"+str(session["lid"])+"'"
#     res = obj.selectOne(qry)
#     return render_template('seller/seller profile view.html', res=res)
#
#
# @app.route('/edit_seller',methods=['GET','POST'])
# def edit_seller():
#     if request.method=="POST":
#         db = Db()
#         name = request.form['abc']
#         street = request.form['str']
#         locality = request.form['local']
#         district = request.form['district']
#         phn = request.form['ph']
#         email=request.form['eml']
#         db.update("update seller set name = '" + name + "',street = '" + street + "',locality = '" + locality + "', district = '" + district + "', phoneno='" + phn + "',email='"+email+"'  where seller_id ='"+str(session["lid"])+"'")
#         db.update("update login set user_name='" + name + "'  where login_id ='"+str(session["lid"])+"'")
#         return ''' <script> alert("Update Sucessfully");window.location = "/seller_view_profile"  </script>'''
#     else:
#         db=Db()
#         emp=db.selectOne("select * from seller where seller_id='"+str(session["lid"])+"'")
#         return render_template('seller/update seller.html', res=emp)
#
#
#
# # @app.route('/edit_seller',methods=['GET','POST'])
# # def edit_seller():
# #     if request.method=="POST":
# #         db = Db()
# #         name = request.form['abc']
# #         street = request.form['str']
# #         locality = request.form['local']
# #         district = request.form['district']
# #         phn = request.form['ph']
# #         email=request.form['eml']
# #         db.update("update seller set name = '" + name + "',street = '" + street + "',locality = '" + locality + "', district = '" + district + "', phoneno='" + phn + "',email='"+email+"'  where seller_id ='"+str(session["lid"])+"'")
# #         db.update("update login set user_name='" + name + "'  where login_id ='"+str(session["lid"])+"'")
# #         return ''' <script> alert("Update Sucessfully");window.location = "/seller_view_profile"  </script>'''
# #     else:
# #         db=Db()
# #         emp=db.selectOne("select * from seller where seller_id='"+str(session["lid"])+"'")
# #         return render_template('seller/update seller.html', res=emp)
#
#
# @app.route('/seller_home')
# def center_home():
#     return render_template("seller/seller home.html")
#
#
# # @app.route('/seller_home')
# # def center_home():
# #     return render_template("seller/seller home.html")
#
# @app.route('/seller_complaint',methods=['GET','POST'])
# def seller_complaint():
#     if request.method == "POST":
#         reply = request.form['textarea']
#         db = Db()
#         db.insert("insert into complaint VALUE('','" + reply + "', curdate(),'" + str(session["lid"]) + "','pending','pending','seller')")
#         return ''' <script> alert("Send Sucessfully");window.location = "/seller_home"  </script>'''
#     else:
#         return render_template('seller/complaint.html')
#
#
# @app.route('/seller_soil_request',methods=['GET','POST'])
# def seller_soil_request():
#     db=Db()
#     obj=db.selectOne("select * from seller where seller_id='"+str(session["lid"])+"'")
#     if request.method == 'POST':
#         db=Db()
#         amnt=500
#         res = db.insert("insert into soil_report VALUE('', '"+str(session["lid"])+"','"+str(amnt)+"',curdate(),'pending')")
#         session['soil_id']=res
#         return ''' <script> alert("Send Sucessfully");window.location = "/seller_soil_payment"  </script>'''
#     else:
#         return render_template("seller/sent soil request seller.html",res=obj)
#
#
# @app.route('/seller_soil_payment',methods=['GET','POST'])
# def seller_soil_payment():
#
#     if request.method == 'POST':
#         db = Db()
#         acc = request.form['abc']
#         # car = request.form['efg']
#         # mon = request.form['ijk']
#         # yr = request.form['lmn']
#         # cvv = request.form['hjk']
#         res=db.selectOne("select * from payment WHERE account_no='"+acc+"' and user_id='"+str(session["lid"])+"'")
#         amount1 = int(res['amount'])
#         if res is not None:
#             if amount1 >500:
#                 db.update("update soil_report set status='booked' where soilreport_id='" + str(session['soil_id']) + "' ")
#                 db.update("update payment set amount='"+str(amount1-500)+"' where user_id='" + str(session["lid"]) + "' and account_no='"+acc+"' ")
#                 db.update("update payment set amount=amount+500 where user_id=1  ")
#                 return ''' <script> alert("Booked Successfully");window.location = "/seller_home"  </script>'''
#             else:
#                 return ''' <script> alert("insufficient Balance");window.location = "/soil_payment"  </script>'''
#         else:
#             return ''' <script> alert("Enter Correct Account Number");window.location = "/soil_payment"  </script>'''
#         # et = db.selectOne("select amount from payment WHERE user_id='" + str(session["lid"]) + "'")
#         # print(ed,et,acc)
#         # if ed==str(acc):
#         #     if et>=500:
#         #         db.update("update soil_report set status='booked' where user_id='" + str(session["lid"]) + "' ")
#         #         db.update("update payment set amount=amount-500 where user_id='" + str(session["lid"]) + "'")
#         #         return ''' <script> alert("Send Sucessfully");window.location = "/"  </script>'''
#         #     else:
#         #         return ''' <script> alert("insufficient Balance");window.location = "/soil_payment"  </script>'''
#         # else:
#         #     return ''' <script> alert("Enter Correct Account Number");window.location = "/soil_payment"  </script>'''
#
#
#     else:
#         return render_template("seller/seller soil payment.html" )
#
#
#
# #@app.route('/view_soil_booking')
# # def view_soil_booking():
# #         qry = "select * from soil_report where user_id='"+str(session["lid"])+"';"
# #         obj = Db()
# #         res = obj.select(qry)
# #         return render_template("user/view soil report.html", res=res)
#
#
#
# @app.route('/view_soil_report_seller')
# def view_soil_report_seller():
#     qry=select("select * from soil_report where ")
#
#
#
# @app.route('/add_product')
# def add_product():
#     qry = "select * from ,user where query.user_id=user.user_id;"
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

# @app.route('/user_home')
# def user_home():
#     return render_template("user/user_home.html")
#
#
#
#
# @app.route('/add_user',methods=['get','post'])
# def add_user():
#     if request.method=="POST":
#         db=Db()
#         name=request.form['textfield2']
#         photo=request.files['fileField']
#         date=datetime.datetime.now().strftime("%y%m%d-%H%M%S")
#
#         photo.save=(r"C:\Users\akhil\Downloads\flaskProject5\static\images\\"+date+'.jpg')
#
#         photo.save=(r"C:\flaskProject5\static\images/"+date+'.jpg')
#
#         path=("static/images/"+date+'.jpg')
#         gender=request.form['radio']
#         street=request.form['textfield3']
#         Locality=request.form['textfield4']
#         district=request.form['district']
#         phoneno=request.form['textfield5']
#         email=request.form['textfield6']
#         password=request.form['textfield7']
#         confirmpassword=request.form['textfield8']
#         db.insert("insert into login values ('','"+email+"','"+str(confirmpassword)+"','user')")
#         db.insert ("insert into user values ('','"+name+"','"+street+"','"+phoneno+"','"+gender+"','"+Locality+"','"+district+"','"+str(path)+"','"+email+"')")
#         return '''<script>alert('register successfull');window.location="/user_home"</script>'''
#     else:
#         return render_template('user/user_registration.html')
#
#
# @app.route('/user_view_profile')
# def user_view_profile():
#     obj=Db()
#     print(session["lid"])
#     res = obj.selectOne("select * from user where user_id= '"+str(session["lid"])+"'")
#     print(res)
#     return render_template('user/user profile view.html', res=res)
#
#
#
# @app.route('/user_update/<c_id>',methods=['GET','POST'])
# def center_update(c_id):
#     db = Db()
#     qry = "select * from user where user_id='"+str(session["lid"])+"'"
#     res=db.selectOne(qry)
#     if request.method=='POST':
#        db=Db()
#        name=request.form['abc']
#        street=request.form['str']
#        locality=request.form['local']
#        district=request.form['district']
#        phn=request.form['ph']
#        # email=request.form['eml']
#        passw= request.form['pas']
#        db.update("update user set user_name = '" + name + "',street = '"+street+"',locality = '"+locality+"', district = '"+district+"', phone_number='"+phn+"'  where user_id ='"+str(session['lid'])+"'")
#        db.update("update login set user_name='" + name + "',password='"+passw+"' where login_id='"+str(session["lid"])+"'")
#        return ''' <script> alert("Send Sucessfully");window.location = "/center_view/<c_id>"  </script>'''
#     else:
#          return render_template('user/update user.html',res=res)
#
#
# # @app.route('/insert/<u_id>',methods=['GET','POST'])
# # def update_user(u_id):
# #      db = Db()
# #      qry = "select * from booking,seller,user where booking.street =seller.street"
# #      res=db.select(qry)
# #      if request.method=='POST':
# #          db=Db()
# #          noet=request.form['textarea']
# #
# #          db.insert("insert into notification VALUE('','"+noet+"','" + u_id + "',curdate(),datetime.now())")
# #          return ''' <script> alert("Send Sucessfully");window.location = "/center_view/<c_id>"  </script>'''#
# #      else:
# #
# #         return render_template('seller/update_center.html',res=res)
#
# @app.route('/cart')
# def cart():
#     return render_template("user/cart view.html")
#
#
# @app.route('/user_feedback',methods=['GET','POST'])
# def user_feedback():
#      if request.method == 'POST':
#          db=Db()
#          noet=request.form['textarea']
#          db.insert("insert into feedback VALUE('','" + noet +"', '"+str(session["lid"])+"',curdate(),curtime())")
#          return ''' <script> alert("Send Sucessfully");window.location = "/user_feedback"  </script>'''
#
#
#      else:
#         return render_template("user/feedback.html")
# # @app.route('/user_feedback',methods=['GET','POST'])
# # def user_feedback():
# #     if request.method == 'POST':
# #         db=Db()
# #         noet=request.form['textarea']
# #         db.insert("insert into feedback VALUE('','" + noet +"', '"+str(session["lid"])+"',curdate(),curtime())")
# #         return ''' <script> alert("Send Sucessfully");window.location = "/center_view/<c_id>"  </script>'''
# #
# #     else:
# #         return render_template("user/feedback.html")
#
#
# # @app.route('/user_feedback',methods=['GET','POST'])
# # def user_feedback():
# #     if request.method == 'POST':
# #         db=Db()
# #         noet=request.form['textarea']
# #         db.insert("insert into feedback VALUE('','" + noet +"', '"+str(session["lid"])+"',curdate(),curtime())")
# #         return ''' <script> alert("Send Sucessfully");window.location = "/center_view/<c_id>"  </script>'''
# #     else:
# #         return render_template("user/feedback.html")
#
#
# @app.route('/soil_request',methods=['GET','POST'])
# def soil_request():
#     db=Db()
#     obj=db.selectOne("select * from user where user_id='"+str(session["lid"])+"'")
#     if request.method == 'POST':
#         db=Db()
#
#
#
#         name = request.form['abc']
#         street = request.form['def']
#         locality = request.form['jkl']
#         phn= request.form['mno']
#
#
#         amnt=500
#         res = db.insert("insert into soil_report VALUE('', '"+str(session["lid"])+"','"+str(amnt)+"',curdate(),'pending')")
#         session['soil_id']=res
#         return ''' <script> alert("Send Sucessfully");window.location = "/soil_payment"  </script>'''
#     else:
#         return render_template("user/sent soil report.html",res=obj)
#
# @app.route('/view_booking')
# def view_booking():
#     db=Db()
#     obj=db.selectOne("select * from booking,booking_master,product where booking.master_id=booking_master.master_id and booking.product_id=product.product_id and user_id='"+str(session["lid"])+"'")
#
#     return render_template("user/view booking.html", res=obj)
#
#
#
# @app.route('/soil_payment',methods=['GET','POST'])
# def soil_payment():
#
#
#
#     if request.method == 'POST':
#         db = Db()
#         acc = request.form['abc']
#         # car = request.form['efg']
#         # mon = request.form['ijk']
#         # yr = request.form['lmn']
#         # cvv = request.form['hjk']
#         res=db.selectOne("select * from payment WHERE account_no='"+acc+"' and user_id='"+str(session["lid"])+"'")
#         amount1 = int(res['amount'])
#         if res is not None:
#             if amount1 >=500:
#                 db.update("update soil_report set status='booked' where soilreport_id='" + str(session['soil_id']) + "' ")
#                 db.update("update payment set amount='"+str(amount1-500)+"' where user_id='" + str(session["lid"]) + "' and account_no='"+acc+"' ")
#                 return ''' <script> alert("Booked Successfully");window.location = "/soil_payment"  </script>'''
#             else:
#                 return ''' <script> alert("insufficient Balance");window.location = "/soil_payment"  </script>'''
#         else:
#
#             return ''' <script> alert("Enter Correct Account Number");window.location = "/soil_payment"  </script>'''
#         # et = db.selectOne("select amount from payment WHERE user_id='" + str(session["lid"]) + "'")
#         # print(ed,et,acc)
#         # if ed==str(acc):
#         #     if et>=500:
#         #         db.update("update soil_report set status='booked' where user_id='" + str(session["lid"]) + "' ")
#         #         db.update("update payment set amount=amount-500 where user_id='" + str(session["lid"]) + "'")
#         #         return ''' <script> alert("Send Sucessfully");window.location = "/"  </script>'''
#         #     else:
#         #         return ''' <script> alert("insufficient Balance");window.location = "/soil_payment"  </script>'''
#         # else:
#         #      return ''' <script> alert("Enter Correct Account Number");window.location = "/soil_payment"  </script>'''
#
#
#     else:
#         return render_template("user/soil payment.html" )
#
#
#
# @app.route('/view_soil_booking')
# def view_soil_booking():
#         qry = "select * from soil_report where user_id='"+str(session["lid"])+"';"
#         obj = Db()
#         res = obj.select(qry)
#         return render_template("user/view soil report.html", res=res)
#
#
#
# @app.route('/user_complaint',methods=['GET','POST'])
#
# # @app.route('/user_complaint')
#
# def user_complaint():
#     if request.method == 'POST':
#         db=Db()
#         noet=request.form['textarea']
#
#         db.insert("insert into complaint VALUE('','" + noet +"',curdate(), '"+str(session["lid"])+"','pending','pending','user')")
#         return ''' <script> alert("Send Sucessfully");window.location = "/user_home/<c_id>"  </script>'''
#     else:
#         return render_template("user/feedback.html")
#
#
# # @app.route('/user_complaint')
#
#
#         # db.insert("insert into complaint VALUE('','" + noet +"', '"+str(session["lid"])+"',curdate(),curtime())")
#         # return ''' <script> alert("Send Sucessfully");window.location = "/center_view/<c_id>"  </script>'''
#     # else:
#     #     return render_template("user/feedback.html")


if __name__ == '__main__':
    app.run()
