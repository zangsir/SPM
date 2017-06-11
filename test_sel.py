#!/usr/bin/python

# Import modules for CGI handling 
import cgi, cgitb 

# Create instance of FieldStorage 
form = cgi.FieldStorage() 


# Get data from fields
if form.getvalue('dropdown'):
    first_name = form.getvalue('dropdown')
else:
	first_name = 'nothing'

print "Content-type:text/html\r\n\r\n"
print "<html>"
print "<head>"
print "<title>Hello - Second CGI Program</title>"
print "</head>"
print "<body>"
print "<h2>Hello %s</h2>" %first_name
print "</body>"
print "</html>"