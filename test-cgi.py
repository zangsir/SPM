#!/usr/bin/python
#import modules for CGI handling 

# Get data from fields
first_name = "Shuo"
last_name="Zhang"
print "Content-type:text/html\r\n\r\n"
print "<html>"
print "<head>"
print "<title>Hello - Second CGI Program</title>"
print "</head>"
print "<body>"
print "<h2>Hello %s %s</h2>" % (first_name, last_name)
print "</body>"
print "</html>"