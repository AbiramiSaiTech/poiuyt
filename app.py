#! /usr/bin/python3
from flask import Flask, request, jsonify,render_template,redirect,url_for,session

import logging





#

import time

import datetime 

from bs4 import BeautifulSoup

import os

import random

from selenium import webdriver

from selenium.webdriver.common.by import By

from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.support.ui import WebDriverWait as wait

from selenium.webdriver.chrome.options import Options

from selenium.webdriver.common.action_chains import ActionChains

import undetected_chromedriver as uc

from selenium import webdriver

import sys



app = Flask(__name__)

DEBUG = True

app.secret_key = 'SAITECHNOLOGIES1'

@app.route('/',methods = ['GET','POST'])	

def login():

	try:

		if request.method == "POST":
			session['password'] = str(request.form.get("ps"))
			session['username'] = str(request.form.get("un"))
			return redirect(url_for("book"))

		else:

			return render_template("login.html")

	except Exception as e:

		print(e)

		#return 'Login Failed!'
		return str(e)

def check_popup(driver):

    try:

        driver.switch_to.alert.accept()

    except Exception as e:

        print(e)

@app.route('/book',methods = ['GET','POST'])	        

def book():

    try:   

        if request.method == "POST":
			#DRiver
            #ipadd_=request.environ.get('HTTP_X_REAL_IP', request.remote_addr)  
            # PROXY="139.99.89.65:8080"
            # webdriver.DesiredCapabilities.CHROME['proxy'] = {"httpProxy": PROXY,"ftpProxy": PROXY, "sslProxy": PROXY,"proxyType": "MANUAL",}
            # webdriver.DesiredCapabilities.CHROME['acceptSslCerts']=True
            options = webdriver.ChromeOptions() 

            options.add_argument("--no-sandbox")

            options.add_argument("--headless")

            #options.add_argument("start-maximized")

            options.add_argument('--disable-automation')
                #options.add_argument('--proxy-server=%s' % PROXY)

            options.add_experimental_option("excludeSwitches", ["enable-automation"])

            options.add_experimental_option('useAutomationExtension', False)
            
            #driver = uc.Chrome(options=options , executable_path=("C:\\Users\\admin\\Downloads\\chromedriver_win32 (6)\\chromedriver.exe"))
            driver = uc.Chrome(options=options,executable_path=('/usr/bin/chromedriver'))
            driver.get("https://gis.sicc.org.sg/?page_id=7709") #https://gis.sicc.org.sg/    
            time.sleep(5)
            #da=driver.find_elements_by_xpath('//*[@id="dropdownCountrySelector"]/span')[0].text
            return driver.page_source

            username = driver.find_element_by_id("user_login")

            username.clear()

            username.send_keys(session['username'])#T0163399

            

            password = driver.find_element_by_name("pwd")

            password.clear()

            password.send_keys(session['password'])#96719280

            

            driver.find_element_by_name("wp-submit").click()
            try:

                gl=driver.find_element_by_link_text("GOLF")



                hover = ActionChains(driver).move_to_element(gl)

                hover.perform()

				

                kl=wait(driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT,"GOLF BOOKING")))

                kl.click()
            except:
                driver.close()
                return("Login Failed")

            import datetime as dd 
            from datetime import datetime  
            oo=driver.find_elements_by_css_selector(".fc-today")
            date=oo[1].get_attribute('data-date') 
            tod=datetime.fromisoformat(date).date()
            d = dd.timedelta(days = 5)
            a = tod + d
            print(a)
            k_val=a.strftime("%d-%B-%Y")
            session['a'] = str(a)
            session['k_val'] = str(k_val)
            

            cour= request.form.get("course")

            tee= request.form.get("ap")

            tee1=request.form.get("tee1")

            tee2=request.form.get("tee2")

            mem1=request.form.get("mem1")

            mem2=request.form.get("mem2")

            mem_cat=request.form.get("mem")

            t=cour+tee
                
            if tee =='a':
    
                s=tee1[:(tee1.index(':')+1)]
    
            else:
    
                s=tee2[:(tee2.index(':')+1)]
    
            print(s)
            while(True):
                try: 
                    l=driver.find_elements_by_xpath("//*[contains(@data-date,'" +str(session["a"])+"')]")
                    if len(l) >= 2: 
                        l[1].click()
                    else:
                        l[0].click()
                    
                    da=driver.find_elements_by_xpath('//*[@id="bkdate"]')
                    
                    if str(session["a"]) == da[0].get_attribute('value'):
                    
                        break
                    
                    else:
                    
                        driver.refresh()
                except Exception as e:

                    return str(e)+" "+str(session["a"])+" l:"+''.join(l)

            cou=driver.find_element_by_xpath('//*[@id="'+t+'"]').click()

            check_popup(driver)

            print(s)

            def check_lot():

                try:

                    id_2=driver.find_elements_by_xpath('//span[starts-with(text(), "'+s+'")]//following::span[2]//a[contains(text(),"Select")]')

                except Exception as e: 

                    id_2=[]

                random.shuffle(id_2)

                return id_2

            try:

            	#check timeslot

            	c=check_lot()

            	while c :

                    try:

                        c[0].click()

                        check_popup()

                    except Exception as e: 

                        c=check_lot()

                        continue

            except:

            	driver.refresh()

            	

            #loop 9 min

            def check_lot_9min():

                t_end = time.time() + 60 * 1

                clicked=False

                while time.time() < t_end:

                    c=check_lot()

                    while c :

                        try:

                            c[0].click()

                            check_popup()

                        except Exception as e: 

                            c=check_lot()

                            continue 

                    try:

                        kl=driver.find_element_by_xpath('//*[@id="gf_booking"]/div[3]/div[2]/div[2]/ul[2]/li[2]/span[1]').click()

                        clicked=True

                        break

                    except:

                        continue

                return clicked

            try:

            	kl=driver.find_element_by_xpath('//*[@id="gf_booking"]/div[3]/div[2]/div[2]/ul[2]/li[2]/span[1]').click()

            except:

                if check_lot_9min():

                    print('yes')

                else:

                    print('no')
                    driver.close()

                    return 'Sorry, Given tee time already allocated!'

            #book

            l=driver.find_element_by_xpath('/html/body/div[1]/form/div[3]/div[2]/div[2]/ul[2]/li[2]/span[1]/div/div[3]/div/ul/li[2]')

            l.click()

            

            name=driver.find_element_by_xpath('/html/body/div[1]/form/div[3]/div[2]/div[2]/ul[2]/li[2]/span[2]/input')

            name.send_keys(mem1)#T0232800

            driver.find_element_by_xpath('//*[@id="gf2_name"]').click()

            

            # name1=driver.find_element_by_xpath('/html/body/div[1]/form/div[3]/div[2]/div[2]/ul[2]/li[2]/span[3]/input').click()

            

            kl=driver.find_element_by_xpath('//*[@id="gf_booking"]/div[3]/div[2]/div[2]/ul[2]/li[3]/span[1]').click()

            time.sleep(2)

            if mem_cat == 'Member':

            

                l=driver.find_element_by_xpath('/html/body/div[1]/form/div[3]/div[2]/div[2]/ul[2]/li[3]/span[1]/div/div[3]/div/ul/li[2]')

                l.click()

                name=driver.find_element_by_xpath('/html/body/div[1]/form/div[3]/div[2]/div[2]/ul[2]/li[3]/span[2]/input')

                name.send_keys(mem2)#T0221888

            else:

                l=driver.find_element_by_xpath('/html/body/div[1]/form/div[3]/div[2]/div[2]/ul[2]/li[3]/span[1]/div/div[3]/div/ul/li[3]')

                l.click()

                name=driver.find_element_by_xpath('/html/body/div[1]/form/div[3]/div[2]/div[2]/ul[2]/li[3]/span[3]/input')

                name.send_keys(mem2)#T0221888

            

            driver.find_element_by_xpath('//*[@id="gf3_name"]').click()

            driver.find_element_by_xpath('//*[@id="gf_booking"]/div[3]/div[2]/div[2]/ul[2]/li[4]/span[1]/div/div[2]/b').click()

            

            val=driver.find_element_by_xpath('//*[@id="gf_booking"]/div[3]/div[1]/div[3]/dl[1]/dd').text

            

            check_popup(driver)

            time.sleep(45)

            check_popup(driver)

            driver.find_element_by_xpath('//*[@id="gf_booking"]/div[3]/div[2]/div[2]/ul[2]/li[5]/span[2]/input').click()

            check_popup(driver)

            time.sleep(45)

            check_popup(driver)

            check_popup(driver)

            try:

            	if driver.find_element_by_xpath('//*[@id="print_area"]/div[2]/div[1]/h4').text == 'My Flights':
                    driver.close()

                    return 'Booking Confirmed Successfully!!'

            except:
                driver.close()

                return 'Member Session not valid, Booking cancelled!!'

        else:
            return render_template("results.html")

    except Exception as e:
        print(e)
        return str(e)+":Last"

        #return 'Not Booked!!  Session cancelled!! '

		

		

if __name__ == '__main__':



    if(DEBUG):

        logging.getLogger().setLevel(logging.DEBUG)

    else:

        logging.getLogger().setLevel(logging.INFO)

    app.run(debug=DEBUG)


