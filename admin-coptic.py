#!//anaconda/bin/python
# -*- coding: UTF-8 -*-

import cgi, cgitb 
import os
from os.path import isfile, join
from os import listdir
from modules.logintools import login
from modules.configobj import ConfigObj
from modules.pathutils import *
import urllib
from modules.coptic_sql import *
from modules.dataenc import pass_dec, pass_enc


def perform_action(text_content, logging=True):
    #this is used to write information into a text file to serve as a debugging tool and log
    #change logging=True to start logging
    if logging:
        f=open("hwak.txt","a")
        f.write('\n')
        f.write(text_content)
        f.close()

def write_user_file(username,password,admin,email,realname,git_username,git_password):
    #this is used to write information into a text file to serve as a debugging tool and log
    #change logging=True to start logging
    userdir="users/"
    f=open(userdir+username+'.ini',"w")
    f.write('username='+username+'\n')
    f.write('password='+pass_enc(password)+'\n')
    f.write('realname='+realname+'\n')
    f.write('admin='+str(admin)+'\n')
    f.write('email='+email+'\n')
    f.write('max-age=0'+'\n')
    f.write('numlogins = 85\nnumused = 2869\n')
    f.write('git_username='+git_username+'\n')
    f.write('git_password='+pass_enc(git_password)+'\n')
    f.close()


def update_password(user,new_pass):
    f=open('users/'+user+'.ini','r')
    ff=f.read().split('\n')
    f.close()

    new_file=[]
    for line in ff:
        if line!='':
            line_split=line.split('=')
            if line_split[0].strip().startswith('password'):
                newline='password = ' + pass_enc(new_pass)
                new_file.append(newline)
            else:
                new_file.append(line)
    open('users/'+user+'.ini', 'w').close()
    g=open('users/'+user+'.ini','a')
    for l in new_file:
        g.write(l+'\n')
    g.close()


def update_git_info(user,new_git_username,new_git_password):
    f=open('users/'+user+'.ini','r')
    ff=f.read().split('\n')
    f.close()

    new_file=[]
    for line in ff:
        if line!='':
            line_split=line.split('=')
            if line_split[0].strip().startswith('git_password'):
                newline='git_password = ' + pass_enc(new_git_password)
                new_file.append(newline)
            elif line_split[0].strip().startswith('git_username'):
                newline='git_username = ' + new_git_username
                new_file.append(newline)
            else:
                new_file.append(line)
    open('users/'+user+'.ini', 'w').close()
    g=open('users/'+user+'.ini','a')
    for l in new_file:
        g.write(l+'\n')
    g.close()





def load_admin(user,admin,theform):
    warn=""
    if theform.getvalue('user_delete'):
        userdir='users/'
        user_del_file=theform.getvalue('user_delete')
        user_del=user_del_file.split('.ini')[0]
        perform_action(user_del)
        #delete_user(user_del)
        #need to also delete the user.ini file
        os.remove(userdir+user_del_file)

    if theform.getvalue('create_user'):
        perform_action('create user')
        
        username=theform.getvalue('username')
        password=theform.getvalue('password')
        realname=theform.getvalue('realname')
        email=theform.getvalue('email')
        admin=theform.getvalue('admin')
        git_username=theform.getvalue('git_username')
        git_password=theform.getvalue('git_password')

        if username!=None and password!=None:

            #create user in database
            #create_user(username)
            #need to write a user file for login tools
            write_user_file(username,password,admin,email,realname,git_username,git_password)
        else:
            warn="</br><b style='color:red;'>ERROR:No username supplied; user cannot be created.</b></br>"

    if theform.getvalue('init_db'):
        perform_action('init db')
        setup_db()

    page= "Content-type:text/html\r\n\r\n"
    page+="""

    <!DOCTYPE html>
    <html>
    <head>
    <style>
    table {
        font-family: arial, sans-serif;
        border-collapse: collapse;
        width:400pt;
    }

    td, th {
        
        text-align: left;
        padding: 8px;
    }

    body{padding:10pt;}

    </style>
    </head>
    <body>

    <h1 >Coptic XML transcription editor</h1> 
        <p style="border-bottom:groove;"><i>administration and user management</i> | <a href="landing.py">back to document list</a> </p>
    
    
    

    """
    page+="""<form action="admin-coptic.py" method='post'>"""

    #page+="""<h2> User Management </h2>"""

    #a list of all users
    page += '''<h2>User Management</h2>
    
    
    <p><h3>Select users to delete:</h3></p>
    <select id="userlist_select" name='user_delete' class="doclist">
    '''
    scriptpath = os.path.dirname(os.path.realpath(__file__)) + os.sep
    userdir = scriptpath + "users" + os.sep

    userfiles = [ f for f in listdir(userdir) if isfile(join(userdir,f)) ]
    for userfile in sorted(userfiles):
        if userfile != "config.ini" and userfile != "default.ini" and userfile != "admin.ini" and userfile.endswith(".ini"):
            userfile = userfile.replace(".ini","")
            page += '<option value="' + userfile + '.ini">'+userfile+'</option>'
    
    page+="</select>"

    
    page+="""</br></br><input type="submit" value='delete user'>
    </form>"""

    #add user

    page+="""</br><h3>Enter user info to create new user:</h3></br><form action='admin-coptic.py' method='post'>
    username <input type='text' name='username'> </br></br>
    password <input type='password' name='password'> </br></br>
    realname <input type='text' name='realname'> </br></br>
    email <input type='text' name='email'> </br></br>
    admin <select name="admin">
    <option value="0">user</option>
    <option value="1">Git committer</option>
    <option value="3">admin-user</option> </select></br></br>
    git username <input type='text' name='git_username'></br></br>
    git password <input type='password' name='git_password'></br></br>




    </br></br><input type='hidden' name='create_user' value='true'><input type='submit' value='create user'></form>"""
    if warn!="":
        page+=warn



    

    page+="<br><br><h2>Database management</h2>"
    #init database, setup_db, wipe all documents

    page+="""<form action='admin-coptic.py' method='post'>
    <b style='color:red'>warning: this will wipe the database!</b>
    <br><input type='hidden' name='init_db' value='true'><input type='submit' value='init database'></form>"""



    page+="</body></html>"
 

    return page


def load_user_config(user,admin,theform):
    if theform.getvalue('new_pass'):
        new_pass=theform.getvalue('new_pass')
        perform_action(new_pass)
        update_password(user,new_pass)
    if theform.getvalue('new_git_password'):

        new_git_password=theform.getvalue('new_git_password')
        new_git_username=theform.getvalue('new_git_username')
        perform_action(new_git_password)
        perform_action(new_git_username)

        update_git_info(user,new_git_username,new_git_password)


    page= "Content-type:text/html\r\n\r\n"
    page+="""

    <!DOCTYPE html>
    <html>
    <head>
    <style>
    table {
        font-family: arial, sans-serif;
        border-collapse: collapse;
        width:400pt;
    }

    td, th {
        
        text-align: left;
        padding: 8px;
    }

    body{padding:10pt;}

    </style>
    </head>
    <body>

    <h1 >Coptic XML transcription editor</h1> 
        <p style="border-bottom:groove;"><i>edit user info</i> | <a href="landing.py">back to document list</a> </p>
    
    <h2>Edit your account information</h2>
    
    
    """
    #edit user password
    username_info="""<table><tr><td>username</td><td>%s</td></tr>"""%user
    username_info+="""
    <form action='admin-coptic.py' method='post'>
    <tr><td>new password</td><td><input type='password' name='new_pass'></td></tr></table>
    
    """
    


    page+=username_info
    page+="<input type='submit' value='change'> </form>"
    page+="</br><p>note: after you changed your password you'll be logged out and you need to log in using your new password again</p>"

    #edit git info
    if admin=="1":
        page+="<form action='admin-coptic.py' method='post'><table><tr><td>new git username</td><td><input type='text' name='new_git_username'></td></tr><tr><td>new git password</td><td><input type='password' name='new_git_password'></td></tr></table>"


        page+="<input type='submit' value='change'> </form>"
    
    page+="</body></html>"

    


    return page

def open_main_server():
    thisscript = os.environ.get('SCRIPT_NAME', '')
    action = None
    theform = cgi.FieldStorage()
    scriptpath = os.path.dirname(os.path.realpath(__file__)) + os.sep
    userdir = scriptpath + "users" + os.sep
    action, userconfig = login(theform, userdir, thisscript, action)
    user = userconfig["username"]
    admin = userconfig["admin"]
    if admin == "3":
        print load_admin(user,admin,theform)
    elif admin == "0" or admin=="1":
        print load_user_config(user,admin,theform)





open_main_server()



