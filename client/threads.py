#!/usr/bin/env python
# coding: utf-8
from decorators import async, run_thread
from concretefactory.ultrasonicSensorFactory import UltrasonicSensorFactory
from concretefactory.motionSensorFactory import MotionSensorFactory
from concretefactory.humiditySensorFactory import HumididtySensorFactory
from concretefactory.temperatureSensorFactory import TemperatureSensorFactory

import time, datetime, random, sqlite3
import RPi.GPIO as GPIO 

#Arquivo de banco de dados do SQLite
dbname='sensores.sqlite'

SLEEPTIME_DISTANCIA = 3
SLEEPTIME_TEMPERATURA_UMIDADE = 5
SLEEPTIME_MOVIMENTO = 2

#@async
@run_thread
def create_async_sensor(condition,sensor_id, tipo, portas,db_get_sensor_type):
	
	#if (db_get_sensor_type(sensor_id) == None):
	#	this.exit();
	
	# try:
		if(tipo == "sr04"):
			try:
				srf04 = UltrasonicSensorFactory.createSensor("SRF04")
				srf04.changeSetup(int(portas["echo"]), int(portas["trigger"]))
				srf04.setup()
				while (True):
					if (db_get_sensor_type(sensor_id) == None):
						exit()

					condition.acquire()
					print "Capturando dados de distancia (SRF04 #"+str(sensor_id)+"_e:"+portas["echo"]+",t:"+portas["trigger"]+")"
					distancia_cm = round(srf04.distance_in_cm(),2)
					gravar_dados_sensor((sensor_id, distancia_cm, "cm", "Distancia", datetime.datetime.now()))
					condition.notify()
					condition.release()
					time.sleep(SLEEPTIME_DISTANCIA)
			finally:
				print 'Fim'  
				GPIO.cleanup() 
		
		if(tipo == "sr05"):
				try:
					srf05 = UltrasonicSensorFactory.createSensor("SRF05")
					srf05.changeSetup(int(portas["echo"]), int(portas["trigger"]))
				 	srf05.setup()
					while (True):
						if (db_get_sensor_type(sensor_id) == None):
							exit()

						condition.acquire()
						print "Capturando dados de distancia (sr05 #"+str(sensor_id)+"_e:"+portas["echo"]+",t:"+portas["trigger"]+")"
						distancia_cm = round(srf04.distance_in_cm(),2)
						gravar_dados_sensor((sensor_id, distancia_cm, "cm", "Distancia", datetime.datetime.now()))
						condition.notify()
						condition.release()
						time.sleep(SLEEPTIME_DISTANCIA)
				finally:
					print 'Fim'  
					GPIO.cleanup()  

		if(tipo == "pir"):
				try:
					pir = MotionSensorFactory.createSensor("PIR")
					pir.changeSetup(int(portas["data"]))
				 	pir.setup()
					while (True):
						if (db_get_sensor_type(sensor_id) == None):
							exit()

						condition.acquire()
						print "Capturando dados de movimento (PIR #"+str(sensor_id)+"_d:"+portas["data"]+")"
						moviment = pir.isMotionDetected()
						gravar_dados_sensor((sensor_id, moviment, "n/a", "Movimento", datetime.datetime.now()))
						condition.notify()
						condition.release()
						time.sleep(SLEEPTIME_MOVIMENTO)
				finally:
					print 'Fim'  
					GPIO.cleanup() 

		if(tipo == "dht11"):
				try:
					dht11_H = HumididtySensorFactory.createSensor("DHT11Humididty")
					dht11_H.changeSetup(int(portas["data"]))
					dht11_H.setup()
					dht11_T = TemperatureSensorFactory.createSensor("DHT11Temperature")
					dht11_T.changeSetup(int(portas["data"]))
					dht11_T.setup() 
					while (True):
						if (db_get_sensor_type(sensor_id) == None):
							exit()

						condition.acquire()      
						print "Capturando dados de umidade e temperatura (DHT11 #"+str(sensor_id)+"_d:"+portas["data"]+")"
						temperature = dht11_T.getTemperature()
						gravar_dados_sensor((sensor_id, temperature, "C", "Temperatura", datetime.datetime.now()))
						humidity = dht11_H.getHumidity()
						gravar_dados_sensor((sensor_id, humidity, "%", "Humidade", datetime.datetime.now()))   
						condition.notify()
						condition.release()
						time.sleep(SLEEPTIME_TEMPERATURA_UMIDADE)
				finally:
					print 'Fim'  
				 	GPIO.cleanup()  
	# except (KeyboardInterrupt, SystemExit):
	# 	raise 
	# except Exception, e:
 #    print e.getMessage() 
	# 	print "Matando thread"

# store the temperature in the database
def gravar_dados_sensor(values=()):
		conn=sqlite3.connect(dbname)
		cur=conn.cursor()
		query = 'INSERT INTO LOG (id_sensor, valor, unidade, variavel, data) VALUES (%s)' % (
				', '.join(['?'] * len(values))
		)
		cur.execute(query, values)
		conn.commit()
		id = cur.lastrowid
		cur.close()
		conn.close()
		return id
