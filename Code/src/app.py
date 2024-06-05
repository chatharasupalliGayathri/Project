# from flask import Flask,render_template,redirect 
from web3 import Web3,HTTPProvider
import json
import os
from flask import Flask,render_template,request,redirect,session
from bson import ObjectId
from pymongo import MongoClient
from datetime import datetime
from keras.models import load_model  
from PIL import Image, ImageOps  
import numpy as np
import requests
import urllib3

blockchain="http://127.0.0.1:7545"
web3=Web3(HTTPProvider(blockchain)) #tan-power
app=Flask('name',static_folder='static')
app.secret_key = 'fapo'
dbClient=MongoClient('mongodb://localhost:27017/')
db=dbClient['fapo']
userdata=db['userdata']
agroDealers=db['agroDealers']
indiBuyers=db['indiBuyers']
emarts=db['emarts']
biddings=db['biddings']
bioIndus=db['bioIndus']
negoData=db['negoData']
urequests=db['urequests']
loc=""
phno=""
name=""
msg1=""
sname=""
crop=""
crop1=""
cname=""
cphno=""
gtemp=""
gli=""
hum=""

# app=Flask(__name__,static_folder='static')

@app.route("/",methods=['POST','GET'])
def home1():
    return render_template('index.html')

@app.route("/about",methods=['POST','GET'])
def about1():
    return render_template('about.html')

@app.route("/service",methods=['POST','GET'])
def service1():
    return render_template('service.html')

# @app.route("/booking",methods=['POST','GET'])
# def booking():
#     return render_template('booking.html')

@app.route("/team",methods=['POST','GET'])
def team1():
    return render_template('team.html')

# @app.route("/testimonial",methods=['POST','GET'])
# def testimonial():
#     return render_template('testimonial.html')

# @app.route("/contact",methods=['POST','GET'])
# def contact():
#     return render_template('contact.html')

# if __name__=="__main__":
#     app.run(debug=True)
@app.route('/enter')
def home():
    return render_template('home.html')

@app.route('/freg')
def reg():
    return render_template('auth.html')

@app.route('/creg')
def reg1():
    return render_template('auth1.html')

@app.route('/flog')
def log():
    return render_template('auth.html')

@app.route('/clog')
def log1():
    return render_template('auth1.html')

@app.route('/slog')
def log2():
    info=bioIndus.find()
    data1=list(info)
    moksha=['Moksha Bio Energy Products','Vijayawada','+91 988 533 5864']
    indus=[]
    indus.append(moksha)
    for i in data1:
        dummy=[]
        dummy.append(i.get('name'))
        dummy.append(i.get('phno'))
        indus.append(dummy)
    return render_template('slogin.html',data=indus)

@app.route('/production')
def production():
    global loc
    return render_template('production.html')

@app.route('/selling')
def selling():
    return render_template('selling.html')

@app.route('/insurance')
def insurance():
    return render_template('insurance.html')

@app.route('/fregister',methods=['POST','GET'])
def register():
    name=request.form.get('name')
    age=request.form.get('age')
    # gender=request.form.get('gender')
    loc=request.form.get('loc')
    landm=request.form.get('landm')
    phno=request.form.get('phno')
    crop=request.form.get('crop')
    yof=request.form.get('yof')
    exis_user=userdata.find_one({'name':name,'phno':phno})
    if exis_user:
        msg="User already existed,Please create new user"
        return render_template('auth.html',msg=msg)
    else:
        user={'name':name,'age':age,'loc':loc,'landm':landm,'phno':phno,'crop':crop,'yof':yof}
        userdata.insert_one(user)
        msg="Registartion successful!!!"
        return render_template('auth.html',msg=msg)
    
@app.route('/flogin',methods=['POST','GET'])
def login():
    global loc
    global phno
    global name
    global crop
    name=request.form.get('name')
    phno=request.form.get('phno')
    user=userdata.find_one({'name':name,'phno':phno})
    if user!=None:
        loc=user['loc']
        phno=user['phno']
        name=user['name']
        crop=user['crop']
        session['username']=phno
        return redirect('/uhome')
    else:
        msg="Invalid details"
        return render_template('auth.html',msg=msg)

@app.route('/cregister',methods=['POST','GET'])
def register1():
    name=request.form.get('name')
    age=request.form.get('age')
    # gender=request.form.get('gender')
    loc=request.form.get('loc')
    landm=request.form.get('landm')
    phno=request.form.get('phno')
    exis_user=indiBuyers.find_one({'name':name,'phno':phno})
    if exis_user:
        msg="User already existed,Please create new user"
        return render_template('cregister.html',msg=msg)
    else:
        user={'name':name,'age':age,'loc':loc,'landm':landm,'phno':phno}
        indiBuyers.insert_one(user)
        msg="Registartion successful!!!"
        return render_template('auth1.html',msg=msg)

@app.route('/clogin',methods=['POST','GET'])
def login1():
    global cphno
    global cname
    name=request.form.get('name')
    phno=request.form.get('phno')
    # print(name,phno)
    user=indiBuyers.find_one({'name':name,'phno':phno})
    if user!=None:
        cphno=user['phno']
        cname=user['name']
        return redirect('/chome')
    else:
        msg="Invalid details"
        return render_template('auth1.html',msg=msg)

@app.route('/chome',methods=['POST','GET'])
def chome():
    global crop1
    print("name is:",cname)
    info1=urequests.find({'type':'indi','sname':cname})
    info=list(info1)
    # print(info[0]['cname'])
    if len(info)>0:
        crop1=info[0]['cname']
        return render_template('chome.html',data=info)
    else:
        return render_template('chome.html',msg="No requests found!!!")

@app.route('/cupstatus/<x>',methods=['POST','GET'])
def cupstatus(x):
    name2=x
    status="Accepted"
    urequests.update_one({'_id':ObjectId(name2)},{'$set':{'status':status}})
    return redirect('/chome')

@app.route('/report',methods=['POST','GET'])
def report():
    loc1=loc
    if loc1=="":
        loc1="guntur"
    print(loc1)
    if(loc1=="krishna"):
        loc1="vijayawada"
    url = 'https://api.openweathermap.org/data/2.5/weather?q={}&appid={}'.format(loc1,'5cc0112b7233c62b228f04428e2a2163')
    res = requests.get(url)
    data1 = res.json()
    temp1 = data1['main']['temp']
    gtemp=int(temp1-273.15)
    print(gtemp)
    try:
        response = requests.get(url)
        data = response.json()
        visibility = data['visibility']  # Visibility in meters
        cloudiness = data['clouds']['all']  # Cloud cover percentage
        light_intensity = int(visibility * (1 - cloudiness / 100)/10)
    except Exception as e:
        light_intensity = None
        print(f"Error: {e}")
    gli=light_intensity
    hum=data1['main']['humidity']
    info=[gtemp,gli,hum,crop1]
    # print(gtemp,gli,hum,crop)
    dcnt=10
    info.append(dcnt)
    mcnt=20
    info.append(mcnt)
    return render_template('report.html',data=info)

@app.route('/slogin',methods=['POST','GET'])
def login2():
    global sname
    sname=request.form.get('sname')
    return redirect('/shome')
    
@app.route('/shome',methods=['POST','GET'])
def shome():
    info1=urequests.find({'type':'stubble','sname':sname})
    info=list(info1)
    return render_template('shome.html',data=info)

@app.route('/upstatus/<x>',methods=['POST','GET'])
def upstatus(x):
    name2=x
    status="Accepted"
    urequests.update_one({'_id':ObjectId(name2)},{'$set':{'status':status}})
    return redirect('/shome')

@app.route('/uhome',methods=['POST','GET'])
def uhome():
    global loc
    print(crop)
    if(loc=="vijayawada"):
        loc="krishna"
    info=agroDealers.find({'loc':loc.lower()})
    data1=list(info)
    if len(data1)>0:
        dealers=[]
        for i in data1:
            dummy=[]
            dummy.append(i.get('name'))
            dummy.append(i.get('loc'))
            dummy.append(i.get('lm'))
            dummy.append(i.get('phno'))
            dealers.append(dummy)
        return render_template('uhome.html',data=dealers)
    else:
        msg="No shops found under your Location"
        return render_template('uhome.html',msg=msg)   

@app.route('/sdata')
def sdata():
    msg1=""
    global loc
    global gtemp
    global gli
    global hum
    # print(loc)
    if(loc=="krishna"):
        loc="vijayawada"
    url = 'https://api.openweathermap.org/data/2.5/weather?q={}&appid={}'.format(loc,'5cc0112b7233c62b228f04428e2a2163')
    res = requests.get(url)
    data1 = res.json()
    # if data1['cod'] == '404':
    #     msg1="City details not available"
    #     print("City not found")
        #remaining code keep in else
    temp = data1['main']['temp']
    temp1=int(temp-273.15)
    if temp1>=70:
        msg="It's too hot!!!"
    elif temp1<70:
        msg="It's fine"
    try:
        response = requests.get(url)
        data = response.json()
        visibility = data['visibility']  # Visibility in meters
        cloudiness = data['clouds']['all']  # Cloud cover percentage
        light_intensity = int(visibility * (1 - cloudiness / 100)/10)
    except Exception as e:
        light_intensity = None
        print(f"Error: {e}")
    API_KEY = '5cc0112b7233c62b228f04428e2a2163'
    url2 = f'http://api.openweathermap.org/geo/1.0/direct?q={loc}&limit=1&appid={API_KEY}'
    response1 = requests.get(url2)
    if response1.status_code == 200:
        data = response1.json()
        latitude = data[0]['lat']
        longitude = data[0]['lon']
        url1 = f'http://api.openweathermap.org/data/2.5/air_pollution?lat={latitude}&lon={longitude}&appid={API_KEY}'
        response = requests.get(url1)
        if response.status_code == 200:
            data = response.json()
            if 'list' in data:
                air_quality = data['list'][0]['main']['aqi']
                components=data['list'][0]['components']
                # print('Air Quality Index (AQI):', air_quality)
                # print('components:',data['list'][0]['components'])
            else:
                msg1='No air quality data available for the specified location.'
        else:
            msg1='Failed to fetch air quality data. Please check your API key and try again.'
    else:
        msg1='Failed to fetch city data. Please check your API key and try again.'
    gtemp=temp1
    gli=light_intensity
    hum=data1['main']['humidity']
    return render_template('sensor.html',data=data1,temp=temp1,msg=msg,msg1=msg1,li=light_intensity,aq=air_quality,com=components)

@app.route('/dis')
def dis():
    return render_template('disease.html')

@app.route('/disease', methods=['POST', 'GET'])
def disease():
    if request.method == 'POST':
        img = request.files['image']
        if img:
            img_path = "static/" + img.filename
            img.save(img_path)
            np.set_printoptions(suppress=True)
            model = load_model("keras_model.h5", compile=False)
            class_names = open("labels.txt", "r").readlines()
            data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
            image = Image.open(img).convert("RGB")
            size = (224, 224)
            image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)
            image_array = np.asarray(image)
            normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1
            data[0] = normalized_image_array
            prediction = model.predict(data)
            index = np.argmax(prediction)
            class_name = class_names[index]
            confidence_score = prediction[0][index]
            result = f"Class: {class_name[2:]}, Confidence Score: {confidence_score}"
            # print(result)
            reasons_index = result.find("Reasons=[")
            na=result[2:reasons_index-1]
            # print("name:",na)
            remedies_index = result.find("Remedies=[")
            if reasons_index != -1:
                reasons_end_index = result.find("]", reasons_index)
                reasons_str = result[reasons_index + len("Reasons=["):reasons_end_index]
                reasons = [reason.strip() for reason in reasons_str.split(",")]
            if remedies_index != -1:
                remedies_end_index = result.find("]", remedies_index)
                remedies_str = result[remedies_index + len("Remedies=["):remedies_end_index]
                remedies = [remedy.strip() for remedy in remedies_str.split(",")]
            # print("Reasons:", reasons)
            # print("Remedies:", remedies)
            return render_template('disease.html',na=na[5:],reasons=reasons,remedies=remedies,confidence_score=confidence_score,img=img_path)
        else:
            return render_template('disease.html', result="Image file not accepted")
    else:
        return render_template('disease.html', result=None)

@app.route('/toone',methods=['POST','GET'])
def toone():
    info=indiBuyers.find()
    data1=list(info)
    if len(data1)>0:
        dealers=[]
        for i in data1:
            dummy=[]
            dummy.append(i.get('name'))
            dummy.append(i.get('loc'))
            dummy.append(i.get('phno'))
            dealers.append(dummy)
        return render_template('indibuyers.html',data=dealers)
    else:
        msg="No Buyers found"
        return render_template('indibuyers.html',msg=msg)

@app.route('/sell1',methods=['POST','GET'])
def sell1():
    sname=request.form.get('item')
    cname1=request.form.get('cname')
    cquan1=request.form.get('cquan')
    type="indi"
    edate=str(datetime.now().day)+"/"+str(datetime.now().month)+"/"+str(datetime.now().year)
    exis_req=urequests.find_one({'sname':sname,'name':name,'cname':cname1})
    if exis_req:
        if exis_req['status']=="pending":
            return redirect('/toone')
    else:
        status="pending"
        new_req={'sname':sname,'name':name,'cname':cname1,'cquan':cquan1,'type':type,'date':edate,'status':status}
        urequests.insert_one(new_req)
        msg="Request sent successfully!!!"
        print(msg)
        return redirect('/toone')
    
@app.route('/cprofile',methods=['POST','GET'])
def cprofile():
    global cname
    global cphno
    name1=request.form.get('newName')
    age1=request.form.get('newAge')
    loc1=request.form.get('newLoc')
    lm1=request.form.get('newLm')
    ph1=request.form.get('newPh')
    if name1!=None and name1!="":
        indiBuyers.update_one({'phno':cphno},{'$set':{'name':name1}})
        cname=name1
        print("details updated")
    elif age1!=None and age1!="" :
        indiBuyers.update_one({'phno':cphno},{'$set':{'age':age1}})
        print("details updated")
    elif loc1!=None and loc1!="" :
        indiBuyers.update_one({'phno':cphno},{'$set':{'loc':loc1}})
        print("details updated")
    elif lm1!=None and lm1!="":
        indiBuyers.update_one({'phno':cphno},{'$set':{'landm':lm1}})
        print("details updated")
    elif ph1!=None and ph1!="":
        indiBuyers.update_one({'name':cname},{'$set':{'phno':ph1}})
        cphno=ph1
        print("details updated")
    else:
        data=indiBuyers.find({'phno':cphno,'name':cname})
        data1=list(data)
    data=indiBuyers.find({'phno':cphno,'name':cname})
    data1=list(data)
    print(name1,age1,loc1,lm1,ph1)
    return render_template('cprofile.html',data=data1)

@app.route('/crequests',methods=['POST','GET'])
def crequest1():
    info1=urequests.find({'type':'indi','name':name})
    info=list(info1)
    return render_template('crequests.html',data=info)

@app.route('/cupstatus1/<y>',methods=['POST','GET'])
def cupstatus1(y):
    name2=y
    urequests.delete_one({'_id':ObjectId(name2)})
    return redirect('/crequests')

@app.route('/toemart',methods=['POST','GET'])
def toemart():
    info=emarts.find()
    data1=list(info)
    if len(data1)>0:
        dealers=[]
        for i in data1:
            dummy=[]
            dummy.append(i.get('path'))
            dealers.append(dummy)
        return render_template('sellingm.html',data=dealers)
    else:
        msg="No platforms available"
        return render_template('sellingm.html',msg=msg)

@app.route('/tobidding',methods=['POST','GET'])
def tobidder():
    info=biddings.find()
    data1=list(info)
    if len(data1)>0:
        dealers=[]
        for i in data1:
            dummy=[]
            dummy.append(i.get('path'))
            dealers.append(dummy)
        return render_template('sellingm.html',data=dealers)
    else:
        msg="No platforms available"
        return render_template('sellingm.html',msg=msg)

@app.route('/stubble',methods=['POST','GET'])
def stubble():
    info=bioIndus.find()
    data1=list(info)
    moksha=['Moksha Bio Energy Products','Vijayawada','+91 988 533 5864']
    indus=[]
    indus.append(moksha)
    for i in data1:
        dummy=[]
        dummy.append(i.get('name'))
        dummy.append(i.get('loc'))
        dummy.append(i.get('phno'))
        indus.append(dummy)
    return render_template('stubble.html',data=indus,msg=msg1)
   
@app.route('/stubble1',methods=['POST','GET'])
def stubble1():
    global sname
    sname=request.form.get('item')
    cname=request.form.get('cname')
    cquan=request.form.get('cquan')
    type="stubble"
    edate=str(datetime.now().day)+"/"+str(datetime.now().month)+"/"+str(datetime.now().year)
    exis_req=urequests.find_one({'sname':sname,'name':name,'cname':cname})
    if exis_req:
        if exis_req['status']=="pending":
            return redirect('/stubble')
    else:
        status="pending"
        new_req={'sname':sname,'name':name,'cname':cname,'cquan':cquan,'type':type,'date':edate,'status':status}
        urequests.insert_one(new_req)
        msg="Request sent successfully!!!"
        return redirect('/stubble')

@app.route('/requests',methods=['POST','GET'])
def request1():
    info1=urequests.find({'type':'stubble','name':name})
    info=list(info1)
    return render_template('requests.html',data=info)

@app.route('/upstatus1/<y>',methods=['POST','GET'])
def upstatus1(y):
    name2=y
    urequests.delete_one({'_id':ObjectId(name2)})
    return redirect('/requests')

@app.route('/profile',methods=['POST','GET'])
def profile():
    global name
    global phno
    name1=request.form.get('newName')
    age1=request.form.get('newAge')
    loc1=request.form.get('newLoc')
    lm1=request.form.get('newLm')
    ph1=request.form.get('newPh')
    crop1=request.form.get('newCrop')
    if name1!=None and name1!="":
        userdata.update_one({'phno':phno},{'$set':{'name':name1}})
        name=name1
        print("details updated")
    elif age1!=None and age1!="" :
        userdata.update_one({'phno':phno},{'$set':{'age':age1}})
        print("details updated")
    elif loc1!=None and loc1!="" :
        userdata.update_one({'phno':phno},{'$set':{'loc':loc1}})
        print("details updated")
    elif lm1!=None and lm1!="":
        userdata.update_one({'phno':phno},{'$set':{'landm':lm1}})
        print("details updated")
    elif crop1!=None and crop1!="":
        userdata.update_one({'phno':phno},{'$set':{'crop':crop1}})
        print("details updated")
    elif ph1!=None and ph1!="":
        # print(name)
        userdata.update_one({'name':name},{'$set':{'phno':ph1}})
        phno=ph1
        print("details updated")
    else:
        data=userdata.find({'phno':phno,'name':name})
        data1=list(data)
    data=userdata.find({'phno':phno,'name':name})
    data1=list(data)
    print(name1,age1,loc1,lm1,ph1,crop1)
    return render_template('profile.html',data=data1)

@app.route('/storeselling',methods=['POST','GET'])
def storeselling():
    cname=request.form.get('cname')
    btype=request.form.get('btype')
    ename=request.form.get('ename')
    bdname=request.form.get('bdname')
    if ename=="":
        ename=bdname
    bname=request.form.get('bname')
    cquan=request.form.get('cquan')
    amt=request.form.get('amt')
    date=request.form.get('date')
    edate=str(datetime.now().day)+"/"+str(datetime.now().month)+"/"+str(datetime.now().year)
    type="selling"
    selldata={
        'name':name,
        'cname':cname,
        'btype':btype,
        'wname':ename,
        'bname':bname,
        'cquan':cquan,
        'amt':amt,
        'date':date,
        'edate':edate,
        'type':type
    }
    msg="Data Stored successful!!!"
    bdata=[name,cname,btype,ename,bname,cquan,amt,date,edate,type]
    # print("bdata:",bdata)
    if(cname==None):
        return render_template('storedata.html')
    bdata1=",".join(bdata)
    wallet="0x59392F3A77cf29dbe7Fd576288369a49c61FCd2B"
    web3.eth.defaultAccount=wallet
    artifact="../build/contracts/insertdata.json"
    with open(artifact,'r') as f:
        artifact_json=json.loads(f.read())
        contract_abi=artifact_json['abi'] 
        contract_address=artifact_json['networks']['5777']['address'] 
        contract=web3.eth.contract(
        abi=contract_abi,
        address=contract_address
    )
    tx_hash=contract.functions.store(bdata1).transact()
    web3.eth.waitForTransactionReceipt(tx_hash)
    negoData.insert_one(selldata)
    return render_template('selling.html',msg=msg)    

@app.route('/storestubble',methods=['POST','GET'])
def storestubble():
    sname=request.form.get('sname')
    iname=request.form.get('iname')
    bname=request.form.get('bname')
    squan=request.form.get('squan')
    amt=request.form.get('amt')
    date=request.form.get('date')
    edate=str(datetime.now().day)+"/"+str(datetime.now().month)+"/"+str(datetime.now().year)
    type="stubble"
    selldata={
        'name':name,
        'sname':sname,
        'iname':iname,
        'bname':bname,
        'squan':squan,
        'amt':amt,
        'date':date,
        'edate':edate,
        'type':type
    }
    msg="Data Stored successful!!!"
    bdata=[name,sname,iname,bname,squan,amt,date,edate,type]
    if(sname==None):
        return render_template('storedata.html')
    bdata1=",".join(bdata)
    wallet="0x59392F3A77cf29dbe7Fd576288369a49c61FCd2B"
    web3.eth.defaultAccount=wallet
    artifact="../build/contracts/insertdata.json"
    with open(artifact,'r') as f:
        artifact_json=json.loads(f.read())
        contract_abi=artifact_json['abi'] 
        contract_address=artifact_json['networks']['5777']['address'] 
        contract=web3.eth.contract(
        abi=contract_abi,
        address=contract_address
    )
    tx_hash=contract.functions.store(bdata1).transact()
    web3.eth.waitForTransactionReceipt(tx_hash)
    negoData.insert_one(selldata)
    return redirect('/stubble')    

@app.route('/storescheme',methods=['POST','GET'])
def storescheme():
    sname=request.form.get('sname')
    cname=request.form.get('cname')
    if sname=="":
        sname=cname
    stype=request.form.get('stype')
    apay=request.form.get('apay')
    date=request.form.get('date')
    edate=str(datetime.now().day)+"/"+str(datetime.now().month)+"/"+str(datetime.now().year)
    type="scheme"
    selldata={
        'name':name,
        'sname':sname,
        'stype':stype,
        'apay':apay,
        'date':date,
        'edate':edate,
        'type':type
    }
    msg="Data Stored successful!!!"
    bdata=[name,sname,stype,apay,date,edate,type]
    if(sname==None):
        return render_template('storedata.html')
    bdata1=",".join(bdata)
    wallet="0x59392F3A77cf29dbe7Fd576288369a49c61FCd2B"
    web3.eth.defaultAccount=wallet
    artifact="../build/contracts/insertdata.json"
    with open(artifact,'r') as f:
        artifact_json=json.loads(f.read())
        contract_abi=artifact_json['abi'] 
        contract_address=artifact_json['networks']['5777']['address'] 
        contract=web3.eth.contract(
        abi=contract_abi,
        address=contract_address
    )
    tx_hash=contract.functions.store(bdata1).transact()
    web3.eth.waitForTransactionReceipt(tx_hash)
    negoData.insert_one(selldata)
    return render_template('insurance.html',msg=msg)  

@app.route('/showselling',methods=['POST','GET'])
def showselling():
    info=negoData.find({'name':name,'type':"selling"})
    data1=list(info)
    if len(data1)>0:
        data=[]
        for i in data1:
            dummy=[]
            dummy.append(i.get('cname'))
            dummy.append(i.get('btype'))
            dummy.append(i.get('bname'))
            dummy.append(i.get('cquan'))
            dummy.append(i.get('amt'))
            dummy.append(i.get('date'))
            dummy.append(i.get('edate'))
            data.append(dummy)
        return render_template('showdata.html',data=data)
    else:
        msg="No transactions till now!!!"
        return render_template('selling.html',msg=msg)

@app.route('/showstubble',methods=['POST','GET'])
def showstubble():
    global msg1
    info=negoData.find({'name':name,'type':"stubble"})
    data1=list(info)
    if len(data1)>0:
        stdata=[]
        for i in data1:
            dummy=[]
            dummy.append(i.get('sname'))
            dummy.append(i.get('iname'))
            dummy.append(i.get('bname'))
            dummy.append(i.get('squan'))
            dummy.append(i.get('amt'))
            dummy.append(i.get('date'))
            dummy.append(i.get('edate'))
            stdata.append(dummy)
        return render_template('showdata.html',data=stdata)
    else:
        msg1="No transactions available!!!"
        return redirect('/stubble')

@app.route('/showscheme',methods=['POST','GET'])
def showscheme():
    info=negoData.find({'name':name,'type':"scheme"})
    data1=list(info)
    if len(data1)>0:
        data=[]
        for i in data1:
            dummy=[]
            dummy.append(i.get('sname'))
            dummy.append(i.get('stype'))
            dummy.append(i.get('apay'))
            dummy.append(i.get('date'))
            dummy.append(i.get('edate'))
            data.append(dummy)
        return render_template('showdata.html',data=data)
    else:
        msg="No transactions till now!!!"
        return render_template('insurance.html',msg=msg)

def readDataFromThingSpeak1(channelid=2457233):
    http = urllib3.PoolManager()
    response = http.request('GET', 'https://api.thingspeak.com/channels/' + str(channelid) + '/feeds.json?results=8000')
    response = response.data
    response = response.decode('utf-8')
    response = json.loads(response)
    feeds = response['feeds']
    return feeds
@app.route('/irrigation',methods=['POST','GET'])
def irrigation():
    datafile=readDataFromThingSpeak1()
    data=[]
    for i in datafile:
        # print(i)
        created_at = i['created_at']
        parsed_time = datetime.strptime(created_at, '%Y-%m-%dT%H:%M:%SZ')
        date = parsed_time.date().strftime('%Y-%m-%d')
        time = parsed_time.time().strftime('%H:%M:%S')
        entry_id = int(i['entry_id'])
        field1 = int(i['field1'])
        field2 = int(i['field2'])
        if i['field3']!=None:
            field3 = int(i['field3'])
        else:
            field3=None
        # print(field3)
        result_list = [entry_id, date, time, field1, field2, field3]
        msg = ''
        if field1 > 700:
            msg += 'Soil is too wet. '
        elif field1 < 200:
            msg += 'Soil is too dry. '
        if field2 == 0:
            msg += 'Motor is off. '
        else:
            msg += 'Motor is on. '
        if field3 == 0 or field3==None:
            msg += 'Light is off. '
        else:
            msg += 'Light is on. '
        result_list.append(msg)
        # print(result_list)
        data.append(result_list)        
    return render_template('irrigation.html',data=data)

@app.route('/logout')
def logout():
    session.pop('username',None)
    return redirect('/enter')

@app.route('/exit')
def logout1():
    session.pop('username',None)
    return redirect('/')

if __name__=="__main__":
    app.run(debug=True,host='0.0.0.0')