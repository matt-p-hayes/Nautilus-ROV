import socket	

def socket_send(data, s):

	# send GUI NMEA string
	s.send(data.encode())

	# receive/print ROS response over socket
	print(s.recv(1024).decode())


