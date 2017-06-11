#!//anaconda/bin/python
# -*- coding: UTF-8 -*-

# Import modules for CGI handling 
import cgi, cgitb 
import os, shutil
from os import listdir
from modules.logintools import login
from modules.configobj import ConfigObj
from modules.pathutils import *
import urllib
from modules.coptic_sql import *
from os.path import isfile, join
from modules.dataenc import pass_dec, pass_enc
import github3
from requests.auth import HTTPBasicAuth
import requests



def make_options(**kwargs):
    if "file" in kwargs:
        names = open(kwargs["file"],'r').read().replace("\r","").split("\n")
        #print len(names)
        names = list(name[:name.find("\t")] for name in names)
    elif "names" in kwargs:
        names = kwargs[names]
    selected = kwargs["selected"] if "selected" in kwargs else None
    options=""
    for name in names:
        if name!='':
            options+='<option value=%s>\n' %name
    return options


def cell(text):
    return "\n    <td>" + str(text) + "</td>"


def perform_action(text_content, logging=True):
    #this is used to write information into a text file to serve as a debugging tool and log
    #change logging=True to start logging
    if logging:
        f=open("hwak.txt","a")
        f.write('\n')
        f.write(text_content.encode("utf8"))
        f.close()






def serialize_file(text_content,file_name):
    f=open(file_name,'w')
    f.write(text_content.encode("utf8"))
    f.close()




def load_page(user,admin,theform):
    perform_action('===========new=============')
    if theform.getvalue('ts_repr'):
        doc_id=theform.getvalue('ts_repr')
        perform_action(doc_id)
    if theform.getvalue('dist'):
        doc_id=theform.getvalue('dist')
        perform_action(doc_id)
    if theform.getvalue('QBC'):
        doc_id=theform.getvalue('QBC')
        perform_action(doc_id)

    page_content="""<table style="background:#eee;padding:5pt;">

<form action='editor.py' method="post">
<table>

<tr>
<td>TS representation:</td>
<td>
  <select name="ts_repr">
    <option value="F0">F0</option>
    <option value="SAX">SAX</option>

</td>
</tr>
<tr>
<td>distance measure:</td>
<td>
  </select>
    <select name="dist">
    <option value="euclidean">euclidean</option>
    <option value="MIN-DIST">MIN-DIST</option>
    
  </select>
  <br><br>
  
</td></tr>
</table>
<input type='submit' name='QBC' value='QBC'>
</form>"""


    

    page= "Content-type:text/html\r\n\r\n"
    page+= urllib.urlopen("editor_codemir.html").read()
    #page=page.replace("**content**",text_content)
    #page=page.replace("**docname**",doc_name)
    #page=page.replace("**filename**",repo_name)
    #page=page.replace("**assigned**",assignee)
    #page=page.replace("**status**",status)
    #page=page.replace("**editdocname**",edit_docname)
    page=page.replace("**editstatus**",page_content)
    #page=page.replace("**editfilename**",edit_filename)
    #page=page.replace("**editassignee**",edit_assignee)
    #page=page.replace("**metadata**",metadata)
    #page=page.replace("**NLP**",nlp_service)
    #if int(admin)>0:
     #   page=page.replace("**github**",push_git)
    #else:
     #   page = page.replace("**github**", '')
    #page=page.replace("**js**",js)

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
    print load_page(user,admin,theform).encode("utf8")


open_main_server()