# HTTP Payload
Checking HTTP Request Response for Search HTTP Injector BUG with python requests

<h3>How to Use</h3>
Checking with direct method :  
<li>python httpay.py --url www.bug.com</li><br>

Checking with remote proxy method :
<li>python httpay.py --url www.bug.com --proxy ip:port</li>

<br>You can using txt file to check two or more website :
<li>python python httpay.pay --file bug.txt</li><br>

After checking the website bug, the program automatically create the report result.txt
if you want name it manually you can using --result argument
<li>python python httpay.pay --file bug.txt --result report.txt</li><br>

<h3>Notes</h3>
Some internet provider have default proxy although in direct connection, this default proxy make different result with direct result with no default proxy. You can search the default proxy for your internet provider.