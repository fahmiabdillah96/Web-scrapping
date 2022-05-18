# Load selenium components
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import pandas as pd
import numpy as np


# Establish web driver and go to report site URL
url = "http://surveilans-dinkesdki.net/rekap_harian.php"
driver = webdriver.Chrome(r'driver\chromedriver.exe')
driver.get(url)

rb = driver.find_element(By.CSS_SELECTOR, ("input[type='radio'][value='2'][name='radiobutton']"))
rb.click()

#Get Kota
kota = driver.find_element(By.NAME, "KODYA")
drp_kota = Select(kota)
drp_kota.select_by_index(1) #index 1 = kota jakarta pusat
nama_kota = drp_kota.first_selected_option
nama_kota = nama_kota.text



# select bulan
rb2 = driver.find_element(By.CSS_SELECTOR, ("input[type='radio'][value='3'][name='radiobutton1']"))
rb2.click()

# get the structured dummy data
data_prev = pd.read_csv('data\Rekap_RS_new.csv')

for m in range(0,12):
    # GET BULAN TAHUN
    year = 2016 #year to access
    bulan = driver.find_element(By.NAME, "BBULANS")
    bulan2 = driver.find_element(By.NAME, "BBULANE")

    drp_bulan = Select(bulan)
    drp_bulan.select_by_index(m)
    nama_bulan = drp_bulan.first_selected_option
    nama_bulan = nama_bulan.text

    drp_bulan2 = Select(bulan2)
    drp_bulan2.select_by_index(m)

    drp_tahun = driver.find_element(By.NAME, "BTAHUN")
    drp_tahun.clear()
    drp_tahun.send_keys(str(year))

    list_p =[]

    cbpenyakit = driver.find_element(By.CSS_SELECTOR,
                                     ("input[type='checkbox'][value='checkbox'][name='CBPENYAKIT']"))
    cbpenyakit.click()

    for e in range(1, 35):
        # Get penyakit
        penyakit = driver.find_element(By.NAME, "PENYAKIT")
        drp_penyakit = Select(penyakit)
        drp_penyakit.select_by_index(e)

        # click submit
        submit = driver.find_element(By.CSS_SELECTOR, "input[type='submit'][name='SUBMIT']")
        submit.click()

        xpath_total = "//tbody/tr[2]/td/table/tbody/tr/td/table[3]/tbody/tr[12]/td[3]/div"
        total_penyakit = driver.find_element(By.XPATH, xpath_total)
        total_penyakit2 = total_penyakit.text

        if total_penyakit2 == "0":
            list_p.append(e)


    cbpenyakit = driver.find_element(By.CSS_SELECTOR,
                                     ("input[type='checkbox'][value='checkbox'][name='CBPENYAKIT']"))
    cbpenyakit.click()
    print(list_p)

    # Get RS
    cbrs = driver.find_element(By.CSS_SELECTOR, ("input[type='checkbox'][value='checkbox'][name='CBRS']"))
    cbrs.click()

    ignore = [41,162]  # list of indices to be ignored (hospital outside jakarta)
    l = [ind for ind in range(1,171) if ind not in ignore]


    for z in l:
        rs = driver.find_element(By.NAME, "RS")
        drp_rs = Select(rs)
        drp_rs.select_by_index(z) #index
        nama_rs = drp_rs.first_selected_option
        nama_rs = nama_rs.text

        # click submit
        submit = driver.find_element(By.CSS_SELECTOR, "input[type='submit'][name='SUBMIT']")
        submit.click()

        xpath_total = "//tbody/tr[2]/td/table/tbody/tr/td/table[3]/tbody/tr[12]/td[3]/div"
        total = driver.find_element(By.XPATH, xpath_total)
        total2 = total.text
        print(total2,":", end=' ')

        if total2 != "0":
            print(nama_kota, nama_rs, nama_bulan, year)
            peny = [ind for ind in range(1, 35) if ind not in list_p]
            for d in peny:
                cbpenyakit = driver.find_element(By.CSS_SELECTOR, ("input[type='checkbox'][value='checkbox'][name='CBPENYAKIT']"))
                cbpenyakit.click()

                # Get penyakit
                penyakit = driver.find_element(By.NAME, "PENYAKIT")
                drp_penyakit = Select(penyakit)
                drp_penyakit.select_by_index(d)  # index penyakit
                nama_penyakit = drp_penyakit.first_selected_option
                nama_penyakit = nama_penyakit.text

                # click submit
                submit = driver.find_element(By.CSS_SELECTOR, "input[type='submit'][name='SUBMIT']")
                submit.click()

                xpath_total = "//tbody/tr[2]/td/table/tbody/tr/td/table[3]/tbody/tr[12]/td[3]/div"
                total_p = driver.find_element(By.XPATH, xpath_total)
                total_p2 = total_p.text
                print(nama_penyakit, ":", total_p2)

                if total_p2 != "0":
                    cbumur = driver.find_element(By.CSS_SELECTOR, ("input[type='checkbox'][value='checkbox'][name='CBUMUR']"))
                    cbumur.click()

                    cbkel = driver.find_element(By.CSS_SELECTOR, ("input[type='checkbox'][value='checkbox'][name='CBKELAMIN']"))
                    cbkel.click()

                    data_temp = pd.DataFrame(columns=['KECAMATAN'])

                    for i in range(1,11):

                        #Get umur
                        umur = driver.find_element(By.NAME, "UMUR")
                        drp_umur = Select(umur)
                        drp_umur.select_by_index(i) #index 1
                        umur2 = drp_umur.first_selected_option
                        umur2 = umur2.text

                        jkel = ["L","P"]

                        for k in jkel:
                            jk = driver.find_element(By.NAME, "KELAMIN")
                            drp_jk = Select(jk)
                            drp_jk.select_by_value(k) #index 1
                            jenis_kelamin = drp_jk.first_selected_option
                            jenis_kelamin = jenis_kelamin.text

                            # click submit
                            submit = driver.find_element(By.CSS_SELECTOR, "input[type='submit'][name='SUBMIT']")
                            submit.click()


                            xpath_1 = "//tbody/tr[2]/td/table/tbody/tr/td/table[3]/tbody/tr["
                            xpath_2 = "]/td["
                            xpath_3 = "]/div"

                            total_path="//tbody/tr[2]/td/table/tbody/tr/td/table[3]/tbody/tr[12]/td[3]/div"
                            total_s = driver.find_element(By.XPATH, total_path)
                            total_ss = total_s.text

                            value1=[]
                            if total_ss != "0":
                                for r in range(1,12):
                                    value2=[]
                                    for c in range(2,4):
                                        final = xpath_1 + str(r) + xpath_2 + str(c) + xpath_3
                                        val = driver.find_element(By.XPATH, final)
                                        val2 = val.text
                                        value2.append(val2)
                                    value1.append(value2)


                                df = pd.DataFrame(value1)

                                new_header = [df.iloc[0,0], str(umur2+"_"+k)]  # grab the first row for the header
                                df = df[1:]  # take the data less the header row
                                df.columns = new_header  # set the header row as the df header


                                data_temp=data_temp.merge(df, on='KECAMATAN', how='outer')



                    # get the name of kota, kecamatan, and bulan of this loop
                    list_kota = []
                    list_penyakit = []
                    list_bulan = []
                    tahun = []
                    list_rs = []

                    for i in range(10):  # means the number of rows in 1 table
                        list_kota.append(nama_kota)
                        list_penyakit.append(nama_penyakit)
                        list_bulan.append(nama_bulan)
                        tahun.append(year)
                        list_rs.append(nama_rs)

                    # merge no and jenis penyakit
                    df_wilayah = pd.DataFrame({'KOTA': list_kota, 'JENIS PENYAKIT': list_penyakit,
                                                'RUMAH SAKIT': list_rs, 'BULAN': list_bulan, 'TAHUN': tahun})
                    data_sementara = df_wilayah.join(data_temp)

                    data_prev = pd.concat([data_prev,data_sementara])


                    cbumur = driver.find_element(By.CSS_SELECTOR, ("input[type='checkbox'][value='checkbox'][name='CBUMUR']"))
                    cbumur.click()

                    cbkel = driver.find_element(By.CSS_SELECTOR, ("input[type='checkbox'][value='checkbox'][name='CBKELAMIN']"))
                    cbkel.click()

                penyakit = driver.find_element(By.NAME, "PENYAKIT")
                drp_penyakit = Select(penyakit)
                drp_penyakit.select_by_value("0")  # index penyakit

                cbpenyakit = driver.find_element(By.CSS_SELECTOR, ("input[type='checkbox'][value='checkbox'][name='CBPENYAKIT']"))
                cbpenyakit.click()
            data_prev.to_csv('data\Rekap_RS_Jaksel_{}_{}{}.csv'.format(nama_rs, nama_bulan, year), index=False)
        elif total2=="0":
            print(nama_kota, nama_rs, nama_bulan, year)
    # Get RS
    cbrs = driver.find_element(By.CSS_SELECTOR, ("input[type='checkbox'][value='checkbox'][name='CBRS']"))
    cbrs.click()


