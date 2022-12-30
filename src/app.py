from flask import Flask, jsonify, request, session, redirect, url_for, render_template
from flask_mysqldb import MySQL
from config import config
from werkzeug.utils import secure_filename
from flask_cors import CORS, cross_origin
import os
from random import sample

app = Flask(__name__)
CORS(app)
conn = MySQL(app)


#      ░░░░░██╗░█████╗░░██████╗██╗░░██╗░██████╗██████╗░
#      ░░░░░██║██╔══██╗██╔════╝██║░░██║██╔════╝██╔══██╗
#      ░░░░░██║██║░░██║╚█████╗░███████║╚█████╗░██████╦╝
#      ██╗░░██║██║░░██║░╚═══██╗██╔══██║░╚═══██╗██╔══██╗
#      ╚█████╔╝╚█████╔╝██████╔╝██║░░██║██████╔╝██████╦╝
#      ░╚════╝░░╚════╝░╚═════╝░╚═╝░░╚═╝╚═════╝░╚═════╝░
#           𝗦𝗶 𝗰𝗿𝗲𝗲𝘀 𝗾𝘂𝗲 𝗱𝗲𝗯𝗮 𝗺𝗲𝗷𝗼𝗿𝗮𝗿 𝗮𝗹𝗴𝗼 𝗵𝗮𝘇𝗹𝗼 𝘀𝗮𝗯𝗲𝗿
#    If you think something needs to be improved, let me know.


#################### PRINCIPAL ROUTE ####################
@cross_origin
@app.route("/", methods=['GET','DELETE','POST','PUT'])
def home():
    if request.method == 'GET':
        return jsonify({'MESSAGE':"GET - HOME"})
        #return render_template("index.html")
    elif request.method == 'POST':
        return jsonify({'MESSAGE':"HOME"})
    elif request.method == 'PUT':
      return jsonify({'MESSAGE':"PUT - HOME"})
    elif request.method == 'DELETE':
      return jsonify({'MESSAGE':"DELETE - HOME"})
  

@app.route("/uploadFile", methods=['GET','POST'])
def uploadFile():
    if request.method == 'POST':
        
        file = request.files['file']
        
        if file.filename == '':
          return jsonify({'MESSAGE':"What are you doing? You didn't upload any files man..."})
      
        else:
            
            basepath = os.path.dirname(__file__)
            filename= secure_filename(file.filename) 
            extension = os.path.splitext(filename)[1]
            dominio = url_for('uploadFile')
            
            if extension == '.gif' or extension == '.png' or extension == '.jpg' or extension == '.jpeg':
                
                newNameFile = randomString() + extension
                upload_path = os.path.join(basepath, 'static/uploads', newNameFile)
                file.save(upload_path)
                print("<==== ★ ====>\nbasepath: "+str(basepath)+"\nFilename:"+str(filename)+"\nExtension: "+str(extension)+"\nDominio: "+str(dominio)+"\n=================")
                return jsonify({'MESSAGE':"File uploaded!"})
            
            else:
                
                return jsonify({'MESSAGE':"File formad not supported"})


#################### LOGIN ROUTES ####################
@cross_origin
@app.before_request
def before_request(): #THIS METHOD IS TO RESTRICT ROUTES
    if 'username' not in session and request.endpoint in ['see_users', 'see_usersId', 'see_usersName', 'see_rol', 'see_rolId', 'see_rolName', 'add_users', 'add_rol', 'update_users','update_rol','delete_users','delete_rol', 'add_autors', 'add_books', 'add_geners', 'add_Editorials', 'update_autors', 'update_books', 'update_geners', 'update_editorials', 'delete_Autors', 'delete_books', 'delete_geners', 'delete_Editorials']:
        return redirect(url_for('home'))
    elif 'username' in session and request.endpoint in ['login']:
        return redirect(url_for('home'))
    elif 'idRol' in session:
        if session['idRol'] != 1 and request.endpoint in ['see_users', 'see_usersId', 'see_usersName', 'see_rol', 'see_rolId', 'see_rolName', 'add_users', 'add_rol', 'update_users','update_rol','delete_users','delete_rol']:
            return redirect(url_for('home'))
        elif session['idRol'] != 2 and request.endpoint in ['add_autors', 'add_books', 'add_geners', 'add_Editorials', 'update_autors', 'update_books', 'update_geners', 'update_editorials', 'delete_Autors', 'delete_books', 'delete_geners', 'delete_Editorials']:
            return redirect(url_for('home'))

@cross_origin
@app.route("/login/", methods=['GET','POST']) # LOGIN ROUTE (OBVIOUS?)
def login():
    if request.method == 'POST': 
        nameUsers = request.json['nameUsers']
        passUsers = request.json['passUsers']
        #idRol = request.json['idRol']
        try:
            cursor = conn.connection.cursor()
            sql = "SELECT * FROM users WHERE nameUsers='"+str(nameUsers)+"' and passUsers='"+str(passUsers)+"'"
            cursor.execute(sql)
            datos = cursor.fetchall()
            if datos:
                for fila in datos:
                    user = fila[1]
                    password = fila[2]
                    rol = fila[4]
                session['username'] = user
                session['password'] = password
                session['idRol'] = rol
                print(str(rol)+" "+str(user)+" "+str(password))
                return jsonify({'MESSAGE':"USER FOUND"})
                #return jsonify({'MESSAGE':""+str(nameUsers)+" "+str(passUsers)})
            else:
                return jsonify({'MESSAGE':"USER NOT FOUND"},{'user':user},{'password':password},{'rol':rol})
            
        except Exception as ex:
            return jsonify({'Message':"Error: "+str(ex)})
    elif request.method == 'GET':
        return jsonify({'MESSAGE':"GET <-- this is the method"})

@cross_origin
@app.route("/logout/")
def logout():
    if 'username' in session:
        session.pop('username')
    return redirect(url_for('home'))

#################### GET ROUTES ####################
#----USER----

@cross_origin
@app.route('/users/', methods=['GET']) # SEE ALL USERS
def see_users():
    try:
        cursor = conn.connection.cursor()
        sql = "SELECT * FROM users"
        cursor.execute(sql)
        datos = cursor.fetchall()
        users=[]
        if datos != None:
            for fila in datos:
                user={
                    'idUsers':fila[0],
                    'nameUsers':fila[1],
                    'passUsers':fila[2],
                    'dateUsers':fila[3],
                    'idRol':fila[4]
                }
                users.append(user)
            return jsonify({'users':users, 'Message':"users list"})
        else:
            return jsonify({'Message':"A error has ocurred"})
    except Exception as ex:
        return jsonify({'Message':"Error"+str(ex)})

@cross_origin    
@app.route('/users/id/<id>', methods=['GET']) # SEE USERS FOR ID
def see_usersId(id):
    try:
        tableName = 'users'
        nameId = 'idUsers'
        cursor = conn.connection.cursor()
        if validePK(str(id), tableName, nameId):
            sql = "SELECT * FROM users WHERE idUsers='{0}'".format(id)
            cursor.execute(sql)
            datos = cursor.fetchone()    
            if datos != None:
                user={
                    'idUsers':datos[0],
                    'nameUsers':datos[1],
                    'passUsers':datos[2],
                    'dateUsers':datos[3],
                    'idRol':datos[4]
                }
                return jsonify({'users':user, 'Message':"user found"})
        else:
            return jsonify({'Message':"User whit ID: "+id+" not found"})
    except Exception as ex:
        return jsonify({'Message':str(ex)})

@cross_origin
@app.route('/users/name/<name>', methods=['GET']) # SEE USERS FOR NAME
def see_usersName(name):
    try:
        tableName = 'users'
        nameId = 'nameUsers'
        cursor = conn.connection.cursor()
        if validePK(str(name), tableName, nameId):
            sql = "SELECT * FROM users WHERE nameUsers='{0}'".format(name)
            cursor.execute(sql)
            datos = cursor.fetchone()    
            if datos != None:
                user={
                    'idUsers':datos[0],
                    'nameUsers':datos[1],
                    'passUsers':datos[2],
                    'dateUsers':datos[3],
                    'idRol':datos[4]
                }
                return jsonify({'users':user, 'Message':"user found"})
            else:
                return jsonify({'users':user, 'Message':"user not found"})
        else:
            return jsonify({'Message':"User whit Name: "+name+" not found"})
    except Exception as ex:
        return jsonify({'Message':str(ex)})


#----ROL----

@cross_origin
@app.route('/rol/', methods=['GET']) # SEE ALL ROLS
def see_rol():
    try:
        cursor = conn.connection.cursor()
        sql = "SELECT * FROM rol"
        cursor.execute(sql)
        datos = cursor.fetchall()
        rols=[]
        if datos != None:
            for fila in datos:
                rol={
                    'idRol':fila[0],
                    'nameRol':fila[1],
                    'dateRol':fila[2]
                }
                rols.append(rol)
            return jsonify({'users':rols, 'Message':"Rol list"})
        else:
            return jsonify({'Message':"A error has ocurred"})
    except Exception as ex:
        return jsonify({'Message':"Error"+str(ex)})

@cross_origin
@app.route('/rol/id/<id>', methods=['GET']) # SEE ROL FOR ID
def see_rolId(id):
    try:
        tableName = 'rol'
        nameId = 'idRol'
        cursor = conn.connection.cursor()
        if validePK(str(id), tableName, nameId):
            sql = "SELECT * FROM rol WHERE idRol = '{0}'".format(id)
            cursor.execute(sql)
            datos = cursor.fetchall()
            rols=[]

            if datos != None:
                for fila in datos:
                    rol={
                        'idRol':fila[0],
                        'nameRol':fila[1],
                        'dateRol':fila[2]
                    }
                rols.append(rol)
                return jsonify({'Rol':rols})
            else:
                return jsonify({'Message':"A error has ocurred"})
        else:
            return jsonify({'Message':"Rol whit ID: "+id+" not found"})
        
    except Exception as ex:
        return jsonify({'Message':"Error"+str(ex)})

@cross_origin
@app.route('/rol/name/<name>', methods=['GET']) # SEE ROL FOR NAME
def see_rolName(name):
    try:
        tableName = 'rol'
        nameId = 'nameRol'
        cursor = conn.connection.cursor()
        if validePK(str(name), tableName, nameId):
            sql = "SELECT * FROM rol WHERE nameRol = '{0}'".format(name)
            cursor.execute(sql)
            datos = cursor.fetchall()
            rols=[]

            if datos != None:
                for fila in datos:
                    rol={
                        'idRol':fila[0],
                        'nameRol':fila[1],
                        'dateRol':fila[2]
                    }
                rols.append(rol)
                return jsonify({'Rol':rols})
            else:
                return jsonify({'Message':"A error has ocurred"})
        else:
            return jsonify({'Message':"Rol whit name: "+name+" not found"})
        
    except Exception as ex:
        return jsonify({'Message':"Error"+str(ex)})


#----AUTORS----

@cross_origin
@app.route('/autors/', methods=['GET']) # SEE AUTORS WITH ID
def see_autors():
    try:
        cursor = conn.connection.cursor()
        sql = "SELECT * FROM autors"
        cursor.execute(sql)
        datos = cursor.fetchall()
        autors=[]
        if datos != None:
            for fila in datos:
                autor={
                    'idAutors':fila[0],
                    'nameAutors':fila[1],
                    'lsnameAutors':fila[2],
                    'bibliography':fila[3],
                    'yoldAutors':fila[4],
                    'dateAutors':fila[5],
                    'statusAutors':fila[6]
                }
                autors.append(autor)
            return jsonify({'Autors':autors, 'Message':"Autors list"})
        else:
            return jsonify({'Message':"A error has ocurred"})
    except Exception as ex:
        return jsonify({'Message':"Error "+str(ex)})

@cross_origin
@app.route('/autors/id/<id>', methods=['GET']) # SEE AUTORS WITH ID
def see_autorsId(id):
    try:
        tableName = 'autors'
        nameId = 'idAutors'
        cursor = conn.connection.cursor()
        if validePK(str(id), tableName, nameId):
            sql = "SELECT * FROM autors WHERE idAutors = '{0}'".format(id)
            cursor.execute(sql)
            datos = cursor.fetchall()
            autors=[]
            if datos != None:
                for fila in datos:
                    autor={
                        'idAutors':fila[0],
                        'nameAutors':fila[1],
                        'lsnameAutors':fila[2],
                        'bibliography':fila[3],
                        'yoldAutors':fila[4],
                        'dateAutors':fila[5],
                        'statusAutors':fila[6]
                    }
                    autors.append(autor)
                return jsonify({'Autors':autors, 'Message':"Autors list"})
            else:
                return jsonify({'Message':"A error has ocurred"})
        else:
            return jsonify({'Message':"Autor whit ID: "+id+" not found"})
    except Exception as ex:
        return jsonify({'Message':"Error"+str(ex)})

@cross_origin
@app.route('/autors/name/<name>', methods=['GET']) # SEE AUTORS WITH NAME
def see_autorsName(name):
    try:
        tableName = 'autors'
        nameId = 'nameAutors'
        cursor = conn.connection.cursor()
        if validePK(str(name), tableName, nameId):
            sql = "SELECT * FROM autors WHERE nameAutors='{0}'".format(name)
            cursor.execute(sql)
            datos = cursor.fetchall()
            autors=[]
            if datos != None:
                for fila in datos:
                    autor={
                        'idAutors':fila[0],
                        'nameAutors':fila[1],
                        'lsnameAutors':fila[2],
                        'bibliography':fila[3],
                        'yoldAutors':fila[4],
                        'dateAutors':fila[5],
                        'statusAutors':fila[6]
                    }
                    autors.append(autor)
                return jsonify({'Autors':autors, 'Message':"Autors list"})
            else:
                return jsonify({'Message':"A error has ocurred"})
        else:
            return jsonify({'Message':"Autor whit name: "+name+" not found"})
    except Exception as ex:
        return jsonify({'Message':"Error"+str(ex)})

@cross_origin
@app.route('/autors/lastname/<lsname>', methods=['GET']) # SEE AUTORS WITH ID
def see_autorsLsName(lsname):
    try:
        tableName = 'autors'
        nameId = 'lsnameAutors'
        cursor = conn.connection.cursor()
        if validePK(str(lsname), tableName, nameId):
            sql = "SELECT * FROM autors WHERE lsnameAutors='{0}'".format(lsname)
            cursor.execute(sql)
            datos = cursor.fetchall()
            autors=[]
            if datos != None:
                for fila in datos:
                    autor={
                        'idAutors':fila[0],
                        'nameAutors':fila[1],
                        'lsnameAutors':fila[2],
                        'bibliography':fila[3],
                        'yoldAutors':fila[4],
                        'dateAutors':fila[5],
                        'statusAutors':fila[6]
                    }
                    autors.append(autor)
                return jsonify({'Autors':autors, 'Message':"Autors list"})
            else:
                return jsonify({'Message':"A error has ocurred"})
        else:
            return jsonify({'Message':"Autor whit last name: "+lsname+" not found"})
    except Exception as ex:
        return jsonify({'Message':"Error"+str(ex)})


#----GENERS----

@cross_origin
@app.route('/geners/', methods=['GET']) # SEE ALL GENERS
def see_geners():
    try:
        cursor = conn.connection.cursor()
        sql = "SELECT * FROM geners"
        cursor.execute(sql)
        datos = cursor.fetchall()
        geners=[]
        if datos != None:
            for fila in datos:
                gener={
                    'idGeners':fila[0],
                    'nameGeners':fila[1],
                    'dateGeners':fila[2]
                }
                geners.append(gener)
            return jsonify({'users':geners, 'Message':"users list"})
        else:
            return jsonify({'Message':"A error has ocurred"})
    except Exception as ex:
        return jsonify({'Message':"Error"+str(ex)})

@cross_origin
@app.route('/geners/id/<id>', methods=['GET']) # SEE ALL GENERS WITH ID
def see_genersId(id):
    try:
        tableName = 'geners'
        nameId = 'idGeners'
        cursor = conn.connection.cursor()
        if validePK(str(id), tableName, nameId):
            sql = "SELECT * FROM geners WHERE idGeners = '{0}'".format(id)
            cursor.execute(sql)
            datos = cursor.fetchall()
            geners=[]
            if datos != None:
                for fila in datos:
                    gener={
                        'idGeners':fila[0],
                        'nameGeners':fila[1],
                        'dateGeners':fila[2]
                    }
                    geners.append(gener)
                return jsonify({'users':geners, 'Message':"users list"})
            else:
                return jsonify({'Message':"A error has ocurred"})
        else:
            return jsonify({'Message':"Gener whit ID: "+id+" not found"})
    except Exception as ex:
        return jsonify({'Message':"Error"+str(ex)})

@cross_origin()
@app.route('/geners/name/<name>', methods=['GET']) # SEE ALL GENERS WITH NAME
def see_genersName(name):
    try:
        tableName = 'geners'
        nameId = 'nameGeners'
        cursor = conn.connection.cursor()
        if validePK(str(name), tableName, nameId):
            sql = "SELECT * FROM geners WHERE nameGeners = '{0}'".format(name)
            cursor.execute(sql)
            datos = cursor.fetchall()
            geners=[]
            if datos != None:
                for fila in datos:
                    gener={
                        'idGeners':fila[0],
                        'nameGeners':fila[1],
                        'dateGeners':fila[2]
                    }
                    geners.append(gener)
                return jsonify({'users':geners, 'Message':"users list"})
            else:
                return jsonify({'Message':"A error has ocurred"})
        else:
            return jsonify({'Message':"Gener whit ID: "+name+" not found"})
    except Exception as ex:
        return jsonify({'Message':"Error"+str(ex)})
    
  
  
  #----EDITORIALAS----

@cross_origin
@app.route('/editorials/', methods=['GET']) # SEE ALL EDITORIALS
def see_editorials():
    try:
        cursor = conn.connection.cursor()
        sql = "SELECT * FROM editorials"
        cursor.execute(sql)
        datos = cursor.fetchall()
        editorials=[]
        if datos != None:
            for fila in datos:
                editorial={
                    'idEditorials':fila[0],
                    'nameEditorials':fila[1],
                    'dateEditorials':fila[2]
                }
                editorials.append(editorial)
            return jsonify({'users':editorials, 'Message':"users list"})
        else:
            return jsonify({'Message':"A error has ocurred"})
    except Exception as ex:
        return jsonify({'Message':"Error"+str(ex)})

@cross_origin
@app.route('/editorials/id/<id>', methods=['GET']) # SEE ALL EDITORIALS WITH ID
def see_editorialsId(id):
    try:
        tableName = 'editorials'
        nameId = 'idEditorials'
        cursor = conn.connection.cursor()
        if validePK(str(id), tableName, nameId):
            sql = "SELECT * FROM editorials WHERE idEditorials='{0}'".format(id)
            cursor.execute(sql)
            datos = cursor.fetchall()
            editorials=[]
            if datos != None:
                for fila in datos:
                    editorial={
                        'idEditorials':fila[0],
                        'nameEditorials':fila[1],
                        'dateEditorials':fila[2]
                    }
                    editorials.append(editorial)
                return jsonify({'users':editorials, 'Message':"users list"})
            else:
                return jsonify({'Message':"A error has ocurred"})
        else:
            return jsonify({'Message':"Editorial whit ID: "+id+" not found"})
    except Exception as ex:
        return jsonify({'Message':"Error"+str(ex)})

@cross_origin
@app.route('/editorials/name/<name>', methods=['GET']) # SEE ALL GENERS WITH NAME
def see_editorialsName(name):
    try:
        tableName = 'editorials'
        nameId = 'nameEditorials'
        cursor = conn.connection.cursor()
        if validePK(str(name), tableName, nameId):
            sql = "SELECT * FROM editorials WHERE nameEditorials='{0}'".format(name)
            cursor.execute(sql)
            datos = cursor.fetchall()
            editorials=[]
            if datos != None:
                for fila in datos:
                    editorial={
                        'idEditorials':fila[0],
                        'nameEditorials':fila[1],
                        'dateEditorials':fila[2]
                    }
                    editorials.append(editorial)
                return jsonify({'users':editorials, 'Message':"users list"})
            else:
                return jsonify({'Message':"A error has ocurred"})
        else:
            return jsonify({'Message':"Editorial whit ID: "+id+" not found"})
    except Exception as ex:
        return jsonify({'Message':"Error"+str(ex)})



#----BOOKS-----
@cross_origin
@app.route('/books/', methods=['GET']) # SEE ALL BOOKS
def see_books():
    try:
        cursor = conn.connection.cursor()
        sql = "SELECT * FROM books"
        cursor.execute(sql)
        datos = cursor.fetchall()
        books=[]
        if datos != None:
            for fila in datos:
                book={
                    'idBooks':fila[0],
                    'nameBooks':fila[1],
                    'frontBooks':fila[2],
                    'descriptions':fila[3],
                    'priceBooks':fila[4],
                    'dateBooks':fila[5],
                    'statusBooks':fila[6],
                    'idAutors':fila[7],
                    'idGeners':fila[8],
                    'idEditorials':fila[9]
                }
                books.append(book)
            return jsonify({'users':books, 'Message':"users list"})
        else:
            return jsonify({'Message':"A error has ocurred"})
    except Exception as ex:
        return jsonify({'Message':"Error"+str(ex)})
    
@cross_origin
@app.route('/books/id/<id>', methods=['GET']) # SEE BOOKS WITH ID
def see_booksId(id):
    try:
        tableName = 'books'
        nameId = 'idBooks'
        cursor = conn.connection.cursor()
        if validePK(str(id), tableName, nameId):
            sql = "SELECT * FROM books WHERE idBooks='{0}'".format(id)
            cursor.execute(sql)
            datos = cursor.fetchone()    
            if datos != None:
                book={
                    'idBooks':datos[0],
                    'nameBooks':datos[1],
                    'frontBooks':datos[2],
                    'descriptions':datos[3],
                    'priceBooks':datos[4],
                    'dateBooks':datos[5],
                    'statusBooks':datos[6],
                    'idAutors':datos[7],
                    'idGeners':datos[8],
                    'idEditorials':datos[9]
                }
                return jsonify({'books':book, 'Message':"user found"})
        else:
            return jsonify({'Message':"User whit ID: "+id+" not found"})
    except Exception as ex:
        return jsonify({'Message':str(ex)})

@cross_origin
@app.route('/books/name/<name>', methods=['GET']) # SEE BOOKS WITH ID
def see_booksName(name):
    try:
        tableName = 'books'
        nameId = 'nameBooks'
        cursor = conn.connection.cursor()
        if validePK(str(name), tableName, nameId):
            sql = "SELECT * FROM books WHERE nameBooks='{0}'".format(name)
            cursor.execute(sql)
            datos = cursor.fetchone()    
            if datos != None:
                book={
                    'idBooks':datos[0],
                    'nameBooks':datos[1],
                    'frontBooks':datos[2],
                    'descriptions':datos[3],
                    'priceBooks':datos[4],
                    'dateBooks':datos[5],
                    'statusBooks':datos[6],
                    'idAutors':datos[7],
                    'idGeners':datos[8],
                    'idEditorials':datos[9]
                }
                return jsonify({'books':book, 'Message':"user found"})
        else:
            return jsonify({'Message':"User whit name: "+name+" not found"})
    except Exception as ex:
        return jsonify({'Message':str(ex)})
    
@cross_origin
@app.route('/books/idGeners/<idGeners>', methods=['GET']) # SEE BOOKS WITH ID
def see_booksIdGeners(idGeners):
    try:
        tableName = 'books'
        nameId = 'idGeners'
        cursor = conn.connection.cursor()
        if validePK(str(idGeners), tableName, nameId):
            sql = "SELECT * FROM books WHERE idGeners='{0}'".format(idGeners)
            cursor.execute(sql)
            datos = cursor.fetchone()    
            if datos != None:
                book={
                    'idBooks':datos[0],
                    'nameBooks':datos[1],
                    'frontBooks':datos[2],
                    'descriptions':datos[3],
                    'priceBooks':datos[4],
                    'dateBooks':datos[5],
                    'statusBooks':datos[6],
                    'idAutors':datos[7],
                    'idGeners':datos[8],
                    'idEditorials':datos[9]
                }
                return jsonify({'books':book, 'Message':"user found"})
        else:
            return jsonify({'Message':"User whit idGeners: "+idGeners+" not found"})
    except Exception as ex:
        return jsonify({'Message':str(ex)})

#################### POST ROUTES ####################
#----USER----
@cross_origin
@app.route('/addUser/', methods=['POST']) # ADD NEW USER
def add_users():
    try:
        cursor = conn.connection.cursor()
        idRol = request.json['idRol']
        nameUsers = request.json['nameUsers']
        passUsers = request.json['passUsers']
        sql = "INSERT INTO users (idRol, nameUsers, passUsers) VALUES (%s,%s,%s)"
        if validePK(str(nameUsers), 'users', 'nameUsers'):
            return jsonify({'Message':"¡User already exist!"})
        else:
            cursor.execute((sql), (idRol, nameUsers, passUsers))
            conn.connection.commit() # CONFIRM INSERT
            return jsonify({'Message':"¡User Added!"})
    except Exception as ex:
        return jsonify({'Message':"Error: "+str(ex)})

#----ROL----
@cross_origin
@app.route('/addRol/', methods=['POST']) # ADD NEW ROL
def add_rol():
    try:
        cursor = conn.connection.cursor()
        nameRol = request.json['nameRol']
        sql = "INSERT INTO rol(nameRol) VALUES ('"+str(nameRol)+"')"
        if validePK(str(nameRol), 'rol', 'nameRol'):
            return jsonify({'Message':"¡Rol already exist!"})
        else:
            cursor.execute(sql)
            conn.connection.commit() # CONFIRM INSERT
            return jsonify({'Message':"¡Rol added!"})
    except Exception as ex:
        return jsonify({'Message':"Error: "+str(ex)})


#----Autors----
@cross_origin
@app.route('/addAutors/', methods=['POST']) # ADD NEW AUTOR
def add_autors():
    try:
        cursor = conn.connection.cursor()
        nameAutors = request.json['nameAutors']
        lsnameAutors = request.json['lsnameAutors']
        bibliography = request.json['bibliography']
        yoldAutors = request.json['yoldAutors']
        sql = "INSERT INTO autors (nameAutors, lsnameAutors, bibliography, yoldAutors) VALUES (%s,%s,%s,%s)"
        cursor.execute((sql), (nameAutors, lsnameAutors, bibliography, yoldAutors))
        conn.connection.commit() # CONFIRM INSERT
        return jsonify({'Message':"Autor added"})
    except Exception as ex:
        return jsonify({'Message':"Error: "+str(ex)})
    

#----GENERS----
@cross_origin
@app.route('/addGeners/', methods=['POST']) # ADD NEW ROL
def add_geners():
    try:
        cursor = conn.connection.cursor()
        nameGeners = request.json['nameGeners']
        sql = "INSERT INTO geners(nameGeners) VALUES ('"+str(nameGeners)+"')"
        if validePK(str(nameGeners), 'geners', 'nameGeners'):
            return jsonify({'Message':"Gener already exist!"})
        else:
            cursor.execute(sql)
            conn.connection.commit() # CONFIRM INSERT
            return jsonify({'Message':"Gener added!"})
    except Exception as ex:
        return jsonify({'Message':"Error: "+str(ex)})


#----EDITORIALS----
@cross_origin
@app.route('/addEditorials/', methods=['POST']) # ADD NEW ROL
def add_Editorials():
    try:
        cursor = conn.connection.cursor()
        nameEditorials = request.json['nameEditorials']
        sql = "INSERT INTO editorials (nameEditorials) VALUES ('"+str(nameEditorials)+"')"
        if validePK(str(nameEditorials), 'editorials', 'nameEditorials'):
            return jsonify({'Message':"Gener already exist!"})
        else:
            cursor.execute(sql)
            conn.connection.commit() # CONFIRM INSERT
            return jsonify({'Message':"Editorial added!"})
    except Exception as ex:
        return jsonify({'Message':"Error: "+str(ex)})


#################### DELETE ROUTES ####################
#----USER----
@cross_origin
@app.route('/delUsers/<id>', methods=['DELETE']) # DELETE USER
def delete_users(id):
    try:
        cursor = conn.connection.cursor()
        if validePK(str(id), 'users', 'idUsers'):
            sql = "DELETE FROM users WHERE idUsers='{0}'".format(id)
            cursor.execute(sql)
            conn.connection.commit() # CONFIRM INSERT
            return jsonify({'Message':"User delated"})
        else:
            return jsonify({'Message':"User with ID: "+id+" not found"})
    except Exception as ex:
        return jsonify({'Message':"Error: "+str(ex)})


#----ROL----
@cross_origin
@app.route('/delRol/<id>', methods=['DELETE']) # DELETE ROL
def delete_Rol(id):
    try:
        cursor = conn.connection.cursor()
        if validePK(str(id), 'rol', 'idRol'):
            sql = "DELETE FROM rol WHERE idRol='{0}'".format(id)
            cursor.execute(sql)
            conn.connection.commit() # CONFIRM INSERT
            return jsonify({'Message':"Rol delated"})
        else:
            return jsonify({'Message':"Rol with ID: "+id+" not found"})
    except Exception as ex:
        return jsonify({'Message':"Error: "+str(ex)})


#----AUTORS----
@cross_origin
@app.route('/delAutors/<id>', methods=['DELETE']) # DELETE AUTORS
def delete_Autors(id):
    try:
        cursor = conn.connection.cursor()
        if validePK(str(id), 'autors', 'idAutors'):
            sql = "DELETE FROM autors WHERE idAutors='{0}'".format(id)
            cursor.execute(sql)
            conn.connection.commit() # CONFIRM INSERT
            return jsonify({'Message':"Autor delated"})
        else:
            return jsonify({'Message':"Autor with ID: "+id+" not found"})
    except Exception as ex:
        return jsonify({'Message':"Error: "+str(ex)})


#----GENERS----
@cross_origin
@app.route('/delGeners/<id>', methods=['DELETE']) # DELETE GENERS
def delete_Geners(id):
    try:
        cursor = conn.connection.cursor()
        if validePK(str(id), 'geners', 'idGeners'):
            sql = "DELETE FROM geners WHERE idGeners='{0}'".format(id)
            cursor.execute(sql)
            conn.connection.commit() # CONFIRM INSERT
            return jsonify({'Message':"Gener delated"})
        else:
            return jsonify({'Message':"Gener with ID: "+id+" not found"})
    except Exception as ex:
        return jsonify({'Message':"Error: "+str(ex)})


#----EDITORIALS----
@cross_origin
@app.route('/delEditorials/<id>', methods=['DELETE']) # DELETE EDITORIAL
def delete_Editorials(id):
    try:
        cursor = conn.connection.cursor()
        if validePK(str(id), 'editorials', 'idEditorials'):
            sql = "DELETE FROM editorials WHERE idEditorials='{0}'".format(id)
            cursor.execute(sql)
            conn.connection.commit() # CONFIRM INSERT
            return jsonify({'Message':"Editorial delated"})
        else:
            return jsonify({'Message':"Editorial with ID: "+id+" not found"})
    except Exception as ex:
        return jsonify({'Message':"Error: "+str(ex)})

#################### PUT ROUTES ####################
@cross_origin
@app.route('/upUsers/<id>', methods=['PUT']) # UPDATE USERS
def update_users(id):
    try:
        cursor = conn.connection.cursor()
        if validePK(str(id), 'users', 'idUsers'):
            idRol = request.json['idRol']
            nameUsers = request.json['nameUsers']
            passUsers = request.json['passUsers']
            sql = "UPDATE users SET idRol=%s, nameUsers=%s, passUsers=%s WHERE idUsers=%s"
            cursor.execute((sql), (idRol, nameUsers, passUsers, id))
            conn.connection.commit() # CONFIRM INSERT
            return jsonify({'Message':"User updated"})
        else:
            return jsonify({'Message':"User whit ID: "+id+" not found"})
    except Exception as ex:
        return jsonify({'Message':"Error: "+str(ex)})


#----ROL----
@cross_origin
@app.route('/upRol/<id>', methods=['PUT']) # UPDATE ROL
def update_rol(id):
    try:
        cursor = conn.connection.cursor()
        if validePK(str(id), 'rol', 'idRol'):
            nameRol = request.json['nameRol']
            sql = "UPDATE rol SET nameRol=%s WHERE idRol=%s"
            cursor.execute((sql), (nameRol,  id))
            conn.connection.commit() # CONFIRM INSERT
            return jsonify({'Message':"Rol Updated"})
        else:
            return jsonify({'Message':"Rol whit ID: "+id+" not found"})
    except Exception as ex:
        return jsonify({'Message':"Error: "+str(ex)})


#----Autors----
@cross_origin
@app.route('/upAutors/<id>', methods=['PUT']) # UPDATE AUTORS
def update_autors(id):
    try:
        cursor = conn.connection.cursor()
        if validePK(str(id), 'autors', 'idAutors'):
            nameAutors = request.json['nameAutors']
            lsnameAutors = request.json['lsnameAutors']
            bibliography = request.json['bibliography']
            yoldAutors = request.json['yoldAutors']
            sql = "UPDATE autors SET nameAutors=%s, lsnameAutors=%s, bibliography=%s, yoldAutors=%s WHERE idAutors=%s"
            cursor.execute((sql), (nameAutors, lsnameAutors, bibliography, yoldAutors, id))
            conn.connection.commit() # CONFIRM INSERT
            return jsonify({'Message':"Autor updated"})
        else:
            return jsonify({'Message':"Autor whit ID: "+id+" not found"})
    except Exception as ex:
        return jsonify({'Message':"Error: "+str(ex)})    

#----GENERS----
@cross_origin
@app.route('/upGeners/<id>', methods=['PUT']) # UPDATE GENERS
def update_geners(id):
    try:
        cursor = conn.connection.cursor()
        if validePK(str(id), 'geners', 'idGeners'):
            nameGeners = request.json['nameGeners']
            sql = "UPDATE geners SET nameGeners=%s WHERE idGeners=%s"
            cursor.execute((sql), (nameGeners,  id))
            conn.connection.commit() # CONFIRM INSERT
            return jsonify({'Message':"Gener Updated"})
        else:
            return jsonify({'Message':"Gener whit ID: "+id+" not found"})
    except Exception as ex:
        return jsonify({'Message':"Error: "+str(ex)})

#----EDITORIALS----
@cross_origin
@app.route('/upEditorials/<id>', methods=['PUT']) # UPDATE EDITORIALS
def update_editorials(id):
    try:
        cursor = conn.connection.cursor()
        if validePK(str(id), 'editorials', 'idEditorials'):
            nameEditorials = request.json['nameEditorials']
            sql = "UPDATE editorials SET nameEditorials=%s WHERE idEditorials=%s"
            cursor.execute((sql), (nameEditorials,  id))
            conn.connection.commit() # CONFIRM INSERT
            return jsonify({'Message':"Gener Updated"})
        else:
            return jsonify({'Message':"Gener whit ID: "+id+" not found"})
    except Exception as ex:
        return jsonify({'Message':"Error: "+str(ex)})


#################### VALIDATIONS ####################   

def validar_codigo(id: str) -> bool:
    return (id.isnumeric() and len(id) <= 11 and len(id) >= 1) 
     
def validePK(columnData: str, table: str, nameColumn: str) -> bool: #VALIDE USERS AND PRIMARY KEYS
    cursor = conn.connection.cursor()
    sql = "SELECT * FROM "+str(table)+" WHERE "+str(nameColumn)+"='"+str(columnData)+"'"
    print("Table: "+str(table)+" - Column: "+str(nameColumn)+" - Data: "+str(columnData)+"")
    cursor.execute(sql)
    dato = cursor.fetchone()
    if dato:
        return True
    else:
        return False 

def notFound(error):
    return jsonify({'Message':"Error: "+str(error)}), 404

def methodNotAllowed(error):
    return jsonify({'Message':"Error: "+str(error)}), 405

def randomString():
    txt = '1234567890abcdefghijklmnopkrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_'
    log = 20
    secuence = txt.upper()
    txt_result = sample(secuence,log)
    final_txt = "".join(txt_result)
    return final_txt

if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.register_error_handler(404, notFound)
    app.register_error_handler(405, methodNotAllowed)
    app.run()