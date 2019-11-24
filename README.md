CSC-573 -- INTERNET PROTOCOLS
Instructor - Dr. Muhammad Shazad
Group -3
Group Members : 
Viplove Rakheja
Shelmon Lewis
Aneesh Bhagwat
Nishank Staish

Before starting the project, make sure that the firewall in both server and client side are turned off.
Steps to Run the Projects:
1) Run the two server codes avaiable in the server folder by: 
	1.a) python amazon.py
	1.b) python walmart.py
	Make sure the servers are running continuosly
2) Open the directory Client Side containing a folder name cgi-bin and a HTML file
3) MAke sure the server ip address and the port is same as that in the amazon.py and walmart.py or else the TCP connection will not setup.
3) Open terminal in that directory and type : pyhton -m CGIHTTPServer and press enter
4) Open any web browser application and then type localhost:8000 in the URL bar
5) After pressing enter, a web page will appear with a search bar in it.
6) Enter the product that needs to be searched and press the seach button.
7) Results will be diplayed once the data is received from the servers.
