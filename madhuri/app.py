from flask import Flask, render_template, redirect, url_for, session, g, jsonify, json
from flask_bcrypt import Bcrypt
from werkzeug.security import generate_password_hash, \
    check_password_hash
import mysql.connector
from datetime import datetime
from flask import request
from flask import jsonify
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)
bcrypt = Bcrypt(app)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':

        session.pop('user', None)
        db = mysql.connector.connect(user='root', password='admin', host='localhost', database='animal')
        cursor = db.cursor()
        user = request.form['username']
        cursor.execute('SELECT * FROM user WHERE username = %s', [user])
        records = cursor.fetchall()

        if records:
            # if bcrypt.hashpw(request.form['pass'].encode('utf-8'),records['password'].encode('utf-8'))==records['password'].encode('utf-8'):
            #     session['username']=request.form['username']
            v = (check_password_hash(records[0][5], request.form['password']))
            if v == True:
                session['user'] = request.form['username']
                return redirect(url_for('home'))
                # return redirect(url_for('home'))

    return render_template('login1.html')


@app.route('/home')
def home():
    # if g.user:
    return render_template('index.html')


@app.route('/')
def index():
    return render_template('login1.html')


# logout
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))


@app.route('/inci')
def inci():
    return render_template('incident.html')


@app.route('/form')
def form():
    return render_template('form-elements-component.html')


@app.route("/color")
def color():
    db = mysql.connector.connect(user='root', password='admin', host='localhost', database='animal')
    cursor = db.cursor()
    query = "SELECT * FROM master__color"
    cursor.execute(query)
    records = cursor.fetchall()
    db.commit()
    db.close()
    return render_template('colormaster.html', values=records)


@app.route("/createc", methods=['post'])
def createc():
    db = mysql.connector.connect(user='root', password='admin', host='localhost', database='animal')
    cursor = db.cursor()
    color = request.form['type_of_color']  # from from
    description = request.form['description']
    query = "INSERT INTO  master__color(color,description) VALUES(%s,%s)"  # from database
    cursor.execute(query, (color, description))
    db.commit()
    db.close()
    return redirect(url_for('color'))


@app.route("/updatec", methods=['POST'])
def updatec():
    db = mysql.connector.connect(user='root', password='admin', host='localhost', database='animal')
    cursor = db.cursor()
    sid = request.form['color_id']
    color = request.form['type_of_color']
    description = request.form['description']
    query = "UPDATE master__color SET color=%s , description=%s WHERE id=%s"
    cursor.execute(query, (color, description, sid))
    db.commit()
    cursor.close()
    db.close()
    return redirect(url_for('color'))


@app.route("/deletec", methods=['POST'])
def deletec():
    db = mysql.connector.connect(user='root', password='admin', host='localhost', database='animal')
    cursor = db.cursor()
    sid = request.form['color2_id']
    cursor.execute('DELETE FROM  master__color WHERE id = %s', [request.form['color2_id']])
    db.commit()
    cursor.close()
    db.close()
    return redirect(url_for('color'))


# breed master
@app.route("/breed")
def breed():
    db = mysql.connector.connect(user='root', password='admin', host='localhost', database='animal')
    cursor = db.cursor()
    query = "SELECT * FROM master__breed"
    cursor.execute(query)
    records = cursor.fetchall()
    db.commit()
    db.close()
    return render_template('breed.html', values=records)


@app.route("/createb", methods=['post'])
def createb():
    db = mysql.connector.connect(user='root', password='admin', host='localhost', database='animal')
    cursor = db.cursor()
    breed = request.form['breed']  # from from
    description = request.form['description']
    query = "INSERT INTO  master__breed(breed,description) VALUES(%s,%s)"  # from database
    cursor.execute(query, (breed, description))
    db.commit()
    db.close()
    return redirect(url_for('breed'))


@app.route("/updateb", methods=['POST'])
def updateb():
    db = mysql.connector.connect(user='root', password='admin', host='localhost', database='animal')
    cursor = db.cursor()
    sid = request.form['breed_id']
    breed = request.form['breed']
    description = request.form['description']
    query = "UPDATE master__breed SET breed=%s , description=%s WHERE id=%s"
    cursor.execute(query, (breed, description, sid))
    db.commit()
    cursor.close()
    db.close()
    return redirect(url_for('breed'))


@app.route("/deleteb", methods=['POST'])
def deleteb():
    db = mysql.connector.connect(user='root', password='admin', host='localhost', database='animal')
    cursor = db.cursor()
    sid = request.form['breed2_id']
    cursor.execute('DELETE FROM  master__breed WHERE id = %s', [request.form['breed2_id']])
    db.commit()
    cursor.close()
    db.close()
    return redirect(url_for('breed'))


# vaccinemaster
@app.route("/vaccine")
def vaccine():
    db = mysql.connector.connect(user='root', password='admin', host='localhost', database='animal')
    cursor = db.cursor()
    query = "SELECT * FROM master__vaccination"
    cursor.execute(query)
    records = cursor.fetchall()
    db.commit()
    db.close()
    return render_template('vaccinemaster.html', values=records)


# FOR CREATING THE ROWS
@app.route("/createvaccine", methods=['post'])
def createvaccine():
    db = mysql.connector.connect(user='root', password='admin', host='localhost', database='animal')
    cursor = db.cursor()
    types = request.form['type_of_vaccination']
    description = request.form['description']
    query = "INSERT INTO master__vaccination(type,description) VALUES(%s,%s)"
    cursor.execute(query, (types, description))
    # cursor.execute(sql)
    db.commit()
    db.close()
    return redirect(url_for('vaccine'))


# FOR UPDATING THE ROWS
@app.route("/updatevaccine", methods=['POST'])
def updatevaccine():
    db = mysql.connector.connect(user='root', password='admin', host='localhost', database='animal')
    cursor = db.cursor()
    vid = request.form['vaccine_id']
    types = request.form['type_of_vaccination']
    description = request.form['description']
    query = "UPDATE master__vaccination SET type=%s , description=%s WHERE id=%s"
    cursor.execute(query, (types, description, vid))
    db.commit()
    cursor.close()
    db.close()
    return redirect(url_for('vaccine'))


# FOR DELETEING THE ROWS
@app.route("/delete", methods=['POST'])
def delete():
    db = mysql.connector.connect(user='root', password='admin', host='localhost', database='animal')
    cursor = db.cursor()
    vid = request.form['vacc_id']
    cursor.execute('DELETE FROM master__vaccination WHERE id = %s', [request.form['vacc_id']])
    db.commit()
    cursor.close()
    db.close()
    return redirect(url_for('vaccine'))


# Food
@app.route("/food")
def food():
    db = mysql.connector.connect(user='root', password='admin', host='localhost', database='animal')
    cursor = db.cursor()
    query = "SELECT master__food.id,  master__food.name, master__species.species FROM master__food INNER JOIN  master__species ON master__food.species_id=master__species.id"
    query1 = "SELECT * FROM master__species"
    cursor.execute(query)
    records = cursor.fetchall()
    cursor.execute(query1)
    records1 = cursor.fetchall()
    db.commit()
    db.close()
    return render_template('food.html', values=records, values1=records1)


@app.route("/createf", methods=['post'])
def createf():
    db = mysql.connector.connect(user='root', password='admin', host='localhost', database='animal')
    cursor = db.cursor()
    food = request.form['type_of_food']  # from from
    species = request.form['species_id']
    query = "INSERT INTO  master__food(name,species_id) VALUES(%s,%s)"  # from database
    cursor.execute(query, (food, species))
    db.commit()
    db.close()
    return redirect(url_for('food'))


@app.route("/updatef", methods=['POST'])
def updatef():
    db = mysql.connector.connect(user='root', password='admin', host='localhost', database='animal')
    cursor = db.cursor()
    sid = request.form['food_id']
    # return sid
    food = request.form['type_of_food']
    species = request.form['species_id']
    query = "UPDATE master__food SET name=%s , species_id=%s WHERE id=%s"
    cursor.execute(query, (food, species, sid))
    db.commit()
    cursor.close()
    db.close()
    return redirect(url_for('food'))


@app.route("/deletef", methods=['POST'])
def deletef():
    db = mysql.connector.connect(user='root', password='admin', host='localhost', database='animal')
    cursor = db.cursor()
    sid = request.form['food2_id']
    cursor.execute('DELETE FROM  master__food WHERE id = %s', [request.form['food2_id']])
    db.commit()
    cursor.close()
    db.close()
    return redirect(url_for('food'))


# TEST
@app.route("/test")
def test():
    db = mysql.connector.connect(user='root', password='admin', host='localhost', database='animal')
    cursor = db.cursor()
    query = "SELECT * FROM master__test"
    cursor.execute(query)
    records = cursor.fetchall()
    db.commit()
    db.close()
    return render_template('testmaster.html', values=records)


# FOR CREATING THE ROWS
@app.route("/createtest", methods=['post'])
def createtest():
    db = mysql.connector.connect(user='root', password='admin', host='localhost', database='animal')
    cursor = db.cursor()
    types = request.form['type_of_test']  # from from
    description = request.form['description']
    query = "INSERT INTO master__test(type,description) VALUES(%s,%s)"  # from database
    cursor.execute(query, (types, description))
    db.commit()
    db.close()
    return redirect(url_for('test'))


# FOR UPDATING THE ROWS
@app.route("/updatetest", methods=['POST'])
def updatetest():
    db = mysql.connector.connect(user='root', password='admin', host='localhost', database='animal')
    cursor = db.cursor()
    tid = request.form['test_id']
    types = request.form['type_of_test']
    description = request.form['description']
    query = "UPDATE master__test SET type=%s , description=%s WHERE id=%s"
    cursor.execute(query, (types, description, tid))
    db.commit()
    cursor.close()
    db.close()
    return redirect(url_for('test'))


# FOR DELETEING THE ROWS
@app.route("/deletet", methods=['POST'])
def deletet():
    db = mysql.connector.connect(user='root', password='admin', host='localhost', database='animal')
    cursor = db.cursor()
    tid = request.form['tes_id']
    cursor.execute('DELETE FROM master__test WHERE id = %s', [request.form['tes_id']])
    db.commit()
    cursor.close()
    db.close()
    return redirect(url_for('test'))


# species
@app.route("/species")
def species():
    db = mysql.connector.connect(user='root', password='admin', host='localhost', database='animal')
    cursor = db.cursor()
    query = "SELECT * FROM  master__species"
    cursor.execute(query)
    records = cursor.fetchall()
    db.commit()
    db.close()
    return render_template('speciesmaster.html', values=records)


# FOR CREATING THE ROWS
@app.route("/createspec", methods=['post'])
def createspec():
    db = mysql.connector.connect(user='root', password='admin', host='localhost', database='animal')
    cursor = db.cursor()
    types = request.form['type_of_species']  # from from
    description = request.form['description']
    query = "INSERT INTO  master__species(species,description) VALUES(%s,%s)"  # from database
    cursor.execute(query, (types, description))
    db.commit()
    db.close()
    return redirect(url_for('species'))


# FOR UPDATING THE ROWS
@app.route("/updatespec", methods=['POST'])
def updatespec():
    db = mysql.connector.connect(user='root', password='admin', host='localhost', database='animal')
    cursor = db.cursor()
    sid = request.form['species_id']
    types = request.form['type_of_species']
    description = request.form['description']
    query = "UPDATE master__species SET species=%s , description=%s WHERE id=%s"
    cursor.execute(query, (types, description, sid))
    db.commit()
    cursor.close()
    db.close()
    return redirect(url_for('species'))


# FOR DELETEING THE ROWS
@app.route("/deletes", methods=['POST'])
def deletes():
    db = mysql.connector.connect(user='root', password='admin', host='localhost', database='animal')
    cursor = db.cursor()
    sid = request.form['spec_id']
    cursor.execute('DELETE FROM  master__species WHERE id = %s', [request.form['spec_id']])
    db.commit()
    cursor.close()
    db.close()
    return redirect(url_for('species'))


# size
@app.route("/size")
def size():
    db = mysql.connector.connect(user='root', password='admin', host='localhost', database='animal')
    cursor = db.cursor()
    query = "SELECT * FROM master__size"
    cursor.execute(query)
    records = cursor.fetchall()
    db.commit()
    db.close()
    return render_template('sizemaster.html', values=records)


# FOR CREATING THE ROWS
@app.route("/createsize", methods=['post'])
def createsize():
    db = mysql.connector.connect(user='root', password='admin', host='localhost', database='animal')
    cursor = db.cursor()
    size = request.form['size']  # from from
    description = request.form['description']
    query = "INSERT INTO  master__size(size,description) VALUES(%s,%s)"  # from database
    cursor.execute(query, (size, description))

    db.commit()
    db.close()
    return redirect(url_for('size'))


# FOR UPDATING THE ROWS
@app.route("/updatesize", methods=['POST'])
def updatesize():
    db = mysql.connector.connect(user='root', password='admin', host='localhost', database='animal')
    cursor = db.cursor()
    sid = request.form['size_id']
    size = request.form['size']
    description = request.form['description']
    query = "UPDATE master__size SET size=%s , description=%s WHERE id=%s"
    cursor.execute(query, (size, description, sid))
    db.commit()
    cursor.close()
    db.close()
    return redirect(url_for('size'))


# FOR DELETEING THE ROWS
@app.route("/deletesi", methods=['POST'])
def deletesi():
    db = mysql.connector.connect(user='root', password='admin', host='localhost', database='animal')
    cursor = db.cursor()
    sid = request.form['size1_id']
    cursor.execute('DELETE FROM  master__size WHERE id = %s', [request.form['size1_id']])
    db.commit()
    cursor.close()
    db.close()
    return redirect(url_for('size'))


# hair
@app.route("/hair")
def hair():
    db = mysql.connector.connect(user='root', password='admin', host='localhost', database='animal')
    cursor = db.cursor()
    query = "SELECT * FROM master__hair"
    cursor.execute(query)
    records = cursor.fetchall()
    db.commit()
    db.close()
    return render_template('hairmaster.html', values=records)


@app.route("/createha", methods=['post'])
def createha():
    db = mysql.connector.connect(user='root', password='admin', host='localhost', database='animal')
    cursor = db.cursor()
    hair = request.form['type_of_hair']  # from from
    description = request.form['description']
    query = "INSERT INTO  master__hair(hair,description) VALUES(%s,%s)"  # from database
    cursor.execute(query, (hair, description))
    db.commit()
    db.close()
    return redirect(url_for('hair'))


@app.route("/updateha", methods=['POST'])
def updateha():
    db = mysql.connector.connect(user='root', password='admin', host='localhost', database='animal')
    cursor = db.cursor()
    sid = request.form['hair_id']
    print(request.form['hair_id'])
    hair = request.form['type_of_hair']
    description = request.form['description']
    query = "UPDATE master__hair SET hair=%s , description=%s WHERE id=%s"
    cursor.execute(query, (hair, description, sid))
    db.commit()
    cursor.close()
    db.close()
    return redirect(url_for('hair'))


@app.route("/deleteh", methods=['POST'])
def deleteh():
    db = mysql.connector.connect(user='root', password='admin', host='localhost', database='animal')
    cursor = db.cursor()
    sid = request.form['hair2_id']
    cursor.execute('DELETE FROM  master__hair WHERE id = %s', [request.form['hair2_id']])
    db.commit()
    cursor.close()
    db.close()
    return redirect(url_for('hair'))


# incident
@app.route("/incident")
def incident():
    db = mysql.connector.connect(user='root', password='admin', host='localhost', database='animal')
    cursor = db.cursor()
    query = "SELECT * FROM master__incident"
    cursor.execute(query)
    records = cursor.fetchall()
    db.commit()
    db.close()
    return render_template('incidentmaster.html', values=records)


@app.route("/createinci", methods=['post'])
def createinci():
    db = mysql.connector.connect(user='root', password='admin', host='localhost', database='animal')
    cursor = db.cursor()
    incident = request.form['type_of_incident']  # from from
    description = request.form['description']
    query = "INSERT INTO  master__incident(incident,description) VALUES(%s,%s)"  # from database
    cursor.execute(query, (incident, description))
    db.commit()
    db.close()
    return redirect(url_for('incident'))


@app.route("/updateinci", methods=['POST'])
def updateinci():
    db = mysql.connector.connect(user='root', password='admin', host='localhost', database='animal')
    cursor = db.cursor()
    sid = request.form['incident_id']
    incident = request.form['type_of_incident']
    description = request.form['description']
    query = "UPDATE master__incident SET incident=%s , description=%s WHERE id=%s"
    cursor.execute(query, (incident, description, sid))
    db.commit()
    cursor.close()
    db.close()
    return redirect(url_for('incident'))


@app.route("/deletei", methods=['POST'])
def deletei():
    db = mysql.connector.connect(user='root', password='admin', host='localhost', database='animal')
    cursor = db.cursor()
    sid = request.form['inci1_id']
    cursor.execute('DELETE FROM  master__incident WHERE id = %s', [request.form['inci1_id']])
    db.commit()
    cursor.close()
    db.close()
    return redirect(url_for('incident'))


# Pet
@app.route("/pet", methods=['GET', 'POST'])
def pet():
    db = mysql.connector.connect(user='root', password='admin', host='localhost', database='animal')
    cursor = db.cursor()
    query = "SELECT id,species FROM master__species"
    query1 = "SELECT id,breed FROM master__breed"
    query2 = "SELECT id,size FROM master__size"
    query3 = "SELECT id,hair FROM master__hair"
    query4 = "SELECT id,color FROM master__color"
    query5 = "SELECT * FROM medicare__animal"
    query6 = "SELECT * FROM medicare__client"
    cursor.execute(query)
    records = cursor.fetchall()
    cursor.execute(query1)
    records1 = cursor.fetchall()
    cursor.execute(query2)
    records2 = cursor.fetchall()
    cursor.execute(query3)
    records3 = cursor.fetchall()
    cursor.execute(query4)
    records4 = cursor.fetchall()
    cursor.execute(query5)
    records5 = cursor.fetchall()
    cursor.execute(query6)
    records6 = cursor.fetchall()
    cursor.execute("SELECT medicare__animal.id ,medicare__animal.animal_name,master__breed.breed,master__hair.hair,master__color.color,medicare__animal.date_of_birth,medicare__animal.licence_no,master__species.species,master__size.size,medicare__animal.sex_id,medicare__animal.last_vaccine,medicare__animal.id FROM ((medicare__animal INNER JOIN master__species ON medicare__animal.species_id = master__species.id)  INNER JOIN master__breed ON medicare__animal.breed_id = master__breed.id INNER JOIN master__hair ON medicare__animal.hair_id = master__hair.id INNER JOIN master__color ON medicare__animal.color_id = master__color.id INNER JOIN master__size ON medicare__animal.size_id = master__size.id)")
    records7 = cursor.fetchall()
    # print (records6)
    db.commit()
    db.close()
    return render_template('pet.html', values=records, values1=records1, values2=records2, values3=records3,
                           values4=records4, values5=records5, values6=records6, values7=records7)


@app.route("/peti", methods=['GET', 'POST'])
def peti():
    if request.method == 'GET':
        return render_template('pet.html')
    else:
        db = mysql.connector.connect(user='root', password='admin', host='localhost', database='animal')
        cursor = db.cursor()
        name = request.form['pet_name']
        breed = request.form['breed_name']  # from from
        hair = request.form['hair_name']
        color = request.form['color_name']
        licence = request.form['licence_name']
        species = request.form['sepcies_name']
        size = request.form['size_name']
        sex = request.form['sex']
        vaccine = request.form['vacc']
        color = request.form['color_name']
        clientId = request.form['client_id']
        dates = request.form['date']
        date = datetime.strptime(dates, '%m/%d/%Y')
        query = "INSERT INTO medicare__animal(animal_name,breed_id,hair_id,color_id,licence_no,species_id,size_id,sex_id,last_vaccine,date_of_birth,client_id) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"  # from database
        cursor.execute(query, (name, breed, hair, color, licence, species, size, sex, vaccine, date, clientId))
        db.commit()
        db.close()
        return redirect(url_for('pet'))


@app.route("/updatepet", methods=['GET', 'POST'])
def updatepet():
    if request.method == 'GET':
        return render_template('pet.html')
    else:
        db = mysql.connector.connect(user='root', password='admin', host='localhost', database='animal')
        cursor = db.cursor()
        sid = request.form['peti_id']
        name = request.form['pet_name']
        breed = request.form['breed_name']  # from from
        hair = request.form['hair_name']
        color = request.form['color_name']
        licence = request.form['licence_name']
        species = request.form['sepcies_name']
        size = request.form['size_name']
        sex = request.form['sex']
        vaccine = request.form['vacc']
        color = request.form['color_name']
        clientId = request.form['client_id']
        dates = request.form['date']
        date = datetime.strptime(dates, '%m/%d/%Y')
        query = "UPDATE medicare__animal SET animal_name=%s,date_of_birth=%s, breed_id=%s,hair_id=%s,color_id=%s,last_vaccine=%s,licence_no=%s,size_id=%s,sex_id=%s WHERE id=%s"
        cursor.execute(query, (name, date, breed, hair, color, vaccine, licence, size, sex, sid))
        db.commit()
        cursor.close()
        db.close()
        return redirect(url_for('pet'))


@app.route("/deletepet", methods=['POST'])
def deletepet():
    db = mysql.connector.connect(user='root', password='admin', host='localhost', database='animal')
    cursor = db.cursor()
    sid = request.form['pet_id']
    cursor.execute('DELETE FROM  medicare__animal WHERE id = %s', [request.form['pet_id']])
    db.commit()
    cursor.close()
    db.close()
    return redirect(url_for('pet'))


# Userindex
@app.route("/user", methods=['GET', 'POST'])
def user():
    db = mysql.connector.connect(user='root', password='admin', host='localhost', database='animal')
    cursor = db.cursor()
    query = "SELECT id,first_name,last_name,username,email_id FROM user"
    cursor.execute(query)
    records = cursor.fetchall()
    print(records)
    db.commit()
    db.close()
    return render_template('user.html', values=records)


@app.route("/useri", methods=['GET', 'POST'])
def useri():
    if request.method == 'GET':
        return render_template('user.html')
    else:
        db = mysql.connector.connect(user='root', password='admin', host='localhost', database='animal')
        cursor = db.cursor()
        first = request.form['first_Name']
        last = request.form['last_Name']  # from from
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        cpassword = request.form['cpassword']
        pw_hash = generate_password_hash(password)
        query = "INSERT INTO  user(first_name,last_name,email_id,username,password,confirm_password) VALUES(%s,%s,%s,%s,%s,%s)"  # from database
        cursor.execute(query, (first, last, email, username, pw_hash, pw_hash))
        db.commit()
        db.close()
        return redirect(url_for('user'))


@app.route("/updateuseri", methods=['GET', 'POST'])
def updateuseri():
    if request.method == 'GET':
        return render_template('user.html')
    else:
        db = mysql.connector.connect(user='root', password='admin', host='localhost', database='animal')
        cursor = db.cursor()
        uid = request.form['usere_id']
        name = request.form['first_Name']
        last = request.form['last_Name']
        mail = request.form['email']
        username = request.form['username']
        query = "UPDATE user SET first_name=%s,last_name=%s, email_id=%s,username=%s WHERE id=%s"
        cursor.execute(query, (name, last, mail, username, uid))
        db.commit()
        cursor.close()
        db.close()
        return redirect(url_for('user'))


@app.route("/deleteuser", methods=['POST'])
def deleteuser():
    db = mysql.connector.connect(user='root', password='admin', host='localhost', database='animal')
    cursor = db.cursor()
    sid = request.form['user_id']
    cursor.execute('DELETE FROM  user WHERE id = %s', [request.form['user_id']])
    db.commit()
    cursor.close()
    db.close()
    return redirect(url_for('user'))


# Compunder
@app.route("/compunder")
def compunder():
    db = mysql.connector.connect(user='root', password='admin', host='localhost', database='animal')
    cursor = db.cursor()
    query1 = "SELECT * FROM countries"
    query2 = "SELECT id,name FROM states"
    query3 = "SELECT id,name FROM cities"
    query4="SELECT id, first_name,last_name,email_id,mobile_no from compunder"
    cursor.execute(query1)
    records = cursor.fetchall()
    cursor.execute(query2)
    records1 = cursor.fetchall()
    cursor.execute(query3)
    records2 = cursor.fetchall()
    cursor.execute(query4)
    records3 = cursor.fetchall()
    return render_template('compunder.html', values=records, values1=records1, values2=records2, values3=records3)


@app.route("/updatecomp", methods=['GET', 'POST'])
def updatecomp():
    db = mysql.connector.connect(user='root', password='admin', host='localhost', database='animal')
    cursor = db.cursor()
    first = request.form['last_Name']
    last = request.form['last_Name']
    address = request.form['Address']
    city = request.form['city']
    state = request.form['state']
    country = request.form['country']
    zipcode = request.form['zip']
    email = request.form['email']
    phn = request.form['phone']
    mob = request.form['mobile']
    adhar = request.form['adhar']
    dob = request.form['date']
    query = "INSERT INTO compunder(first_name,last_name,address,city_id,state_id,country_id,email_id,phone_no,mobile_no,zipcode,adhar_no,dateofbirth) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    cursor.execute(query, (first, last, address, city, state, country, email, phn, mob, zipcode, adhar, dob))
    db.commit()
    db.close()
    return redirect(url_for('compunder'))


@app.route("/updatecompunder", methods=['GET', 'POST'])
def updatecompunder():
    if request.method == 'GET':
        return render_template('compunder.html')
    else:
        db = mysql.connector.connect(user='root', password='admin', host='localhost', database='animal')
        cursor = db.cursor()
        uid = request.form['user_id']
        name = request.form['first_name']
        last = request.form['last_name']
        phone = request.form['phone']
        mail = request.form['email']
        query = "UPDATE compunder SET first_name=%s,last_name=%s,phone=%s, email_id=%s WHERE id=%s"
        cursor.execute(query, (name, last, phone, mail, uid))
        db.commit()
        cursor.close()
        db.close()
        return redirect(url_for('compunder'))


@app.route("/deletecomp", methods=['POST'])
def deletecomp():
    db = mysql.connector.connect(user='root', password='admin', host='localhost', database='animal')
    cursor = db.cursor()
    sid = request.form['comp_id']
    cursor.execute('DELETE FROM  compunder WHERE id = %s', [request.form['comp_id']])
    db.commit()
    cursor.close()
    db.close()
    return redirect(url_for('compunder'))


# Clientindex
@app.route("/client")
def client():
    db = mysql.connector.connect(user='root', password='admin', host='localhost', database='animal')
    cursor = db.cursor()
    query = "SELECT id,first_name,last_name,mobile_no,email_id FROM medicare__client"
    query1="SELECT * FROM countries"
    query2 = "SELECT id,name FROM states"
    query3 = "SELECT id,name FROM cities"
    cursor.execute(query)
    records = cursor.fetchall()
    cursor.execute(query1)
    records1 = cursor.fetchall()
    cursor.execute(query2)
    records2 = cursor.fetchall()
    cursor.execute(query3)
    records3 = cursor.fetchall()
    return render_template('client.html', values=records,values1=records1,values2=records2,values3=records3)


@app.route("/incer", methods=['post'])
def incer():
    db = mysql.connector.connect(user='root', password='admin', host='localhost', database='animal')
    cursor = db.cursor()
    first = request.form['first_Namusere']
    last = request.form['last_Name']
    address = request.form['Address']
    city = request.form['city']
    state=request.form['state']
    country=request.form['country']
    zipcode = request.form['zip']
    email = request.form['email']
    mob = request.form['phone']
    adhar = request.form['adhar']
    dob = request.form['date']
    query = "INSERT INTO medicare__client(first_name,last_name,address,city_id,email_id,mobile_no,zipcode,adhar_no,dateofbirth,state_id,country_id) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    cursor.execute(query, (first, last, address, city, email, mob, zipcode, adhar, dob,state,country))
    db.commit()
    db.close()
    return redirect(url_for('client'))


@app.route("/clientup",methods=['GET', 'POST'])
def clientup():
    if request.method == 'GET':
        return render_template('client.html')
    else:
        db = mysql.connector.connect(user='root', password='admin', host='localhost', database='animal')
        cursor = db.cursor()
        sid = request.form['clie_id']
        first = request.form['first_Name']
        last = request.form['last_Name']
        email = request.form['email']
        mob = request.form['phone']
        query = "UPDATE medicare__client SET first_name=%s,last_name=%s,email_id=%s,mobile_no=%s WHERE id=%s"
        cursor.execute(query, (first, last, email, mob, sid))
        db.commit()
        cursor.close()
        db.close()
        return redirect(url_for('client'))

@app.route("/deleteclient", methods=['POST'])
def deleteclient():
    db = mysql.connector.connect(user='root', password='admin', host='localhost', database='animal')
    cursor = db.cursor()
    sid = request.form['client_id']
    cursor.execute('DELETE FROM  medicare__client WHERE id = %s', [request.form['client_id']])
    db.commit()
    cursor.close()
    db.close()
    return redirect(url_for('client'))


# Birth
@app.route("/birth")
def birth():
    db = mysql.connector.connect(user='root', password='admin', host='localhost', database='animal')
    cursor = db.cursor()
    query = "SELECT * FROM medicare__animal"
    query1 = "SELECT * FROM medicare__client"
    query2 = "SELECT * FROM cities"
    cursor.execute(query)
    records = cursor.fetchall()
    cursor.execute(query1)
    records1 = cursor.fetchall()
    cursor.execute(query2)
    records2 = cursor.fetchall()
    return render_template('birth.html', values=records, values1=records1,values2=records2)


@app.route("/insertb", methods=['GET','POST'])
def insertb():
    if request.method == 'GET':
        return render_template('birth.html')
    else:
        db = mysql.connector.connect(user='root', password='admin', host='localhost', database='animal')
        cursor = db.cursor()
        animal = request.form['species_id']
        city = request.form['city']  # from from
        dates = request.form['date']
        date = datetime.strptime(dates, '%m/%d/%Y')
        lbs = request.form['lbsa']
        owner = request.form['owner']
        time = request.form['time']
        weighta = request.form['weighta']
        mail = request.form['email']
        address = request.form['address']
        phone = request.form['phone']
        dname = request.form['dname']
        daddress = request.form['daddress']
        hname = request.form['hname']
        demail = request.form['demail']
        dphone = request.form['dphone']
        query = "INSERT INTO  medicare__birth(animal_id,city_id,date_of_birth,weight,lbs,time_of_birth,user_id,address1,phone_no,email,doctor_name,hospital_name,phone,address,email1) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"  # from database
        cursor.execute(query, (animal, city, date, weighta, lbs, time, owner, address, phone, mail, dname, hname, dphone, daddress,demail))
        db.commit()
        db.close()
        return redirect(url_for('birthindex'))


@app.route("/birthindex")
def birthindex():
    db = mysql.connector.connect(user='root', password='admin', host='localhost', database='animal')
    cursor = db.cursor()
    query = "SELECT medicare__birth.id,medicare__client.first_name,medicare__animal.animal_name,medicare__birth.date_of_birth,medicare__birth.doctor_name FROM (medicare__birth INNER JOIN medicare__client ON medicare__birth.user_id=medicare__client.id) INNER join medicare__animal ON medicare__animal.id=medicare__birth.animal_id"
    cursor.execute(query)
    records = cursor.fetchall()
    return render_template('birthindex.html', values=records)


@app.route("/death")
def death():
    db = mysql.connector.connect(user='root', password='admin', host='localhost', database='animal')
    cursor = db.cursor()
    query = "SELECT * FROM medicare__animal"
    query1 = "SELECT * FROM medicare__client"
    query2 = "SELECT * FROM cities"
    cursor.execute(query)
    records = cursor.fetchall()
    cursor.execute(query1)
    records1 = cursor.fetchall()
    cursor.execute(query2)
    records2 = cursor.fetchall()
    return render_template('death.html', values=records, values1=records1,values2=records2)

@app.route("/insertd", methods=['GET','POST'])
def insertd():
    if request.method == 'GET':
        return render_template('death.html')
    else:
        db = mysql.connector.connect(user='root', password='admin', host='localhost', database='animal')
        cursor = db.cursor()
        animal = request.form['species_id']
        city = request.form['city']  # from from
        dates = request.form['date']
        date = datetime.strptime(dates, '%m/%d/%Y')
        owner = request.form['owner']
        time = request.form['time']
        mail = request.form['email']
        address = request.form['address']
        phone = request.form['phone']
        dname = request.form['dname']
        daddress = request.form['daddress']
        hname = request.form['hname']
        demail = request.form['demail']
        dphone = request.form['dphone']
        query = "INSERT INTO  medicare__death(animal_id,city_id,date_of_death,time_of_death,user_id,address,phone_no,email_id,doctor_name,hospital_name,hphone,haddress,hmail) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"  # from database
        cursor.execute(query, (animal, city, date,time, owner, address, phone, mail, dname, hname, dphone, daddress,demail))
        db.commit()
        db.close()
        return redirect(url_for('deathindex'))

@app.route("/deathindex")
def deathindex():
    db = mysql.connector.connect(user='root', password='admin', host='localhost', database='animal')
    cursor = db.cursor()
    query = "SELECT medicare__death.id,medicare__client.first_name,medicare__animal.animal_name,medicare__death.date_of_death,medicare__death.doctor_name FROM (medicare__death INNER JOIN medicare__client ON medicare__death.user_id=medicare__client.id) INNER join medicare__animal ON medicare__animal.id=medicare__death.animal_id"
    cursor.execute(query)
    records = cursor.fetchall()
    return render_template('deathindex.html', values=records)


@app.route("/doctorindex")
def doctorindex():
    db = mysql.connector.connect(user='root', password='admin', host='localhost', database='animal')
    cursor = db.cursor()
    query = "SELECT id,first_name,email,phone,hospital_name FROM medicare__doctor"
    cursor.execute(query)
    records = cursor.fetchall()
    return render_template('doctorindex.html', values=records)



@app.route("/doctor",methods=['GET','POST'])
def doctor():
    if request.method == 'GET':
        return render_template('doctor.html')
    else:
        db = mysql.connector.connect(user='root', password='admin', host='localhost', database='animal')
        cursor = db.cursor()
        fname = request.form['fname']
        lname = request.form['lname']  # from from
        dates = request.form['date']
        date = datetime.strptime(dates,'%m/%d/%Y')
        dphone = request.form['dphone']
        email = request.form['email']
        address = request.form['address']
        under = request.form['under']
        post = request.form['post']
        spec = request.form['spec']
        college = request.form['college']
        coll = request.form['coll']
        collge = request.form['collge']
        perc = request.form['perc']
        per = request.form['per']
        perce = request.form['per']
        hname = request.form['hname']
        add = request.form['add']
        hphone = request.form['hphone']
        hemail = request.form['hemail']
        query = "INSERT INTO  medicare__doctor(first_name,last_name,email,date_of_birth,phone,address,undergraduate	,coll,per,postgraduate,collge,perc,specialization,college,perce,hospital_name,hphone,hemail,haddress) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"  # from database
        cursor.execute(query, (fname,lname,email,date,dphone,address,under,coll,per,post,collge,perc,spec,college,perce,hname,add,hphone,hemail))
        db.commit()
        db.close()
        return render_template('doctor.html')

@app.route("/deleted", methods=['POST'])
def deleted():
    db = mysql.connector.connect(user='root', password='admin', host='localhost', database='animal')
    cursor = db.cursor()
    sid = request.form['doc_id']
    cursor.execute('DELETE FROM  medicare__doctor WHERE id = %s', [request.form['doc_id']])
    db.commit()
    cursor.close()
    db.close()
    return redirect(url_for('doctorindex'))

@app.route("/doctormodal",methods=['GET', 'POST'])
def doctormodal():
    if request.method == 'GET':
        return render_template('editdoctor.html')
    else:
        db = mysql.connector.connect(user='root', password='admin', host='localhost', database='animal')
        cursor = db.cursor()
        sid = request.form['doct_id']
        fname = request.form['fname']
        email = request.form['email']
        dphone = request.form['dphone']
        hname = request.form['hname']
        query = "UPDATE medicare__doctor SET first_name=%s , email=%s, phone=%s,hospital_name=%s WHERE id=%s"
        cursor.execute(query, (fname, email,dphone, hname,sid,))
        db.commit()
        cursor.close()
        db.close()
        return redirect(url_for('doctorindex'))

@app.route("/vacc",methods=['GET','POST'])
def vacc():
    if request.method=='GET':
        db=mysql.connector.connect(user='root', password='admin', host='localhost', database='animal')
        cursor=db.cursor()
        query="SELECT * FROM medicare__animal"
        query1="SELECT * FROM master__vaccination"
        cursor.execute(query)
        records = cursor.fetchall()
        cursor.execute(query1)
        records1 = cursor.fetchall()
        return render_template('vaccine.html',values=records,values1=records1)

@app.route("/insertv", methods=['GET', 'POST'])
def insertv():
        db=mysql.connector.connect(user='root', password='admin', host='localhost', database='animal')
        cursor=db.cursor()
        pet=request.form['species_id']
        typev=request.form['type'] #from from
        datev=request.form['date']
        datet=datetime.strptime(datev,'%m/%d/%Y')
        cost=request.form['cost']
        query="INSERT INTO  medicare__vaccine(animal_id,vaccine_id,datev,cost) VALUES(%s,%s,%s,%s)"
        cursor.execute(query,(pet,typev,datet,cost))
        db.commit()
        db.close()
        return redirect(url_for('vaccindex'))

@app.route("/vaccindex")
def vaccindex():
    db=mysql.connector.connect(user='root', password='admin', host='localhost', database='animal')
    cursor=db.cursor()
    cursor.execute("SELECT medicare__vaccine.id, medicare__animal.animal_name, master__vaccination.type, medicare__vaccine.datev, medicare__vaccine.cost FROM ((medicare__vaccine INNER JOIN master__vaccination ON medicare__vaccine.vaccine_id = master__vaccination.id) INNER JOIN medicare__animal ON medicare__vaccine.animal_id = medicare__animal.id)")
    records = cursor.fetchall()
    return render_template('vaccindex.html', values=records)

@app.route("/updatevacc", methods=['POST'])
def updatevacc():
    db = mysql.connector.connect(user='root', password='admin', host='localhost', database='animal')
    cursor = db.cursor()
    pet = request.form['vacc_id']
    typev = request.form['type']  # from from
    datev = request.form['date']
    datet = datetime.strptime(datev, '%m/%d/%Y')
    cost = request.form['cost']
    query = "UPDATE medicare__vaccine SET animal_id=%s ,vaccine_id=%s,datev=%s,cost=%s WHERE id=%s"
    cursor.execute(query, (pet,typev,datet,cost))
    db.commit()
    cursor.close()
    db.close()
    return redirect(url_for('vaccindex'))

@app.route("/deletevacc", methods=['POST'])
def deletevacc():
    db = mysql.connector.connect(user='root', password='admin', host='localhost', database='animal')
    cursor = db.cursor()
    sid = request.form['vaccd_id']
    cursor.execute('DELETE FROM medicare__vaccine WHERE id = %s', [request.form['vaccd_id']])
    db.commit()
    cursor.close()
    db.close()
    return redirect(url_for('vaccindex'))


@app.route("/treatment", methods=['GET'])
def treatment():
    if request.method=='GET':
        db=mysql.connector.connect(user='root', password='admin', host='localhost', database='animal')
        cursor=db.cursor()
        query="SELECT id,animal_name FROM medicare__animal"
        query1="SELECT id,type FROM master__test"
        cursor.execute(query)
        records = cursor.fetchall()
        cursor.execute(query1)
        records1 = cursor.fetchall()
        return render_template('treatment.html',values=records,values1=records1)

@app.route("/insertest", methods=['GET', 'POST'])
def insertest():
    db=mysql.connector.connect(user='root', password='admin', host='localhost', database='animal')
    cursor=db.cursor()
    pet=request.form['species_id']
    typev=request.form['test'] #from from
    dated=request.form['testD']
    result=request.form['result']
    datet=datetime.strptime(dated,'%m/%d/%Y')
    comment=request.form['comment']
    cost=request.form['cost']
    decease=request.form['Decease']
    tretment=request.form['tretment']
    certificate=request.form['certificate']
    query="INSERT INTO  medicare__treatment(animal_id,comment,certificate,test_id,decease_name,test_date,tretment_name,result,cost) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    cursor.execute(query,(pet,comment,certificate,typev,decease,datet,tretment,result,cost))
    db.commit()
    db.close()
    return redirect(url_for('treatmentindex'))


@app.route("/treatmentindex")
def treatmentindex():
    db=mysql.connector.connect(user='root', password='admin', host='localhost', database='animal')
    cursor=db.cursor()
    query = "SELECT id,animal_name FROM medicare__animal"
    query1 = "SELECT id,type FROM master__test"
    query2 = ("SELECT medicare__treatment.id,medicare__animal.animal_name,master__test.type,medicare__treatment.test_date,medicare__treatment.comment,medicare__treatment.decease_name,medicare__treatment.result,medicare__treatment.tretment_name,medicare__treatment.cost FROM ((medicare__treatment INNER JOIN medicare__animal ON medicare__treatment.animal_id=medicare__animal.id)INNER join master__test ON  medicare__treatment.test_id=master__test.id)")
    cursor.execute(query)
    records = cursor.fetchall()
    cursor.execute(query1)
    records1 = cursor.fetchall()
    cursor.execute(query2)
    records2 = cursor.fetchall()
    return render_template('treatmentindex.html',values=records,values1=records1,values2=records2)

@app.route("/updatetreat", methods=['POST'])
def updatetreat():
    db = mysql.connector.connect(user='root', password='admin', host='localhost', database='animal')
    cursor = db.cursor()
    sid = request.form['treat_id']
    pet = request.form['species_id']
    typev = request.form['test']  # from from
    dated = request.form['testD']
    result = request.form['result']
    datet = datetime.strptime(dated, '%m/%d/%Y')
    comment = request.form['comment']
    cost = request.form['cost']
    decease = request.form['Decease']
    tretment = request.form['tretment']
    certificate = request.form['certificate']
    query = "UPDATE medicare__treatment SET animal_id=%s , comment=%s, certificate=%s,test_id=%s, decease_name=%s,test_date=%s,tretment_name=%s,result=%s,cost=%s  WHERE id=%s"
    cursor.execute(query, (pet,comment,certificate,typev,decease,datet,tretment,result,cost,sid))
    db.commit()
    cursor.close()
    db.close()
    return redirect(url_for('treatmentindex'))

@app.route("/deletetreat", methods=['POST'])
def deletetreat():
    db = mysql.connector.connect(user='root', password='admin', host='localhost', database='animal')
    cursor = db.cursor()
    sid = request.form['treat_id']
    cursor.execute('DELETE FROM medicare__treatment WHERE id = %s', [request.form['treat_id']])
    db.commit()
    cursor.close()
    db.close()
    return redirect(url_for('treatmentindex'))


#appoindex
@app.route("/appo" , methods=['get'])
def appo():
    db=mysql.connector.connect(user='root', password='admin', host='localhost', database='animal')
    cursor= db.cursor()
    query = "SELECT * FROM medicare__appo"
    query1 = "SELECT id,animal_name FROM medicare__animal"
    query2 = "SELECT id, first_name FROM medicare__client"
    query3="SELECT medicare__appo.id,medicare__client.first_name,medicare__animal.animal_name,medicare__appo.datet,medicare__appo.mob_no,medicare__appo.time FROM (medicare__appo INNER JOIN  medicare__client ON medicare__appo.user_id=medicare__client.id)INNER JOIN medicare__animal ON medicare__appo.animal_id=medicare__animal.id"
    cursor.execute(query)
    records = cursor.fetchall()
    cursor.execute(query1)
    records1 = cursor.fetchall()
    cursor.execute(query2)
    records2 = cursor.fetchall()
    cursor.execute(query3)
    records3 = cursor.fetchall()
    return render_template('appo.html',values=records,values1=records1,values2=records2,values3=records3)

@app.route("/appoi", methods=['GET', 'POST'])
def appoi():
    if request.method == 'GET':
        return render_template('appo.html')
    else:
        db = mysql.connector.connect(user='root', password='admin', host='localhost', database='animal')
        cursor = db.cursor()
        client = request.form['client']
        datep = request.form['date']
        datet = datetime.strptime(datep, '%m/%d/%Y')
        problem = request.form['problem']
        species_id = request.form['species_id']
        time = request.form['time']
        mno = request.form['mno']
        query = "INSERT INTO  medicare__appo(user_id,animal_id,mob_no,datet,time,problem) VALUES(%s,%s,%s,%s,%s,%s)"  # from database
        cursor.execute(query,(client, species_id, mno, datet, time,problem))
        db.commit()
        db.close()
        return redirect(url_for('appo'))

@app.route("/updateappo", methods=['POST'])
def updateappo():
    db = mysql.connector.connect(user='root', password='admin', host='localhost', database='animal')
    cursor = db.cursor()
    sid = request.form['appo_id']
    client = request.form['client']
    datep = request.form['date']
    datet = datetime.strptime(datep, '%m/%d/%Y')
    species_id = request.form['species_id']
    time = request.form['time']
    mno = request.form['mno']
    query = "UPDATE medicare__appo SET user_id=%s , animal_id=%s,mob_no=%s,datet=%s,time=%s WHERE id=%s"
    cursor.execute(query, (client, species_id, mno, datet, time,sid))
    db.commit()
    cursor.close()
    db.close()
    return redirect(url_for('appo'))


@app.route("/deleteapo", methods=['POST'])
def deleteapo():
    db = mysql.connector.connect(user='root', password='admin', host='localhost', database='animal')
    cursor = db.cursor()
    sid = request.form['apo_id']
    cursor.execute('DELETE FROM  medicare__appo WHERE id = %s', [request.form['apo_id']])
    db.commit()
    cursor.close()
    db.close()
    return redirect(url_for('appo'))


@app.route("/auth")
def auth():
    return render_template('auth-lock-screen.html')



if __name__ == "__main__":
    app.run(debug=True)


