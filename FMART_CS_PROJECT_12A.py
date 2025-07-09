from captcha.image import ImageCaptcha
import tkinter as tk
import tkinter.font as font
from tkinter import messagebox
from tkinter import scrolledtext
import sqlite3
from PIL import ImageTk,Image
import random as r
import matplotlib.pyplot as plt
import datetime as dt

database_name='fmart.db'
emp_filename='emp_files\\'
image_name='FMART_LOGO_1.png'
icon_name='FMART_ICON.ico'
captcha_name='login_captcha.png'
window_bg_color='#a1cbf6'
button_bg_color='#a1cbf6'
button_fg_color='#26664f'

#this function generates the random text for the captcha.
def create_captcha_content():
    c1=chr(r.randint(65,90))
    c2=chr(r.randint(65,90))
    n1=str(r.randint(1,9))
    c3=chr(r.randint(65,90))
    c4=chr(r.randint(65,90))
    n2=str(r.randint(1,9))
    c5=chr(r.randint(65,90))
    c6=chr(r.randint(65,90))
    captcha_content=c1+c2+n1+c3+c4+n2+c5+c6
    return captcha_content
captcha_content=create_captcha_content()

#this function generates the actual captcha image.
def create_captcha_image(x):
    image = ImageCaptcha(width=400, height=180)
    captcha_content = x
    image.generate(captcha_content)
    image.write(captcha_content,captcha_name)
create_captcha_image(captcha_content)

#this function creates the main homepage window.
def create_main_login_window():
    login_window=tk.Tk()
    login_window.title('FMART')
    login_window.iconbitmap(icon_name)
    login_window['background']=window_bg_color
    width=login_window.winfo_screenwidth()-40
    height=login_window.winfo_screenheight()-40
    login_window.geometry('%dx%d'%(width,height))
    buttonfont=font.Font(family='Bahnschrift',size=40,weight='bold')
    img=Image.open(image_name)
    res_img=img.resize((500,400), Image.ANTIALIAS)
    logo_image=ImageTk.PhotoImage(res_img)
    logo_label=tk.Label(login_window,image=logo_image,borderwidth=0)
    logo_label.grid(row=0,column=0,columnspan=3,padx=100)
    supervisor_login_button=tk.Button(login_window,text='Supervisor Login',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont,command=lambda: [login_window.destroy(),create_supervisor_login()])
    supervisor_login_button.grid(row=1,column=0,padx=75,pady=75)
    about_us_button=tk.Button(login_window,text='About Us',width=10,bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont,command=lambda: [login_window.destroy(),create_about_us()])
    about_us_button.grid(row=1,column=1,pady=75)
    cashier_login_button=tk.Button(login_window,text='Cashier Login',width=15,bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont,command=lambda: [login_window.destroy(),create_cashier_login()])
    cashier_login_button.grid(row=1,column=2,pady=75)
    login_window.mainloop()

#this function creates the supervisor login page.
def create_supervisor_login():
    #this function verifies if username, password and captcha entered are correct.
    def supervisor_login_verification():
        try:
            global current_supervisor_user, captcha_content
            conn=sqlite3.connect(database_name)
            cur=conn.cursor()
            cur.execute('SELECT PASSWORD FROM SUPERVISOR WHERE USERNAME=?',(username_var.get(),))
            password_details=cur.fetchone()[0]
            conn.close()
            if password_details==password_var.get() and captcha_content==captcha_var.get():
                conn=sqlite3.connect(database_name)
                cur=conn.cursor()
                cur.execute('SELECT SUP_ID FROM SUPERVISOR WHERE USERNAME=?',(username_var.get(),))
                current_supervisor_user=cur.fetchall()[0][0]
                conn.close()
                supervisor_login.destroy()
                create_supervisor_homepage()
            elif password_details!=password_var.get() and captcha_content==captcha_var.get():
                messagebox.showinfo('Login Failed','Failed to login\nPassword details incorrect.\nPlease try again.')
            elif password_details==password_var.get() and captcha_content!=captcha_var.get():
                messagebox.showinfo('Login Failed','Failed to login\nCaptcha details incorrect.\nPlease try again.')
            else:
                messagebox.showinfo('Login Failed','Failed to login\nPassword and captcha details incorrect.\nPlease try again.')
        except TypeError:
                messagebox.showinfo('Login Failed','Failed to login\nNo such username exists.\nPlease try again.')
    supervisor_login=tk.Tk()
    supervisor_login.title('SUPERVISOR LOGIN')
    supervisor_login.iconbitmap(icon_name)
    supervisor_login['background']=window_bg_color
    width=supervisor_login.winfo_screenwidth()-40
    height=supervisor_login.winfo_screenheight()-40
    supervisor_login.geometry('%dx%d'%(width,height))
    contentfont=font.Font(family='Bahnschrift',size=30,weight='bold')
    username_label=tk.Label(supervisor_login,text='Enter Username:',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=contentfont)
    username_label.grid(row=0,column=0,padx=15,pady=15)
    password_label=tk.Label(supervisor_login,text='Enter Password:',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=contentfont)
    password_label.grid(row=1,column=0,padx=15,pady=15)
    img=Image.open(captcha_name)
    display_img=ImageTk.PhotoImage(img)
    captcha_img_label=tk.Label(supervisor_login,image=display_img,bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=contentfont)
    captcha_img_label.grid(row=2,column=0,columnspan=2,padx=15,pady=15)
    captcha_label=tk.Label(supervisor_login,text='Enter Captcha:',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=contentfont)
    captcha_label.grid(row=3,column=0,padx=15,pady=15)
    username_var=tk.StringVar()
    username_entry=tk.Entry(supervisor_login,textvariable=username_var,font=contentfont)
    username_entry.grid(row=0,column=1,padx=15,pady=15)
    password_var=tk.StringVar()
    password_entry=tk.Entry(supervisor_login,textvariable=password_var,font=contentfont)
    password_entry.grid(row=1,column=1,padx=15,pady=15)
    captcha_var=tk.StringVar()
    captcha_entry=tk.Entry(supervisor_login,textvariable=captcha_var,font=contentfont)
    captcha_entry.grid(row=3,column=1,padx=15,pady=15)
    login_button=tk.Button(supervisor_login,text='Login',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=contentfont,command=supervisor_login_verification)
    login_button.grid(row=4,column=0,padx=15,pady=15)
    signup_button=tk.Button(supervisor_login,text='Sign Up',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=contentfont,command=lambda: [supervisor_login.destroy(),create_sign_up()])
    signup_button.grid(row=4,column=1,padx=15,pady=15)
    main_login_return_button=tk.Button(supervisor_login,text='Back',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=contentfont,command=lambda: [supervisor_login.destroy(),create_main_login_window()])
    main_login_return_button.grid(row=0,column=2,padx=40,pady=15)
    supervisor_login.mainloop()
    
#this function creates the sign up page for supervisors.        
def create_sign_up():
    sign_up=tk.Tk()
    sign_up.title('SIGN UP')
    sign_up.iconbitmap(icon_name)
    sign_up['background']=window_bg_color
    width=sign_up.winfo_screenwidth()-40
    height=sign_up.winfo_screenheight()-40
    sign_up.geometry('%dx%d'%(width,height))
    buttonfont=font.Font(family='Bahnschrift',size=40,weight='bold')
    contentfont=font.Font(family='Bahnschrift',size=30,weight='bold')
    selectionfont=font.Font(family='Bahnschrift',size=20,weight='bold')
    name_label=tk.Label(sign_up,text='Enter Name:',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=contentfont)
    name_label.grid(row=0,column=0)
    DOB_label=tk.Label(sign_up,text='Enter DOB as YYYY-MM-DD :',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=contentfont)
    DOB_label.grid(row=1,column=0)
    age_label=tk.Label(sign_up,text='Enter age:',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=contentfont)
    age_label.grid(row=2,column=0)
    gender_label=tk.Label(sign_up,text='Enter gender (M/F) :',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=contentfont)
    gender_label.grid(row=3,column=0)
    address_label=tk.Label(sign_up,text='Enter address:',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=contentfont)
    address_label.grid(row=4,column=0)
    ph_no_label=tk.Label(sign_up,text='Enter Phone Number:',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=contentfont)
    ph_no_label.grid(row=5,column=0)
    email_label=tk.Label(sign_up,text='Enter email ID:',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=contentfont)
    email_label.grid(row=6,column=0)
    username_label=tk.Label(sign_up,text='Enter Username:',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=contentfont)
    username_label.grid(row=7,column=0)
    password_label=tk.Label(sign_up,text='Enter Password:\nMaximum of 18 characters',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=contentfont)
    password_label.grid(row=8,column=0)
    name_var=tk.StringVar()
    name_entry=tk.Entry(sign_up,textvariable=name_var,font=contentfont)
    name_entry.grid(row=0,column=1)
    DOB_var=tk.StringVar()
    DOB_entry=tk.Entry(sign_up,textvariable=DOB_var,font=contentfont)
    DOB_entry.grid(row=1,column=1)
    age_var=tk.StringVar()
    age_entry=tk.Entry(sign_up,textvariable=age_var,font=contentfont)
    age_entry.grid(row=2,column=1)
    gender_var=tk.StringVar()
    gender_entry=tk.Entry(sign_up,textvariable=gender_var,font=contentfont)
    gender_entry.grid(row=3,column=1)
    address_entry=scrolledtext.ScrolledText(sign_up,font=selectionfont,height=2,width=28)
    address_entry.grid(row=4,column=1)
    ph_no_var=tk.StringVar()
    ph_no_entry=tk.Entry(sign_up,textvariable=ph_no_var,font=contentfont)
    ph_no_entry.grid(row=5,column=1)
    email_var=tk.StringVar()
    email_entry=tk.Entry(sign_up,textvariable=email_var,font=contentfont)
    email_entry.grid(row=6,column=1)
    username_var=tk.StringVar()
    username_entry=tk.Entry(sign_up,textvariable=username_var,font=contentfont)
    username_entry.grid(row=7,column=1)
    password_var=tk.StringVar()
    password_entry=tk.Entry(sign_up,textvariable=password_var,font=contentfont)
    password_entry.grid(row=8,column=1)
    #this function adds the new supervisor record to the supervisor table
    def update():
        conn=sqlite3.connect(database_name)
        cur=conn.cursor()
        cur.execute('SELECT * FROM SUPERVISOR')
        rows=cur.fetchall()
        conn.close()
        last_id=rows[-1][0]
        generated_id='SP'+str(int(last_id.replace('SP',''))+1)
        conn=sqlite3.connect(database_name)
        cur=conn.cursor()
        cur.execute('SELECT USERNAME FROM SUPERVISOR')
        username_data=cur.fetchall()
        conn.close()
        username_list=[]
        for i in username_data:
            username_list.append(i[0])
        if username_var.get() not in username_list:
            conn=sqlite3.connect(database_name)
            cur=conn.cursor()
            cur.execute('INSERT INTO SUPERVISOR VALUES(?,?,?,?,?,?,?,?,?,?)',(generated_id,name_var.get(),DOB_var.get(),age_var.get(),gender_var.get(),address_entry.get('1.0','end-1c'),ph_no_var.get(),email_var.get(),username_var.get(),password_var.get()))
            conn.commit()
            conn.close()
            messagebox.showinfo('Success','You have succesfully signed up\nClick OK to proceed')
            sign_up.destroy()
            create_supervisor_login()
        else:
            messagebox.showinfo('Sign Up Failed','Failed to Sign Up\nUsername already exists.\nPlease enter again.')
    main_login_return_button=tk.Button(sign_up,text='Sign Up',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont,command=update)
    main_login_return_button.grid(row=9,column=0,pady=15,padx=15)

#this function creates the cashier login page.
def create_cashier_login():
    #this function verifies if username, password and captcha entered are correct.
    def cashier_login_verification():
        global current_cashier_user
        try:    
            conn=sqlite3.connect(database_name)
            cur=conn.cursor()
            cur.execute('SELECT PASSWORD FROM EMPLOYEE WHERE USERNAME=?',(username_var.get(),))
            password_details=cur.fetchone()[0]
            conn.close()
            if password_details==password_var.get() and captcha_content==captcha_var.get():
                conn=sqlite3.connect(database_name)
                cur=conn.cursor()
                cur.execute('SELECT * FROM EMPLOYEE WHERE USERNAME=?',(username_var.get(),))
                current_cashier_user=cur.fetchall()[0][0]
                conn.close()
                cashier_login.destroy()
                create_cashier_homepage()
            elif password_details!=password_var.get() and captcha_content==captcha_var.get():
                messagebox.showinfo('Login Failed','Failed to login\nPassword details incorrect.\nPlease try again.')
            elif password_details==password_var.get() and captcha_content!=captcha_var.get():
                messagebox.showinfo('Login Failed','Failed to login\nCaptcha details incorrect.\nPlease try again.')
            else:
                messagebox.showinfo('Login Failed','Failed to login\nPassword and captcha details incorrect.\nPlease try again.')
        except TypeError:
                messagebox.showinfo('Login Failed','Failed to login\nNo such username exists.\nPlease try again.')
    cashier_login=tk.Tk()
    cashier_login.title('CASHIER LOGIN')
    cashier_login.iconbitmap(icon_name)
    cashier_login['background']=window_bg_color
    width=cashier_login.winfo_screenwidth()-40
    height=cashier_login.winfo_screenheight()-40
    cashier_login.geometry('%dx%d'%(width,height))
    contentfont=font.Font(family='Bahnschrift',size=30,weight='bold')
    username_label=tk.Label(cashier_login,text='Enter Username:',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=contentfont)
    username_label.grid(row=0,column=0,padx=15,pady=15)
    password_label=tk.Label(cashier_login,text='Enter Password:',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=contentfont)
    password_label.grid(row=1,column=0,padx=15,pady=15)
    img=Image.open(captcha_name)
    display_img=ImageTk.PhotoImage(img)
    captcha_img_label=tk.Label(cashier_login,image=display_img,bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=contentfont)
    captcha_img_label.grid(row=2,column=0,columnspan=2,padx=15,pady=15)
    captcha_label=tk.Label(cashier_login,text='Enter Captcha:',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=contentfont)
    captcha_label.grid(row=3,column=0,padx=15,pady=15)
    username_var=tk.StringVar()
    username_entry=tk.Entry(cashier_login,textvariable=username_var,font=contentfont)
    username_entry.grid(row=0,column=1,padx=15,pady=15)
    password_var=tk.StringVar()
    password_entry=tk.Entry(cashier_login,textvariable=password_var,font=contentfont)
    password_entry.grid(row=1,column=1,padx=15,pady=15)
    captcha_var=tk.StringVar()
    captcha_entry=tk.Entry(cashier_login,textvariable=captcha_var,font=contentfont)
    captcha_entry.grid(row=3,column=1,padx=15,pady=15)
    login_button=tk.Button(cashier_login,text='Login',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=contentfont,command=cashier_login_verification)
    login_button.grid(row=4,column=0,padx=15,pady=15)
    main_login_return_button=tk.Button(cashier_login,text='Back',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=contentfont,command=lambda: [cashier_login.destroy(),create_main_login_window()])
    main_login_return_button.grid(row=0,column=2,padx=40,pady=15)
    cashier_login.mainloop()

#this function creates the 'about us' page.       
def create_about_us():
    about_us=tk.Tk()
    about_us.title('ABOUT US')
    about_us.iconbitmap(icon_name)
    about_us['background']=window_bg_color
    width=about_us.winfo_screenwidth()-40
    height=about_us.winfo_screenheight()-40
    about_us.geometry('%dx%d'%(width,height))
    buttonfont=font.Font(family='Bahnschrift',size=30,weight='bold')
    img=Image.open(image_name)
    res_img=img.resize((250,180), Image.ANTIALIAS)
    logo_image=ImageTk.PhotoImage(res_img)
    l1=tk.Label(about_us,image=logo_image,borderwidth=0)
    l1.grid(row=0,column=0,columnspan=3)
    contentfont=font.Font(family='Bahnschrift',size=22)
    about_us_content='''Welcome to the FMART About Us Page!
    
    FMART (Fresh-MART) is a project that involves the creation of a supermarket management system
    using python and python-SQL connectivity.
    
    FMART offers a wide range of products including but not limited to fruits, vegetables
    dairy products, spices and grains.
    
    Thank you!
    
    The FMART Team
    '''
    about_us_textlabel=tk.Label(about_us,bg=button_bg_color,fg=button_fg_color,text=about_us_content,borderwidth=0,font=contentfont)
    about_us_textlabel.grid(row=1,column=0,columnspan=3,pady=2)
    back_button=tk.Button(about_us,text='Back',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont,command=lambda: [about_us.destroy(),create_main_login_window()])
    back_button.grid(row=2,column=2,pady=4)
    about_us.mainloop()

#this function creates the supervisor homepage window.
def create_supervisor_homepage():
    supervisor_homepage=tk.Tk()
    supervisor_homepage.title('HOME - SUPERVISOR ACCOUNT')
    supervisor_homepage.iconbitmap(icon_name)
    supervisor_homepage['background']=window_bg_color
    width=supervisor_homepage.winfo_screenwidth()-40
    height=supervisor_homepage.winfo_screenheight()-40
    supervisor_homepage.geometry('%dx%d'%(width,height))
    labelfont=font.Font(family='Bahnschrift',size=40,weight='bold',underline=1)
    buttonfont=font.Font(family='Bahnschrift',size=34,weight='bold')
    header_label=tk.Label(supervisor_homepage,text='SUPERVISOR HOMEPAGE',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=labelfont)
    header_label.grid(row=0,column=0,padx=15,pady=15,columnspan=2)
    view_supervisor_profile=tk.Button(supervisor_homepage,text='VIEW PROFILE',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont,command=lambda: [supervisor_homepage.destroy(),create_supervisor_view_profile()])
    view_supervisor_profile.grid(row=1,column=0,padx=15,pady=15)
    view_employee_data=tk.Button(supervisor_homepage,text='VIEW EMPLOYEE DATA',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont,command=lambda: [supervisor_homepage.destroy(),create_supervisor_view_cashiers()])
    view_employee_data.grid(row=2,column=0,padx=15,pady=15)
    view_customer_data=tk.Button(supervisor_homepage,text='VIEW CUSTOMER DATA',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont,command=lambda: [supervisor_homepage.destroy(),create_supervisor_customer_data()])
    view_customer_data.grid(row=3,column=0,padx=15,pady=15)
    view_product_inventory=tk.Button(supervisor_homepage,text='VIEW PRODUCT INVENTORY',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont,command=lambda: [supervisor_homepage.destroy(),create_supervisor_inventory()])
    view_product_inventory.grid(row=4,column=0,padx=15,pady=15)
    set_discount_rate=tk.Button(supervisor_homepage,text='SET DISCOUNT RATE',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont,command=lambda: [supervisor_homepage.destroy(),create_supervisor_discount_rate()])
    set_discount_rate.grid(row=5,column=0,padx=15,pady=15)
    send_message=tk.Button(supervisor_homepage,text='SEND MESSAGE',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont,command=lambda: [supervisor_homepage.destroy(),create_supervisor_send_message()])
    send_message.grid(row=1,column=1,padx=15,pady=15)
    view_product_popularity=tk.Button(supervisor_homepage,text='VIEW PRODUCT POPULARITY',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont,command=lambda: [supervisor_homepage.destroy(),create_supervisor_popular_product()])
    view_product_popularity.grid(row=2,column=1,padx=15,pady=15)
    view_cashier_performance=tk.Button(supervisor_homepage,text='VIEW CASHIER PERFORMANCE',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont,command=lambda: [supervisor_homepage.destroy(),create_supervisor_cashier_performance()])
    view_cashier_performance.grid(row=3,column=1,padx=15,pady=15)
    generate_salary_slip=tk.Button(supervisor_homepage,text='GENERATE SALARY SLIP',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont,command=lambda: [supervisor_homepage.destroy(),create_supervisor_salary_slip()])
    generate_salary_slip.grid(row=4,column=1,padx=15,pady=15)
    logout_button=tk.Button(supervisor_homepage,text='LOGOUT',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont,command=supervisor_homepage.destroy)
    logout_button.grid(row=5,column=1,padx=20,pady=15)
    supervisor_homepage.mainloop()

#this function creates the supervisor inventory page.
def create_supervisor_inventory():
    # this function gets the details of the user selected product.
    def get_selected_product(event):
        try:
            global selected_supervisor_product
            indexnumber=product_details_listbox.curselection()[0]
            selected_supervisor_product=product_details_listbox.get(indexnumber)
            selected_product_id_label.configure(text=selected_supervisor_product[0])
            product_name_entry.delete(0,tk.END)
            product_name_entry.insert(tk.END,selected_supervisor_product[1])
            product_category_entry.delete(0,tk.END)
            product_category_entry.insert(tk.END,selected_supervisor_product[2])
            selected_gst_rate_entry.delete(0,tk.END)
            selected_gst_rate_entry.insert(tk.END,selected_supervisor_product[3])
            product_cost_entry.delete(0,tk.END)
            product_cost_entry.insert(tk.END,selected_supervisor_product[4])
            product_unit_entry.delete(0,tk.END)
            product_unit_entry.insert(tk.END,selected_supervisor_product[5])
            product_available_entry.delete(0,tk.END)
            product_available_entry.insert(tk.END,selected_supervisor_product[6])
            product_purchased_entry.delete(0,tk.END)
            product_purchased_entry.insert(tk.END,selected_supervisor_product[7])
        except IndexError:
            pass
    
    #this function clears all the entry fields.
    def clear_command():
        selected_product_id_label.configure(text='')
        product_name_entry.delete(0,tk.END)
        product_category_entry.delete(0,tk.END)
        selected_gst_rate_entry.delete(0,tk.END)
        product_cost_entry.delete(0,tk.END)
        product_unit_entry.delete(0,tk.END)
        product_available_entry.delete(0,tk.END)  
        product_purchased_entry.delete(0,tk.END) 
     
    #this function gets the category selected by the user.
    def get_selected_category(event):
        try:
            global selected_supervisor_category
            indexnumber=category_listbox.curselection()[0]
            selected_supervisor_category=category_listbox.get(indexnumber)
            selected_category_label.configure(text='Selected Category:\n'+selected_supervisor_category)
        except IndexError:
            pass
    
    #this function displays details of all products in the listbox.
    def view_all_command():
        conn=sqlite3.connect(database_name)
        cur=conn.cursor()
        cur.execute('SELECT * FROM INVENTORY')
        product_details=cur.fetchall()
        conn.close()
        product_details_listbox.delete(0,tk.END)
        for record in product_details:
            product_details_listbox.insert(tk.END,record)
    
    #this function updates the product details in the inventory table.
    def update_command():
        conn=sqlite3.connect(database_name)
        cur=conn.cursor()
        cur.execute('UPDATE INVENTORY SET PROD_NAME=?,PROD_CATEGORY=?,GST_RATE=?,PROD_COST_PER_UNIT=?,UNIT_OF_MEASUREMENT=?,UNITS_AVAILABLE=?,UNITS_PURCHASED=? WHERE PROD_ID=?',(product_name_var.get().replace(' ','_'),product_category_var.get().replace(' ','_'),gst_rate_var.get(),float(product_cost_var.get()),product_unit_var.get().replace(' ','_'),int(product_available_var.get()),int(product_purchased_var.get()),selected_supervisor_product[0]))
        conn.commit()
        conn.close()
    
    #this function deletes the product record from the inventory table.
    def delete_command():
        global selected_supervisor_product
        conn=sqlite3.connect(database_name)
        cur=conn.cursor()
        cur.execute('DELETE FROM INVENTORY WHERE PROD_ID=?',(selected_supervisor_product[0],))
        conn.commit()
        conn.close()

    #this function adds the product record to the inventory table.
    def add_command():
        conn=sqlite3.connect(database_name)
        cur=conn.cursor()
        cur.execute('SELECT * FROM INVENTORY')
        rows=cur.fetchall()
        conn.close()
        last_id=rows[-1][0]
        generated_prod_id='PR'+str(int(last_id.replace('PR',''))+1)
        conn=sqlite3.connect(database_name)
        cur=conn.cursor()
        cur.execute('INSERT INTO INVENTORY VALUES (?,?,?,?,?,?,?,?)',(generated_prod_id,product_name_var.get().replace(' ','_'),product_category_var.get().replace(' ','_'),gst_rate_var.get(),float(product_cost_var.get()),product_unit_var.get().replace(' ','_'),int(product_available_var.get()),int(product_purchased_var.get())))
        conn.commit()
        conn.close()
        conn=sqlite3.connect(database_name)
        cur=conn.cursor()
        cur.execute('SELECT PROD_CATEGORY FROM INVENTORY')
        category_list=cur.fetchall()
        conn.close()
        final_categories=[]
        category_listbox.delete(0,tk.END)
        for i in category_list:
            if i[0] not in final_categories:
                final_categories.append(i[0])
        for category in final_categories:
            category_listbox.insert(tk.END,category)
   
    #this function displays details of products belonging to a particular category.
    def view_category_command():
        conn=sqlite3.connect(database_name)
        cur=conn.cursor()
        cur.execute('SELECT * FROM INVENTORY WHERE PROD_CATEGORY=?',(selected_supervisor_category,))
        product_details=cur.fetchall()
        conn.close()
        product_details_listbox.delete(0,tk.END)
        for record in product_details:
            product_details_listbox.insert(tk.END,record)
            
    supervisor_product_inventory=tk.Tk()
    supervisor_product_inventory.title('PRODUCT INVENTORY')
    supervisor_product_inventory.iconbitmap(icon_name)
    supervisor_product_inventory['background']=window_bg_color
    width=supervisor_product_inventory.winfo_screenwidth()-40
    height=supervisor_product_inventory.winfo_screenheight()-40
    supervisor_product_inventory.geometry('%dx%d'%(width,height))
    headerfont=font.Font(family='Bahnschrift',size=30,weight='bold',underline=1)
    buttonfont=font.Font(family='Bahnschrift',size=20,weight='bold')
    selectionfont=font.Font(family='Bahnschrift',size=12,weight='bold')
    header_label=tk.Label(supervisor_product_inventory,text='PRODUCT INVENTORY',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=headerfont)
    header_label.grid(row=0,column=0,padx=10,pady=8,columnspan=4)
    view_all_button=tk.Button(supervisor_product_inventory,text='View All Products',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont,command=view_all_command)
    view_all_button.grid(row=1,column=0,padx=10,pady=8)
    update_button=tk.Button(supervisor_product_inventory,text='Update',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont,command=update_command)
    update_button.grid(row=1,column=1,padx=10,pady=8)
    delete_button=tk.Button(supervisor_product_inventory,text='Delete',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont,command=delete_command)
    delete_button.grid(row=1,column=2,padx=10,pady=8)
    add_button=tk.Button(supervisor_product_inventory,text='Add',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont,command=add_command)
    add_button.grid(row=1,column=3,padx=10,pady=8)
    clear_button=tk.Button(supervisor_product_inventory,text='Clear Selection',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont,command=clear_command)
    clear_button.grid(row=1,column=4,padx=10,pady=8)
    view_category_button=tk.Button(supervisor_product_inventory,text='View Products in\nSelected Category',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=selectionfont,command=view_category_command)
    view_category_button.grid(row=2,column=4,padx=10,pady=8)
    select_category_label=tk.Label(supervisor_product_inventory,text='Select Category',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont)
    select_category_label.grid(row=2,column=0,padx=10,pady=8)
    product_id_label=tk.Label(supervisor_product_inventory,text='Product ID',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont)
    product_id_label.grid(row=3,column=0,padx=10,pady=8)
    product_name_label=tk.Label(supervisor_product_inventory,text='Product Name',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont)
    product_name_label.grid(row=4,column=0,padx=10,pady=8)
    product_category_label=tk.Label(supervisor_product_inventory,text='Product Category',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont)
    product_category_label.grid(row=5,column=0,padx=10,pady=8)
    gst_rate_label=tk.Label(supervisor_product_inventory,text='GST Rate',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont)
    gst_rate_label.grid(row=6,column=0,padx=10,pady=8)
    cost_label=tk.Label(supervisor_product_inventory,text='Cost Per Unit',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont)
    cost_label.grid(row=7,column=0,padx=10,pady=8)
    unit_label=tk.Label(supervisor_product_inventory,text='Unit of Measurement',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont)
    unit_label.grid(row=8,column=0,padx=10,pady=8)
    unit_available_label=tk.Label(supervisor_product_inventory,text='Units Available',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont)
    unit_available_label.grid(row=9,column=0,padx=10,pady=8)
    unit_purchased_label=tk.Label(supervisor_product_inventory,text='Total Units Purchased\nTill Date',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont)
    unit_purchased_label.grid(row=10,column=0,padx=10,pady=8)
    selected_product_id_label=tk.Label(supervisor_product_inventory,text='',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont)
    selected_product_id_label.grid(row=3,column=1,padx=10,pady=8)
    product_name_var=tk.StringVar()
    product_name_entry=tk.Entry(supervisor_product_inventory,textvariable=product_name_var,font=buttonfont)
    product_name_entry.grid(row=4,column=1,padx=10,pady=8)
    product_category_var=tk.StringVar()
    product_category_entry=tk.Entry(supervisor_product_inventory,textvariable=product_category_var,font=buttonfont)
    product_category_entry.grid(row=5,column=1,padx=10,pady=8)
    gst_rate_var=tk.StringVar()
    selected_gst_rate_entry=tk.Entry(supervisor_product_inventory,textvariable=gst_rate_var,font=buttonfont)
    selected_gst_rate_entry.grid(row=6,column=1,padx=10,pady=8)
    product_cost_var=tk.StringVar()
    product_cost_entry=tk.Entry(supervisor_product_inventory,textvariable=product_cost_var,font=buttonfont)
    product_cost_entry.grid(row=7,column=1,padx=10,pady=8)
    product_unit_var=tk.StringVar()
    product_unit_entry=tk.Entry(supervisor_product_inventory,textvariable=product_unit_var,font=buttonfont)
    product_unit_entry.grid(row=8,column=1,padx=10,pady=8)
    product_available_var=tk.StringVar()
    product_available_entry=tk.Entry(supervisor_product_inventory,textvariable=product_available_var,font=buttonfont)
    product_available_entry.grid(row=9,column=1,padx=10,pady=8)
    product_purchased_var=tk.StringVar()
    product_purchased_entry=tk.Entry(supervisor_product_inventory,textvariable=product_purchased_var,font=buttonfont)
    product_purchased_entry.grid(row=10,column=1,padx=10,pady=8)
    selected_category_label=tk.Label(supervisor_product_inventory,text='',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=selectionfont)
    selected_category_label.grid(row=2,column=3,padx=10,pady=8)
    category_listbox=tk.Listbox(supervisor_product_inventory,fg=button_fg_color,borderwidth=0,font=selectionfont,height=3,width=20)
    category_listbox.grid(row=2,column=1,pady=8)
    scrollbar1=tk.Scrollbar(supervisor_product_inventory)
    scrollbar1.grid(row=2,column=2,pady=8)
    category_listbox.configure(yscrollcommand=scrollbar1.set)
    scrollbar1.configure(command=category_listbox.yview)
    category_listbox.bind('<<ListboxSelect>>',get_selected_category)
    conn=sqlite3.connect(database_name)
    cur=conn.cursor()
    cur.execute('SELECT PROD_CATEGORY FROM INVENTORY')
    category_list=cur.fetchall()
    conn.close()
    final_categories=[]
    category_listbox.delete(0,tk.END)
    for i in category_list:
        if i[0] not in final_categories:
            final_categories.append(i[0])
    for category in final_categories:
        category_listbox.insert(tk.END,category)
    product_details_listbox=tk.Listbox(supervisor_product_inventory,fg=button_fg_color,borderwidth=0,font=selectionfont,height=15,width=55)
    product_details_listbox.grid(row=3,column=2,pady=8,rowspan=8,columnspan=3)
    scrollbar2=tk.Scrollbar(supervisor_product_inventory)
    scrollbar2.grid(row=3,column=5,rowspan=8,pady=8)
    product_details_listbox.configure(yscrollcommand=scrollbar2.set)
    scrollbar2.configure(command=product_details_listbox.yview)
    product_details_listbox.bind('<<ListboxSelect>>',get_selected_product)
    back_button=tk.Button(supervisor_product_inventory,text='Back',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont,command=lambda: [supervisor_product_inventory.destroy(),create_supervisor_homepage()])
    back_button.grid(row=11,column=3,pady=8)
    supervisor_product_inventory.mainloop()

#this function creates the supervisor's customer data page.    
def create_supervisor_customer_data():
    #this function gets details of customer selected by the user.
    def get_selected_customer(event):
        try:
            global selected_customer_by_supervisor
            indexnumber=cust_details_listbox.curselection()[0]
            selected_customer_by_supervisor=cust_details_listbox.get(indexnumber)
            selected_id_label.configure(text=selected_customer_by_supervisor[0])
            name_entry.delete(0,tk.END)
            name_entry.insert(tk.END,selected_customer_by_supervisor[1])
            number_entry.delete(0,tk.END)
            number_entry.insert(tk.END,selected_customer_by_supervisor[2])
            email_entry.delete(0,tk.END)
            email_entry.insert(tk.END,selected_customer_by_supervisor[3])
            
        except IndexError:
            pass
     
    #this function displays details of all customers in a listbox.
    def view_command():
        conn=sqlite3.connect(database_name)
        cur=conn.cursor()
        cur.execute('SELECT * FROM CUSTOMER')
        customer_details=cur.fetchall()
        conn.close()
        cust_details_listbox.delete(0,tk.END)
        for record in customer_details:
            cust_details_listbox.insert(tk.END,record)
    
    #this function adds the customer record to customer table.
    def add_command():
        conn=sqlite3.connect(database_name)
        cur=conn.cursor()
        cur.execute('SELECT * FROM CUSTOMER')
        rows=cur.fetchall()
        conn.close()
        last_id=rows[-1][0]
        generated_cust_id='CT'+str(int(last_id.replace('CT',''))+1)
        conn=sqlite3.connect(database_name)
        cur=conn.cursor()
        cur.execute('INSERT INTO CUSTOMER VALUES (?,?,?,?)',(generated_cust_id,name_var.get(),int(number_var.get()),email_var.get()))
        conn.commit()
        conn.close()
        
    #this function deletes customer record from the customer table.  
    def delete_command():
        global selected_customer_by_supervisor
        conn=sqlite3.connect(database_name)
        cur=conn.cursor()
        cur.execute('DELETE FROM CUSTOMER WHERE CUST_ID=?',(selected_customer_by_supervisor[0],))
        conn.commit()
        conn.close()

    #this function updates the customer details in the customer table.
    def update_command():
        global selected_customer_by_supervisor
        conn=sqlite3.connect(database_name)
        cur=conn.cursor()
        cur.execute('UPDATE CUSTOMER SET NAME=?,PH_NO=?,EMAIL_ID=? WHERE CUST_ID=?',(name_var.get(),int(number_var.get()),email_var.get(),selected_customer_by_supervisor[0]))
        conn.commit()
        conn.close()
        
    #this function clears all the entry fields.
    def clear_command():
        selected_id_label.configure(text='')
        name_entry.delete(0,tk.END)
        number_entry.delete(0,tk.END)
        email_entry.delete(0,tk.END)
        
    supervisor_customer_data=tk.Tk()
    supervisor_customer_data.title('CUSTOMER DATA')
    supervisor_customer_data.iconbitmap(icon_name)
    supervisor_customer_data['background']=window_bg_color
    width=supervisor_customer_data.winfo_screenwidth()-40
    height=supervisor_customer_data.winfo_screenheight()-40
    supervisor_customer_data.geometry('%dx%d'%(width,height))
    headerfont=font.Font(family='Bahnschrift',size=30,weight='bold',underline=1)
    buttonfont=font.Font(family='Bahnschrift',size=20,weight='bold')
    selectionfont=font.Font(family='Bahnschrift',size=12,weight='bold')
    header_label=tk.Label(supervisor_customer_data,text='CUSTOMER DATA',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=headerfont)
    header_label.grid(row=0,column=0,columnspan=3,padx=8,pady=5)
    id_label=tk.Label(supervisor_customer_data,text='Customer ID: ',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont)
    id_label.grid(row=1,column=0,padx=8,pady=5)
    name_label=tk.Label(supervisor_customer_data,text='Name: ',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont)
    name_label.grid(row=2,column=0,padx=8,pady=5)
    number_label=tk.Label(supervisor_customer_data,text='Phone Number: ',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont)
    number_label.grid(row=3,column=0,padx=8,pady=5)
    email_label=tk.Label(supervisor_customer_data,text='Email ID: ',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont)
    email_label.grid(row=4,column=0,padx=8,pady=5)
    selected_id_label=tk.Label(supervisor_customer_data,text='',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont)
    selected_id_label.grid(row=1,column=1,padx=8,pady=5)
    name_var=tk.StringVar()
    name_entry=tk.Entry(supervisor_customer_data,textvariable=name_var,font=buttonfont)
    name_entry.grid(row=2,column=1,padx=8,pady=5)
    number_var=tk.StringVar()
    number_entry=tk.Entry(supervisor_customer_data,textvariable=number_var,font=buttonfont)
    number_entry.grid(row=3,column=1,padx=8,pady=5)
    email_var=tk.StringVar()
    email_entry=tk.Entry(supervisor_customer_data,textvariable=email_var,font=buttonfont)
    email_entry.grid(row=4,column=1,padx=8,pady=5)
    view_button=tk.Button(supervisor_customer_data,text='View',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont,command=view_command)
    view_button.grid(row=5,column=0,padx=8,pady=5)
    add_button=tk.Button(supervisor_customer_data,text='Add',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont,command=add_command)
    add_button.grid(row=5,column=1,padx=8,pady=5)
    delete_button=tk.Button(supervisor_customer_data,text='Delete',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont,command=delete_command)
    delete_button.grid(row=6,column=1,padx=8,pady=5)
    update_button=tk.Button(supervisor_customer_data,text='Update',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont,command=update_command)
    update_button.grid(row=6,column=0,padx=8,pady=5)
    clear_button=tk.Button(supervisor_customer_data,text='Clear Selection',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont,command=clear_command)
    clear_button.grid(row=7,column=0,padx=8,pady=5)
    cust_details_listbox=tk.Listbox(supervisor_customer_data,fg=button_fg_color,borderwidth=0,font=selectionfont,height=12,width=60)
    cust_details_listbox.grid(row=1,column=2,padx=8,pady=5,rowspan=4)
    scrollbar1=tk.Scrollbar(supervisor_customer_data)
    scrollbar1.grid(row=1,column=3,pady=5,rowspan=4)
    cust_details_listbox.configure(yscrollcommand=scrollbar1.set)
    scrollbar1.configure(command=cust_details_listbox.yview)
    scrollbar2=tk.Scrollbar(supervisor_customer_data,orient=tk.HORIZONTAL)
    scrollbar2.grid(row=5,column=2,pady=5)
    cust_details_listbox.configure(xscrollcommand=scrollbar2.set)
    scrollbar2.configure(command=cust_details_listbox.xview)
    cust_details_listbox.bind('<<ListboxSelect>>',get_selected_customer)
    back_button=tk.Button(supervisor_customer_data,text='Back',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont,command=lambda: [supervisor_customer_data.destroy(),create_supervisor_homepage()])
    back_button.grid(row=7,column=1,padx=8,pady=5)
    supervisor_customer_data.mainloop()

#this function creates the supervisor's view profile page.    
def create_supervisor_view_profile():
    #this function updates the supervisor details in the supervisor table.
    def update_command():
        global current_supervisor_user
        conn=sqlite3.connect(database_name)
        cur=conn.cursor()
        cur.execute('UPDATE SUPERVISOR SET NAME=?,DOB=?,AGE=?,GENDER=?,ADDRESS=?,PH_NO=?,EMAIL_ID=?,USERNAME=?,PASSWORD=? WHERE SUP_ID=?',(name_var.get(),DOB_var.get(),int(age_var.get()),gender_var.get(),address_var.get(),int(number_var.get()),email_var.get(),username_var.get(),password_var.get(),current_supervisor_user))
        conn.commit()
        conn.close()
        
    global current_supervisor_user
    supervisor_view_profile=tk.Tk()
    supervisor_view_profile.title('PROFILE')
    supervisor_view_profile.iconbitmap(icon_name)
    supervisor_view_profile['background']=window_bg_color
    width=supervisor_view_profile.winfo_screenwidth()-40
    height=supervisor_view_profile.winfo_screenheight()-40
    supervisor_view_profile.geometry('%dx%d'%(width,height))
    headerfont=font.Font(family='Bahnschrift',size=30,weight='bold',underline=1)
    buttonfont=font.Font(family='Bahnschrift',size=20,weight='bold')
    header_label=tk.Label(supervisor_view_profile,text='PROFILE',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=headerfont)
    header_label.grid(row=0,column=0,padx=15,pady=8,columnspan=2)
    supervisor_id_label=tk.Label(supervisor_view_profile,text='Supervisor ID: ',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont)
    supervisor_id_label.grid(row=1,column=0,padx=15,pady=8)
    supervisor_name_label=tk.Label(supervisor_view_profile,text='Name: ',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont)
    supervisor_name_label.grid(row=2,column=0,padx=15,pady=8)
    supervisor_DOB_label=tk.Label(supervisor_view_profile,text='Date of Birth: ',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont)
    supervisor_DOB_label.grid(row=3,column=0,padx=15,pady=8)
    supervisor_age_label=tk.Label(supervisor_view_profile,text='Age: ',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont)
    supervisor_age_label.grid(row=4,column=0,padx=15,pady=8)
    supervisor_gender_label=tk.Label(supervisor_view_profile,text='Gender: ',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont)
    supervisor_gender_label.grid(row=5,column=0,padx=15,pady=8)
    supervisor_address_label=tk.Label(supervisor_view_profile,text='Address: ',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont)
    supervisor_address_label.grid(row=6,column=0,padx=15,pady=8)
    supervisor_number_label=tk.Label(supervisor_view_profile,text='Phone Number: ',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont)
    supervisor_number_label.grid(row=7,column=0,padx=15,pady=8)
    supervisor_email_label=tk.Label(supervisor_view_profile,text='Email ID: ',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont)
    supervisor_email_label.grid(row=8,column=0,padx=15,pady=8)
    supervisor_username_label=tk.Label(supervisor_view_profile,text='Username: ',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont)
    supervisor_username_label.grid(row=9,column=0,padx=15,pady=8)
    supervisor_password_label=tk.Label(supervisor_view_profile,text='Password: ',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont)
    supervisor_password_label.grid(row=10,column=0,padx=15,pady=8)
    conn=sqlite3.connect(database_name)
    cur=conn.cursor()
    cur.execute('SELECT * FROM SUPERVISOR WHERE SUP_ID=?',(current_supervisor_user,))
    supervisor_record=cur.fetchall()[0]
    conn.close()
    selected_supervisor_id_label=tk.Label(supervisor_view_profile,text=supervisor_record[0],bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont)
    selected_supervisor_id_label.grid(row=1,column=1,padx=15,pady=8)
    name_var=tk.StringVar()
    name_entry=tk.Entry(supervisor_view_profile,textvariable=name_var,font=buttonfont)
    name_entry.grid(row=2,column=1,padx=15,pady=8)
    DOB_var=tk.StringVar()
    DOB_entry=tk.Entry(supervisor_view_profile,textvariable=DOB_var,font=buttonfont)
    DOB_entry.grid(row=3,column=1,padx=15,pady=8)
    age_var=tk.StringVar()
    age_entry=tk.Entry(supervisor_view_profile,textvariable=age_var,font=buttonfont)
    age_entry.grid(row=4,column=1,padx=15,pady=8)
    gender_var=tk.StringVar()
    gender_entry=tk.Entry(supervisor_view_profile,textvariable=gender_var,font=buttonfont)
    gender_entry.grid(row=5,column=1,padx=15,pady=8)
    address_var=tk.StringVar()
    address_entry=tk.Entry(supervisor_view_profile,textvariable=address_var,font=buttonfont)
    address_entry.grid(row=6,column=1,padx=15,pady=8)
    number_var=tk.StringVar()
    number_entry=tk.Entry(supervisor_view_profile,textvariable=number_var,font=buttonfont)
    number_entry.grid(row=7,column=1,padx=15,pady=8)
    email_var=tk.StringVar()
    email_entry=tk.Entry(supervisor_view_profile,textvariable=email_var,font=buttonfont)
    email_entry.grid(row=8,column=1,padx=15,pady=8)
    username_var=tk.StringVar()
    username_entry=tk.Entry(supervisor_view_profile,textvariable=username_var,font=buttonfont)
    username_entry.grid(row=9,column=1,padx=15,pady=8)
    password_var=tk.StringVar()
    password_entry=tk.Entry(supervisor_view_profile,textvariable=password_var,font=buttonfont)
    password_entry.grid(row=10,column=1,padx=15,pady=8)
    name_entry.delete(0,tk.END)
    DOB_entry.delete(0,tk.END)
    age_entry.delete(0,tk.END)
    gender_entry.delete(0,tk.END)
    address_entry.delete(0,tk.END)
    number_entry.delete(0,tk.END)
    email_entry.delete(0,tk.END)
    username_entry.delete(0,tk.END)
    password_entry.delete(0,tk.END)
    name_entry.insert(tk.END,supervisor_record[1])
    DOB_entry.insert(tk.END,supervisor_record[2])
    age_entry.insert(tk.END,supervisor_record[3])
    gender_entry.insert(tk.END,supervisor_record[4])
    address_entry.insert(tk.END,supervisor_record[5])
    number_entry.insert(tk.END,supervisor_record[6])
    email_entry.insert(tk.END,supervisor_record[7])
    username_entry.insert(tk.END,supervisor_record[8])
    password_entry.insert(tk.END,supervisor_record[9])
    update_button=tk.Button(supervisor_view_profile,text='Update',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont,command=lambda: [messagebox.showinfo('Success','Details successfully updated.'),update_command()])
    update_button.grid(row=11,column=0,padx=15,pady=8)
    back_button=tk.Button(supervisor_view_profile,text='Back',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont,command=lambda: [supervisor_view_profile.destroy(),create_supervisor_homepage()])
    back_button.grid(row=11,column=1,padx=15,pady=8)
    supervisor_view_profile.mainloop()  

#this function creates the supervisor's view cashiers page.
def create_supervisor_view_cashiers():
    #this function gets details of cashier selected by user.
    def get_selected_employee(event):
        try:
            global selected_cashier_by_supervisor
            indexnumber=emp_details_listbox.curselection()[0]
            selected_cashier_by_supervisor=emp_details_listbox.get(indexnumber)
            selected_id_label.configure(text=selected_cashier_by_supervisor[0])
            name_entry.delete(0,tk.END)
            name_entry.insert(tk.END,selected_cashier_by_supervisor[1])
            DOB_entry.delete(0,tk.END)
            DOB_entry.insert(tk.END,selected_cashier_by_supervisor[2])
            age_entry.delete(0,tk.END)
            age_entry.insert(tk.END,selected_cashier_by_supervisor[3])
            gender_entry.delete(0,tk.END)
            gender_entry.insert(tk.END,selected_cashier_by_supervisor[4])
            address_entry.delete('1.0','end-1c')
            address_entry.insert('end-1c',selected_cashier_by_supervisor[5])
            number_entry.delete(0,tk.END)
            number_entry.insert(tk.END,selected_cashier_by_supervisor[6])
            email_entry.delete(0,tk.END)
            email_entry.insert(tk.END,selected_cashier_by_supervisor[7])
            username_entry.delete(0,tk.END)
            username_entry.insert(tk.END,selected_cashier_by_supervisor[8])
            password_entry.delete(0,tk.END)
            password_entry.insert(tk.END,selected_cashier_by_supervisor[9])
        except IndexError:
            pass
    
    #this function displays details of all cashiers.
    def view_command():
        conn=sqlite3.connect(database_name)
        cur=conn.cursor()
        cur.execute('SELECT EMP_ID , NAME , DOB , AGE , GENDER , ADDRESS , PH_NO , EMAIL_ID,  USERNAME , PASSWORD FROM EMPLOYEE')
        employee_details=cur.fetchall()
        conn.close()
        emp_details_listbox.delete(0,tk.END)
        for record in employee_details:
            emp_details_listbox.insert(tk.END,record)
    
    #this function adds cashier record to employee table.
    def add_command():
        conn=sqlite3.connect(database_name)
        cur=conn.cursor()
        cur.execute('SELECT * FROM EMPLOYEE')
        rows=cur.fetchall()
        conn.close()
        last_id=rows[-1][0]
        generated_emp_id='EP'+str(int(last_id.replace('EP',''))+1)
        conn=sqlite3.connect(database_name)
        cur=conn.cursor()
        cur.execute('SELECT USERNAME FROM EMPLOYEE')
        employee_data=cur.fetchall()
        conn.close()
        employee_list=[]
        for i in employee_data:
            employee_list.append(i[0])
        if username_var.get() not in employee_list:
            conn=sqlite3.connect(database_name)
            cur=conn.cursor()
            cur.execute('INSERT INTO EMPLOYEE VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',(generated_emp_id,name_var.get(),DOB_var.get(),int(age_var.get()),gender_var.get(),address_entry.get('1.0','end-1c'),int(number_var.get()),email_var.get(),username_var.get(),password_var.get(),None,None,None,None,None,None,None,None,None,None))
            conn.commit()
            conn.close()
            conn=sqlite3.connect(database_name)
            cur=conn.cursor()
            cur.execute('INSERT INTO SALES2022 VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)',(generated_emp_id,name_var.get(),0,0,0,0,0,0,0,0,0,0,0,0))
            conn.commit()
            conn.close()
        else:
            messagebox.showinfo('Adding record failed','Failed to add record of employee.\nUsername is already in use.\nPlease try again.')
    
    #this function deletes cashier record from the employee table.
    def delete_command():
        conn=sqlite3.connect(database_name)
        cur=conn.cursor()
        cur.execute('DELETE FROM EMPLOYEE WHERE EMP_ID=?',(selected_cashier_by_supervisor[0],))
        conn.commit()
        conn.close()
        conn=sqlite3.connect(database_name)
        cur=conn.cursor()
        cur.execute('DELETE FROM SALES2022 WHERE EMP_ID=?',(selected_cashier_by_supervisor[0],))
        conn.commit()
        conn.close()
    
    #this function updates the cashier details in the cashier table.
    def update_command():
        conn=sqlite3.connect(database_name)
        cur=conn.cursor()
        cur.execute('UPDATE EMPLOYEE SET NAME=?,DOB=?,AGE=?,GENDER=?,ADDRESS=?,PH_NO=?,EMAIL_ID=?,USERNAME=?,PASSWORD=? WHERE EMP_ID=?',(name_var.get(),DOB_var.get(),int(age_var.get()),gender_var.get(),address_entry.get('1.0','end-1c'),int(number_var.get()),email_var.get(),username_var.get(),password_var.get(),selected_cashier_by_supervisor[0]))
        conn.commit()
        conn.close()
    
    #this function clears all the entry fields.
    def clear_command():
        selected_id_label.configure(text='')
        name_entry.delete(0,tk.END)
        DOB_entry.delete(0,tk.END)
        age_entry.delete(0,tk.END)
        gender_entry.delete(0,tk.END)
        address_entry.delete('1.0','end-1c')
        number_entry.delete(0,tk.END)
        email_entry.delete(0,tk.END)
        username_entry.delete(0,tk.END)
        password_entry.delete(0,tk.END)
        
    supervisor_view_cashiers=tk.Tk()
    supervisor_view_cashiers.title('CASHIER DATA')
    supervisor_view_cashiers.iconbitmap(icon_name)
    supervisor_view_cashiers['background']=window_bg_color
    width=supervisor_view_cashiers.winfo_screenwidth()-40
    height=supervisor_view_cashiers.winfo_screenheight()-40
    supervisor_view_cashiers.geometry('%dx%d'%(width,height))
    headerfont=font.Font(family='Bahnschrift',size=30,weight='bold',underline=1)
    buttonfont=font.Font(family='Bahnschrift',size=20,weight='bold')
    selectionfont=font.Font(family='Bahnschrift',size=12,weight='bold')
    header_label=tk.Label(supervisor_view_cashiers,text='Employee Data',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=headerfont)
    header_label.grid(row=0,column=0,columnspan=3,padx=8,pady=5)
    id_label=tk.Label(supervisor_view_cashiers,text='Employee ID: ',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont)
    id_label.grid(row=1,column=0,padx=8,pady=5)
    name_label=tk.Label(supervisor_view_cashiers,text='Name: ',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont)
    name_label.grid(row=2,column=0,padx=8,pady=5)
    DOB_label=tk.Label(supervisor_view_cashiers,text='Date of Birth: ',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont)
    DOB_label.grid(row=3,column=0,padx=8,pady=5)
    age_label=tk.Label(supervisor_view_cashiers,text='Age: ',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont)
    age_label.grid(row=4,column=0,padx=8,pady=5)
    gender_label=tk.Label(supervisor_view_cashiers,text='Gender: ',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont)
    gender_label.grid(row=5,column=0,padx=8,pady=5)
    address_label=tk.Label(supervisor_view_cashiers,text='Address: ',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont)
    address_label.grid(row=6,column=0,padx=8,pady=5)
    number_label=tk.Label(supervisor_view_cashiers,text='Phone Number: ',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont)
    number_label.grid(row=7,column=0,padx=8,pady=5)
    email_label=tk.Label(supervisor_view_cashiers,text='Email ID: ',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont)
    email_label.grid(row=8,column=0,padx=8,pady=5)
    username_label=tk.Label(supervisor_view_cashiers,text='Username: ',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont)
    username_label.grid(row=9,column=0,padx=8,pady=5)
    password_label=tk.Label(supervisor_view_cashiers,text='Password: ',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont)
    password_label.grid(row=10,column=0,padx=8,pady=5)
    view_button=tk.Button(supervisor_view_cashiers,text='View',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont,command=view_command)
    view_button.grid(row=11,column=0,padx=8,pady=5)
    add_button=tk.Button(supervisor_view_cashiers,text='Add',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont,command=add_command)
    add_button.grid(row=11,column=1,padx=8,pady=5)
    delete_button=tk.Button(supervisor_view_cashiers,text='Delete',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont,command=delete_command)
    delete_button.grid(row=12,column=1,padx=8,pady=5)
    update_button=tk.Button(supervisor_view_cashiers,text='Update',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont,command=update_command)
    update_button.grid(row=12,column=0,padx=8,pady=5)
    clear_button=tk.Button(supervisor_view_cashiers,text='Clear Selection',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont,command=clear_command)
    clear_button.grid(row=13,column=0,padx=8,pady=5)
    back_button=tk.Button(supervisor_view_cashiers,text='Back',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont,command=lambda: [supervisor_view_cashiers.destroy(),create_supervisor_homepage()])
    back_button.grid(row=13,column=1,padx=8,pady=5)
    selected_id_label=tk.Label(supervisor_view_cashiers,text='',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont)
    selected_id_label.grid(row=1,column=1,padx=8,pady=5)
    name_var=tk.StringVar()
    name_entry=tk.Entry(supervisor_view_cashiers,textvariable=name_var,font=buttonfont)
    name_entry.grid(row=2,column=1,padx=8,pady=5)
    DOB_var=tk.StringVar()
    DOB_entry=tk.Entry(supervisor_view_cashiers,textvariable=DOB_var,font=buttonfont)
    DOB_entry.grid(row=3,column=1,padx=8,pady=5)
    age_var=tk.StringVar()
    age_entry=tk.Entry(supervisor_view_cashiers,textvariable=age_var,font=buttonfont)
    age_entry.grid(row=4,column=1,padx=8,pady=5)
    gender_var=tk.StringVar()
    gender_entry=tk.Entry(supervisor_view_cashiers,textvariable=gender_var,font=buttonfont)
    gender_entry.grid(row=5,column=1,padx=8,pady=5)
    address_entry=scrolledtext.ScrolledText(supervisor_view_cashiers,font=selectionfont,height=2,width=25)
    address_entry.grid(row=6,column=1,padx=8,pady=5)
    number_var=tk.StringVar()
    number_entry=tk.Entry(supervisor_view_cashiers,textvariable=number_var,font=buttonfont)
    number_entry.grid(row=7,column=1,padx=8,pady=5)
    email_var=tk.StringVar()
    email_entry=tk.Entry(supervisor_view_cashiers,textvariable=email_var,font=buttonfont)
    email_entry.grid(row=8,column=1,padx=8,pady=5)
    username_var=tk.StringVar()
    username_entry=tk.Entry(supervisor_view_cashiers,textvariable=username_var,font=buttonfont)
    username_entry.grid(row=9,column=1,padx=8,pady=5)
    password_var=tk.StringVar()
    password_entry=tk.Entry(supervisor_view_cashiers,textvariable=password_var,font=buttonfont)
    password_entry.grid(row=10,column=1,padx=8,pady=5)
    emp_details_listbox=tk.Listbox(supervisor_view_cashiers,fg=button_fg_color,borderwidth=0,font=selectionfont,height=12,width=60)
    emp_details_listbox.grid(row=1,column=2,padx=15,pady=5,rowspan=12)
    scrollbar1=tk.Scrollbar(supervisor_view_cashiers)
    scrollbar1.grid(row=2,column=3,pady=5,rowspan=12)
    emp_details_listbox.configure(yscrollcommand=scrollbar1.set)
    scrollbar1.configure(command=emp_details_listbox.yview)
    scrollbar2=tk.Scrollbar(supervisor_view_cashiers,orient=tk.HORIZONTAL)
    scrollbar2.grid(row=11,column=2,pady=5)
    emp_details_listbox.configure(xscrollcommand=scrollbar2.set)
    scrollbar2.configure(command=emp_details_listbox.xview)
    emp_details_listbox.bind('<<ListboxSelect>>',get_selected_employee)
    supervisor_view_cashiers.mainloop()

#this function creates the supervisor's view cashier performance page.
def create_supervisor_cashier_performance():
    #this function gets details of cashier selected by user.
    def get_selected_employee(event):
        try:
            global selected_cashier_by_supervisor
            indexnumber=emp_details_listbox.curselection()[0]
            selected_cashier_by_supervisor=emp_details_listbox.get(indexnumber)
            required_text1='Selected Employee\n'+selected_cashier_by_supervisor[0]+' - '+selected_cashier_by_supervisor[1]
            selected_employee_label.configure(text=required_text1)
        except IndexError:
            pass
    
    #this function gets details of the month selected by user.
    def get_selected_month(event):
        try:
            global selected_month_by_supervisor
            indexnumber=month_listbox.curselection()[0]
            selected_month_by_supervisor=month_listbox.get(indexnumber)
            required_text2='Selected Month\n'+selected_month_by_supervisor
            selected_month_label.configure(text=required_text2)
        except IndexError:
            pass
    
    #this function displays sales of cashier for selected month.
    def view_command():
        global selected_cashier_by_supervisor , selected_month_by_supervisor
        month_selection_sql='SELECT %s FROM SALES2022 WHERE EMP_ID="%s"'%(selected_month_by_supervisor,selected_cashier_by_supervisor[0])
        conn=sqlite3.connect(database_name)
        cur=conn.cursor()
        cur.execute(month_selection_sql)
        month_sales=cur.fetchall()[0][0]
        conn.close()
        sales_label.configure(text=str(month_sales))
     
    #this function gets details of month selected by user.
    def get_selected_month2(event):
        try:
            global selected_month2_by_supervisor
            indexnumber=month_listbox2.curselection()[0]
            selected_month2_by_supervisor=month_listbox2.get(indexnumber)
            required_text2='Selected Month\n'+selected_month2_by_supervisor
            selected_month2_label.configure(text=required_text2)
        except IndexError:
            pass
        
    #this function displays employee of the month.
    def view_command2():
        global database_name , selected_cashier_by_supervisor , selected_month_by_supervisor 
        month_selection_sql='SELECT EMP_ID , EMP_NAME , MAX(%s) FROM SALES2022'%(selected_month_by_supervisor)
        conn=sqlite3.connect(database_name)
        cur=conn.cursor()
        cur.execute(month_selection_sql)
        max_sales_record=cur.fetchall()[0]
        conn.close()
        emp_of_month_text='Employee ID: ' + max_sales_record[0] + '\n' + 'Employee Name: ' + max_sales_record[1] + '\n' + 'Sales: ' + str(max_sales_record[2])
        emp_label.configure(text=emp_of_month_text)
    
    supervisor_cashier_performance=tk.Tk()
    supervisor_cashier_performance.title('CASHIER PERFORMANCE')
    supervisor_cashier_performance.iconbitmap(icon_name)
    supervisor_cashier_performance['background']=window_bg_color
    width=supervisor_cashier_performance.winfo_screenwidth()-40
    height=supervisor_cashier_performance.winfo_screenheight()-40
    supervisor_cashier_performance.geometry('%dx%d'%(width,height))
    headerfont=font.Font(family='Bahnschrift',size=30,weight='bold',underline=1)
    buttonfont=font.Font(family='Bahnschrift',size=20,weight='bold')
    selectionfont=font.Font(family='Bahnschrift',size=12,weight='bold')
    header_label=tk.Label(supervisor_cashier_performance,text='Cashier Performance',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=headerfont)
    header_label.grid(row=0,column=0,columnspan=4,padx=8,pady=5)
    employee_label=tk.Label(supervisor_cashier_performance,text='Select Employee',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont)
    employee_label.grid(row=1,column=0,padx=8,pady=5)
    month_label=tk.Label(supervisor_cashier_performance,text='Select Month',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont)
    month_label.grid(row=2,column=0,padx=8,pady=5)
    selected_employee_label=tk.Label(supervisor_cashier_performance,text='',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont)
    selected_employee_label.grid(row=1,column=3,padx=8,pady=5)
    selected_month_label=tk.Label(supervisor_cashier_performance,text='',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont)
    selected_month_label.grid(row=2,column=3,padx=8,pady=5)
    emp_details_listbox=tk.Listbox(supervisor_cashier_performance,fg=button_fg_color,borderwidth=0,font=selectionfont,height=5,width=30)
    emp_details_listbox.grid(row=1,column=1,padx=8,pady=5)
    scrollbar1=tk.Scrollbar(supervisor_cashier_performance)
    scrollbar1.grid(row=1,column=2,pady=5)
    emp_details_listbox.configure(yscrollcommand=scrollbar1.set)
    scrollbar1.configure(command=emp_details_listbox.yview)
    emp_details_listbox.bind('<<ListboxSelect>>',get_selected_employee)
    conn=sqlite3.connect(database_name)
    cur=conn.cursor()
    cur.execute('SELECT EMP_ID , NAME FROM EMPLOYEE')
    employee_details=cur.fetchall()
    conn.close()
    emp_details_listbox.delete(0,tk.END)
    for record in employee_details:
        emp_details_listbox.insert(tk.END,record)
    month_listbox=tk.Listbox(supervisor_cashier_performance,fg=button_fg_color,borderwidth=0,font=selectionfont,height=5,width=30)
    month_listbox.grid(row=2,column=1,padx=8,pady=5)
    scrollbar2=tk.Scrollbar(supervisor_cashier_performance)
    scrollbar2.grid(row=2,column=2,pady=5)
    month_listbox.configure(yscrollcommand=scrollbar2.set)
    scrollbar2.configure(command=month_listbox.yview)
    month_listbox.bind('<<ListboxSelect>>',get_selected_month)
    month_list=['JAN','FEB','MAR','APR','MAY','JUN','JUL','AUG','SEP','OCT','NOV','DEC']
    for month in month_list:
        month_listbox.insert(tk.END,month+'_22')
    view_button=tk.Button(supervisor_cashier_performance,text='View Sales',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont,command=view_command)
    view_button.grid(row=3,column=0,padx=8,pady=5)
    sales_label=tk.Label(supervisor_cashier_performance,text='',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont)
    sales_label.grid(row=3,column=1,padx=8,pady=5)
    header_label2=tk.Label(supervisor_cashier_performance,text='Cashier of the Month',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=headerfont)
    header_label2.grid(row=4,column=0,columnspan=4,padx=8,pady=5)
    month_label2=tk.Label(supervisor_cashier_performance,text='Select Month',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont)
    month_label2.grid(row=5,column=0,padx=8,pady=5)
    selected_month2_label=tk.Label(supervisor_cashier_performance,text='',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont)
    selected_month2_label.grid(row=5,column=3,padx=8,pady=5)
    month_listbox2=tk.Listbox(supervisor_cashier_performance,fg=button_fg_color,borderwidth=0,font=selectionfont,height=5,width=30)
    month_listbox2.grid(row=5,column=1,padx=8,pady=5)
    scrollbar3=tk.Scrollbar(supervisor_cashier_performance)
    scrollbar3.grid(row=5,column=2,pady=5)
    month_listbox2.configure(yscrollcommand=scrollbar3.set)
    scrollbar3.configure(command=month_listbox2.yview)
    month_listbox2.bind('<<ListboxSelect>>',get_selected_month2)
    month_list=['JAN','FEB','MAR','APR','MAY','JUN','JUL','AUG','SEP','OCT','NOV','DEC']
    for month in month_list:
        month_listbox2.insert(tk.END,month+'_22')
    view_button2=tk.Button(supervisor_cashier_performance,text='View',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont,command=view_command2)
    view_button2.grid(row=6,column=0,padx=8,pady=5)
    emp_label=tk.Label(supervisor_cashier_performance,text='',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont)
    emp_label.grid(row=6,column=1,padx=8,pady=5)
    graph_button1=tk.Button(supervisor_cashier_performance,text='View Employee\nYear Round Graph',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont,command=lambda: [supervisor_cashier_performance.destroy(),create_year_round_graphs()])
    graph_button1.grid(row=7,column=0,padx=8,pady=5)
    graph_button2=tk.Button(supervisor_cashier_performance,text='Employee Comparison\nGraph',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont,command=lambda: [supervisor_cashier_performance.destroy(),create_employee_comparison_graphs()])
    graph_button2.grid(row=7,column=1,padx=8,pady=5)
    back_button=tk.Button(supervisor_cashier_performance,text='Back',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont,command=lambda: [supervisor_cashier_performance.destroy(),create_supervisor_homepage()])
    back_button.grid(row=7,column=3,padx=8,pady=5)
    supervisor_cashier_performance.mainloop()

#this function creates the view graphs page
def create_year_round_graphs():
    #this function gets details of cashier selected by user.
    def get_selected_employee(event):
        try:
            global selected_cashier_by_supervisor
            indexnumber=emp_details_listbox.curselection()[0]
            selected_cashier_by_supervisor=emp_details_listbox.get(indexnumber)
            required_text1='Selected Employee\n'+selected_cashier_by_supervisor[0]+' - '+selected_cashier_by_supervisor[1]
            selected_employee_label.configure(text=required_text1)
        except IndexError:
            pass
    
    #this displays the monthly sales of the employee as a graph.
    def view_monthly_sales():
        plt.close()
        global selected_cashier_by_supervisor
        conn=sqlite3.connect(database_name)
        cur=conn.cursor()
        cur.execute('SELECT * FROM SALES2022 WHERE EMP_ID=?',(selected_cashier_by_supervisor[0],))
        sales_data=cur.fetchall()[0][2:]
        conn.close()
        month_list=['JAN','FEB','MAR','APR','MAY','JUN','JUL','AUG','SEP','OCT','NOV','DEC']
        plt.scatter (month_list,sales_data,color='blue')
        plt.xlabel('2022 - Months')
        plt.ylabel('Sales (Rs.)')
        title_text='Monthly Sales Comparison for ' + selected_cashier_by_supervisor[0]+ '-' + selected_cashier_by_supervisor[1]
        plt.title(title_text)
        imagename='generated_graphs\\'+selected_cashier_by_supervisor[0]+ '_' + selected_cashier_by_supervisor[1]+'.png'
        plt.savefig(imagename)
        img=Image.open(imagename)
        res_img=img.resize((600,400), Image.ANTIALIAS)
        graph_image=ImageTk.PhotoImage(res_img)
        graph1_label.configure(image=graph_image)
        
    supervisor_cashier_graphs=tk.Tk()
    supervisor_cashier_graphs.title('CASHIER GRAPHS')
    supervisor_cashier_graphs.iconbitmap(icon_name)
    supervisor_cashier_graphs['background']=window_bg_color
    width=supervisor_cashier_graphs.winfo_screenwidth()-40
    height=supervisor_cashier_graphs.winfo_screenheight()-40
    supervisor_cashier_graphs.geometry('%dx%d'%(width,height))
    headerfont=font.Font(family='Bahnschrift',size=35,weight='bold',underline=1)
    buttonfont=font.Font(family='Bahnschrift',size=25,weight='bold')
    selectionfont=font.Font(family='Bahnschrift',size=15,weight='bold')
    employee_sales_label=tk.Label(supervisor_cashier_graphs,text='Employee Sales For This Year',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=headerfont)
    employee_sales_label.grid(row=0,column=0,columnspan=4)
    employee_label=tk.Label(supervisor_cashier_graphs,text='Select Employee',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont)
    employee_label.grid(row=1,column=0,padx=8,pady=5)
    emp_details_listbox=tk.Listbox(supervisor_cashier_graphs,fg=button_fg_color,borderwidth=0,font=selectionfont,height=5,width=30)
    emp_details_listbox.grid(row=1,column=1,padx=8,pady=5)
    scrollbar1=tk.Scrollbar(supervisor_cashier_graphs)
    scrollbar1.grid(row=1,column=2,pady=5)
    emp_details_listbox.configure(yscrollcommand=scrollbar1.set)
    scrollbar1.configure(command=emp_details_listbox.yview)
    emp_details_listbox.bind('<<ListboxSelect>>',get_selected_employee)
    conn=sqlite3.connect(database_name)
    cur=conn.cursor()
    cur.execute('SELECT EMP_ID , NAME FROM EMPLOYEE')
    employee_details=cur.fetchall()
    conn.close()
    emp_details_listbox.delete(0,tk.END)
    for record in employee_details:
        emp_details_listbox.insert(tk.END,record)
    selected_employee_label=tk.Label(supervisor_cashier_graphs,text='',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont)
    selected_employee_label.grid(row=1,column=3,padx=8,pady=5)
    monthly_sales_button=tk.Button(supervisor_cashier_graphs,text='View Monthly\nSales Graph',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont,command=view_monthly_sales)
    monthly_sales_button.grid(row=2,column=0,padx=8,pady=5)
    graph1_label=tk.Label(supervisor_cashier_graphs,borderwidth=0,bg=button_bg_color)
    graph1_label.grid(row=2,column=1,columnspan=3,padx=8,pady=5)
    back_button=tk.Button(supervisor_cashier_graphs,text='Back',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont,command=lambda: [supervisor_cashier_graphs.destroy(),create_supervisor_cashier_performance()])
    back_button.grid(row=3,column=0,padx=8,pady=5)
    supervisor_cashier_graphs.mainloop()

#this function creates the cashier comparison window.
def create_employee_comparison_graphs():
    #this function gets details of month selected by user.
    def get_selected_month(event):
        try:
            global selected_month_by_supervisor
            indexnumber=month_listbox.curselection()[0]
            selected_month_by_supervisor=month_listbox.get(indexnumber)
            required_text2='Selected Month\n'+selected_month_by_supervisor
            selected_month_label.configure(text=required_text2)
        except IndexError:
            pass
    
    #this function displays the comparitive graph of employee sales for selected month.
    def view_employee_sales():
        plt.close()
        global selected_month_by_supervisor
        month_selection_sql='SELECT EMP_NAME , %s FROM SALES2022'%(selected_month_by_supervisor)
        conn=sqlite3.connect(database_name)
        cur=conn.cursor()
        cur.execute(month_selection_sql)
        records=cur.fetchall()
        conn.close()
        name_list=[]
        sales_list=[]
        for i in records:
            name_list.append(i[0])
            sales_list.append(i[1])
        plt.scatter(name_list,sales_list,color='blue')
        plt.xlabel('Employee Name')
        plt.ylabel('Sales for month of '+selected_month_by_supervisor)
        title_text='Comparitive Sales of Employees For the Month of ' + selected_month_by_supervisor
        plt.title(title_text)
        graphname='generated_graphs\\'+selected_month_by_supervisor+'.png'
        plt.savefig(graphname)
        img=Image.open(graphname)
        res_img=img.resize((600,400), Image.ANTIALIAS)
        graph_image=ImageTk.PhotoImage(res_img)
        graph2_label.configure(image=graph_image)
           
    supervisor_cashier_graphs=tk.Tk()
    supervisor_cashier_graphs.title('CASHIER GRAPHS')
    supervisor_cashier_graphs.iconbitmap(icon_name)
    supervisor_cashier_graphs['background']=window_bg_color
    width=supervisor_cashier_graphs.winfo_screenwidth()-40
    height=supervisor_cashier_graphs.winfo_screenheight()-40
    supervisor_cashier_graphs.geometry('%dx%d'%(width,height))
    headerfont=font.Font(family='Bahnschrift',size=35,weight='bold',underline=1)
    buttonfont=font.Font(family='Bahnschrift',size=25,weight='bold')
    selectionfont=font.Font(family='Bahnschrift',size=15,weight='bold')
    employee_sales_label=tk.Label(supervisor_cashier_graphs,text='Employee Comparison',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=headerfont)
    employee_sales_label.grid(row=0,column=0,columnspan=4)
    selected_month_label=tk.Label(supervisor_cashier_graphs,text='',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont)
    selected_month_label.grid(row=1,column=3,padx=8,pady=5)
    month_label=tk.Label(supervisor_cashier_graphs,text='Select Month',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont)
    month_label.grid(row=1,column=0,padx=8,pady=5)
    month_listbox=tk.Listbox(supervisor_cashier_graphs,fg=button_fg_color,borderwidth=0,font=selectionfont,height=5,width=30)
    month_listbox.grid(row=1,column=1,padx=8,pady=5)
    scrollbar2=tk.Scrollbar(supervisor_cashier_graphs)
    scrollbar2.grid(row=1,column=2,pady=5)
    month_listbox.configure(yscrollcommand=scrollbar2.set)
    scrollbar2.configure(command=month_listbox.yview)
    month_listbox.bind('<<ListboxSelect>>',get_selected_month)
    month_list=['JAN','FEB','MAR','APR','MAY','JUN','JUL','AUG','SEP','OCT','NOV','DEC']
    for month in month_list:
        month_listbox.insert(tk.END,month+'_22')
    employee_sales_button=tk.Button(supervisor_cashier_graphs,text='View Employee\nSales Graph',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont,command=view_employee_sales)
    employee_sales_button.grid(row=2,column=0,padx=8,pady=5)
    graph2_label=tk.Label(supervisor_cashier_graphs,borderwidth=0,bg=button_bg_color)
    graph2_label.grid(row=2,column=1,columnspan=3,padx=8,pady=5)
    back_button=tk.Button(supervisor_cashier_graphs,text='Back',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont,command=lambda: [supervisor_cashier_graphs.destroy(),create_supervisor_cashier_performance()])
    back_button.grid(row=3,column=0,padx=8,pady=5)
    supervisor_cashier_graphs.mainloop()

#this function creates the set discount rate window.    
def create_supervisor_discount_rate():
    #this function updates the discount rate in the rate table.
    def update_command():
        global current_discount_rate
        conn=sqlite3.connect(database_name)
        cur=conn.cursor()
        cur.execute('UPDATE RATE SET DISCOUNT_RATE=?',(discount_rate_var.get(),))
        conn.commit()
        conn.close()
        conn=sqlite3.connect(database_name)
        cur=conn.cursor()
        cur.execute('SELECT * FROM RATE')
        current_discount_rate=cur.fetchall()[0][0]
        conn.close()
        discount_rate_entry.delete(0,tk.END)
        discount_rate_entry.insert(tk.END,current_discount_rate)
    supervisor_discount_rate=tk.Tk()
    supervisor_discount_rate.title('SET DISCOUNT RATES')
    supervisor_discount_rate.iconbitmap(icon_name)
    supervisor_discount_rate['background']=window_bg_color
    width=supervisor_discount_rate.winfo_screenwidth()-40
    height=supervisor_discount_rate.winfo_screenheight()-40
    supervisor_discount_rate.geometry('%dx%d'%(width,height))
    headerfont=font.Font(family='Bahnschrift',size=40,weight='bold',underline=1)
    buttonfont=font.Font(family='Bahnschrift',size=35,weight='bold')
    set_rate_header_label=tk.Label(supervisor_discount_rate,text='SET DISCOUNT RATE',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=headerfont)
    set_rate_header_label.grid(row=0,column=0,columnspan=3)
    discount_rate_label=tk.Label(supervisor_discount_rate,text='Discount Rate',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont)
    discount_rate_label.grid(row=1,column=0)
    discount_rate_var=tk.StringVar()
    discount_rate_entry=tk.Entry(supervisor_discount_rate,textvariable=discount_rate_var,font=buttonfont)
    discount_rate_entry.grid(row=1,column=1,padx=15,pady=15)
    conn=sqlite3.connect(database_name)
    cur=conn.cursor()
    cur.execute('SELECT * FROM RATE')
    current_discount_rate=cur.fetchall()[0][0]
    conn.close()
    discount_rate_entry.delete(0,tk.END)
    discount_rate_entry.insert(tk.END,current_discount_rate)
    update_button=tk.Button(supervisor_discount_rate,text='Update',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont,command=lambda: [messagebox.showinfo('Success','Discount rate has been successfully updated'),update_command()])
    update_button.grid(row=1,column=2,padx=15,pady=15)
    back_button=tk.Button(supervisor_discount_rate,text='Back',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont,command=lambda: [supervisor_discount_rate.destroy(),create_supervisor_homepage()])
    back_button.grid(row=2,column=2,padx=15,pady=15)
    supervisor_discount_rate.mainloop()

#this function creates the generate salary slip window.
def create_supervisor_salary_slip():
    #this function gets details of cashier selected by user.
    def get_selected_employee(event):
        try:
            global selected_cashier_by_supervisor
            indexnumber=emp_details_listbox.curselection()[0]
            selected_cashier_by_supervisor=emp_details_listbox.get(indexnumber)
            required_text1='Selected Employee\n'+selected_cashier_by_supervisor[0]+' - '+selected_cashier_by_supervisor[1]
            selected_employee_label.configure(text=required_text1)
        except IndexError:
            pass
    
    #this function gets details of month selected by user.
    def get_selected_month(event):
        try:
            global selected_month_by_supervisor
            indexnumber=month_listbox.curselection()[0]
            selected_month_by_supervisor=month_listbox.get(indexnumber)
            required_text2='Selected Month\n'+selected_month_by_supervisor
            selected_month_label.configure(text=required_text2)
        except IndexError:
            pass
    
    #this function generates the salary slip
    def generate_command():
        global selected_cashier_by_supervisor,selected_month_by_supervisor , emp_of_the_month
        if selected_month_by_supervisor.startswith('JAN'):
            conn=sqlite3.connect(database_name)
            cur=conn.cursor()
            cur.execute('SELECT EMP_ID , MAX(JAN_22) FROM SALES2022')
            emp_of_the_month=cur.fetchall()[0][0]
            conn.close()
            if emp_of_the_month==selected_cashier_by_supervisor[0]:
                bonus=10000
            else:
                bonus=0
        elif selected_month_by_supervisor.startswith('FEB'): 
            conn=sqlite3.connect(database_name)
            cur=conn.cursor()
            cur.execute('SELECT EMP_ID , MAX(FEB_22) FROM SALES2022')
            emp_of_the_month=cur.fetchall()[0][0]
            conn.close()
            if emp_of_the_month==selected_cashier_by_supervisor[0]:
                bonus=10000
            else:
                bonus=0
        elif selected_month_by_supervisor.startswith('MAR'): 
            conn=sqlite3.connect(database_name)
            cur=conn.cursor()
            cur.execute('SELECT EMP_ID , MAX(MAR_22) FROM SALES2022')
            emp_of_the_month=cur.fetchall()[0][0]
            conn.close()
            if emp_of_the_month==selected_cashier_by_supervisor[0]:
                bonus=10000
            else:
                bonus=0
        elif selected_month_by_supervisor.startswith('APR'): 
            conn=sqlite3.connect(database_name)
            cur=conn.cursor()
            cur.execute('SELECT EMP_ID , MAX(APR_22) FROM SALES2022')
            emp_of_the_month=cur.fetchall()[0][0]
            conn.close()
            if emp_of_the_month==selected_cashier_by_supervisor[0]:
                bonus=10000
            else:
                bonus=0
        elif selected_month_by_supervisor.startswith('MAY'): 
            conn=sqlite3.connect(database_name)
            cur=conn.cursor()
            cur.execute('SELECT EMP_ID , MAX(MAY_22) FROM SALES2022')
            emp_of_the_month=cur.fetchall()[0][0]
            conn.close()
            if emp_of_the_month==selected_cashier_by_supervisor[0]:
                bonus=10000
            else:
                bonus=0
        elif selected_month_by_supervisor.startswith('JUN'):
            conn=sqlite3.connect(database_name)
            cur=conn.cursor()
            cur.execute('SELECT EMP_ID , MAX(JUN_22) FROM SALES2022')
            emp_of_the_month=cur.fetchall()[0][0]
            conn.close()
            if emp_of_the_month==selected_cashier_by_supervisor[0]:
                bonus=10000
            else:
                bonus=0
        elif selected_month_by_supervisor.startswith('JUL'): 
            conn=sqlite3.connect(database_name)
            cur=conn.cursor()
            cur.execute('SELECT EMP_ID , MAX(JUL_22) FROM SALES2022')
            emp_of_the_month=cur.fetchall()[0][0]
            conn.close()
            if emp_of_the_month==selected_cashier_by_supervisor[0]:
                bonus=10000
            else:
                bonus=0
        elif selected_month_by_supervisor.startswith('AUG'):
            conn=sqlite3.connect(database_name)
            cur=conn.cursor()
            cur.execute('SELECT EMP_ID , MAX(AUG_22) FROM SALES2022')
            emp_of_the_month=cur.fetchall()[0][0]
            conn.close()
            if emp_of_the_month==selected_cashier_by_supervisor[0]:
                bonus=10000
            else:
                bonus=0
        elif selected_month_by_supervisor.startswith('SEP'): 
            conn=sqlite3.connect(database_name)
            cur=conn.cursor()
            cur.execute('SELECT EMP_ID , MAX(SEP_22) FROM SALES2022')
            emp_of_the_month=cur.fetchall()[0][0]
            conn.close()
            if emp_of_the_month==selected_cashier_by_supervisor[0]:
                bonus=10000
            else:
                bonus=0
        elif selected_month_by_supervisor.startswith('OCT'):
            conn=sqlite3.connect(database_name)
            cur=conn.cursor()
            cur.execute('SELECT EMP_ID , MAX(OCT_22) FROM SALES2022')
            emp_of_the_month=cur.fetchall()[0][0]
            conn.close()
            if emp_of_the_month==selected_cashier_by_supervisor[0]:
                bonus=10000
            else:
                bonus=0
        elif selected_month_by_supervisor.startswith('NOV'): 
            conn=sqlite3.connect(database_name)
            cur=conn.cursor()
            cur.execute('SELECT EMP_ID , MAX(NOV_22) FROM SALES2022')
            emp_of_the_month=cur.fetchall()[0][0]
            conn.close()
            if emp_of_the_month==selected_cashier_by_supervisor[0]:
                bonus=10000
            else:
                bonus=0
        elif selected_month_by_supervisor.startswith('DEC'):
            conn=sqlite3.connect(database_name)
            cur=conn.cursor()
            cur.execute('SELECT EMP_ID , MAX(DEC_22) FROM SALES2022')
            emp_of_the_month=cur.fetchall()[0][0]
            conn.close()
            if emp_of_the_month==selected_cashier_by_supervisor[0]:
                bonus=10000
            else:
                bonus=0
        
        generated_filename='emp_files\\'+selected_cashier_by_supervisor[0]+'_'+selected_cashier_by_supervisor[1]+'_'+selected_month_by_supervisor+'_'+'payslip.txt'
        saved_filename=selected_cashier_by_supervisor[0]+'_'+selected_cashier_by_supervisor[1]+'_'+selected_month_by_supervisor+'_'+'payslip.txt'
        month_selection_sql='SELECT %s FROM SALES2022 WHERE EMP_ID="%s"'%(selected_month_by_supervisor,selected_cashier_by_supervisor[0])
        conn=sqlite3.connect(database_name)
        cur=conn.cursor()
        cur.execute(month_selection_sql)
        month_sales=cur.fetchall()[0][0]
        commission_pay=month_sales*0.02
        conn.close()
        conn=sqlite3.connect(database_name)
        cur=conn.cursor()
        cur.execute('SELECT * FROM BASE_SALARY')
        base_salary=cur.fetchall()[0][0]
        conn.close()
        f=open(generated_filename,'w')
        top_border='------------------------------'
        payslip_text='''
        %s
        Employee ID: %s
        Employee Name: %s
        Month: %s
        %s
        Base salary: %s
        Total Sales: %s
        Commission: %s
        Employee of the month bonus: %s
        Total Salary: %s
        '''%(top_border,selected_cashier_by_supervisor[0],selected_cashier_by_supervisor[1],selected_month_by_supervisor,top_border,str(base_salary),str(month_sales),str(commission_pay),str(float(bonus)),str(base_salary+month_sales+commission_pay+bonus))
        f.write(payslip_text)
        f.close()
        conn=sqlite3.connect(database_name)
        cur=conn.cursor()
        cur.execute('INSERT INTO FILES VALUES (?)',(saved_filename,))
        conn.commit()
        conn.close()
        
    supervisor_salary_slip=tk.Tk()
    supervisor_salary_slip.title('GENERATE SALARY SLIP')
    supervisor_salary_slip.iconbitmap(icon_name)
    supervisor_salary_slip['background']=window_bg_color
    width=supervisor_salary_slip.winfo_screenwidth()-40
    height=supervisor_salary_slip.winfo_screenheight()-40
    supervisor_salary_slip.geometry('%dx%d'%(width,height))
    headerfont=font.Font(family='Bahnschrift',size=30,weight='bold',underline=1)
    buttonfont=font.Font(family='Bahnschrift',size=20,weight='bold')
    selectionfont=font.Font(family='Bahnschrift',size=12,weight='bold')
    header_label=tk.Label(supervisor_salary_slip,text='Generate Salary Slip',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=headerfont)
    header_label.grid(row=0,column=0,columnspan=4,padx=8,pady=5)
    employee_label=tk.Label(supervisor_salary_slip,text='Select Employee',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont)
    employee_label.grid(row=1,column=0,padx=8,pady=5)
    month_label=tk.Label(supervisor_salary_slip,text='Select Month',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont)
    month_label.grid(row=2,column=0,padx=8,pady=5)
    selected_employee_label=tk.Label(supervisor_salary_slip,text='',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont)
    selected_employee_label.grid(row=1,column=3,padx=8,pady=5)
    selected_month_label=tk.Label(supervisor_salary_slip,text='',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont)
    selected_month_label.grid(row=2,column=3,padx=8,pady=5)
    generate_button=tk.Button(supervisor_salary_slip,text='Generate',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont,command=lambda:[generate_command(),messagebox.showinfo('Success','Payslip has been successfully created!')])
    generate_button.grid(row=3,column=0,padx=8,pady=5)
    emp_details_listbox=tk.Listbox(supervisor_salary_slip,fg=button_fg_color,borderwidth=0,font=selectionfont,height=5,width=30)
    emp_details_listbox.grid(row=1,column=1,padx=8,pady=5)
    scrollbar1=tk.Scrollbar(supervisor_salary_slip)
    scrollbar1.grid(row=1,column=2,pady=5)
    emp_details_listbox.configure(yscrollcommand=scrollbar1.set)
    scrollbar1.configure(command=emp_details_listbox.yview)
    emp_details_listbox.bind('<<ListboxSelect>>',get_selected_employee)
    conn=sqlite3.connect(database_name)
    cur=conn.cursor()
    cur.execute('SELECT EMP_ID , NAME FROM EMPLOYEE')
    employee_details=cur.fetchall()
    conn.close()
    emp_details_listbox.delete(0,tk.END)
    for record in employee_details:
        emp_details_listbox.insert(tk.END,record)
    month_listbox=tk.Listbox(supervisor_salary_slip,fg=button_fg_color,borderwidth=0,font=selectionfont,height=5,width=30)
    month_listbox.grid(row=2,column=1,padx=8,pady=5)
    scrollbar2=tk.Scrollbar(supervisor_salary_slip)
    scrollbar2.grid(row=2,column=2,pady=5)
    month_listbox.configure(yscrollcommand=scrollbar2.set)
    scrollbar2.configure(command=month_listbox.yview)
    month_listbox.bind('<<ListboxSelect>>',get_selected_month)
    month_list=['JAN','FEB','MAR','APR','MAY','JUN','JUL','AUG','SEP','OCT','NOV','DEC']
    for month in month_list:
        month_listbox.insert(tk.END,month+'_22')
    back_button=tk.Button(supervisor_salary_slip,text='Back',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont,command=lambda: [supervisor_salary_slip.destroy(),create_supervisor_homepage()])
    back_button.grid(row=3,column=3)
    supervisor_salary_slip.mainloop()

#this function creates the view popular products window.
def create_supervisor_popular_product():
    supervisor_popular=tk.Tk()
    supervisor_popular.title('PRODUCT POPULARITY')
    supervisor_popular.iconbitmap(icon_name)
    supervisor_popular['background']=window_bg_color
    width=supervisor_popular.winfo_screenwidth()-40
    height=supervisor_popular.winfo_screenheight()-40
    supervisor_popular.geometry('%dx%d'%(width,height))
    buttonfont=font.Font(family='Bahnschrift',size=30,weight='bold')
    contentfont=font.Font(family='Bahnschrift',size=20,weight='bold')
    top_header_label=tk.Label(supervisor_popular,text='10 Most Popular Products',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont)
    top_header_label.grid(row=0,column=0,padx=15,pady=15)
    bottom_header_label=tk.Label(supervisor_popular,text='10 Least Popular Products',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont)
    bottom_header_label.grid(row=2,column=0,padx=15,pady=15)
    top_products_listbox=tk.Listbox(supervisor_popular,fg=button_fg_color,borderwidth=0,font=contentfont,height=5,width=55)
    top_products_listbox.grid(row=1,column=0,padx=15,pady=15)
    scrollbar1=tk.Scrollbar(supervisor_popular)
    scrollbar1.grid(row=1,column=1,pady=15)
    top_products_listbox.configure(yscrollcommand=scrollbar1.set)
    scrollbar1.configure(command=top_products_listbox.yview)
    top_products_listbox.bind('<<ListboxSelect>>')
    bottom_products_listbox=tk.Listbox(supervisor_popular,fg=button_fg_color,borderwidth=0,font=contentfont,height=5,width=55)
    bottom_products_listbox.grid(row=3,column=0,padx=15,pady=15)
    scrollbar2=tk.Scrollbar(supervisor_popular)
    scrollbar2.grid(row=3,column=1,pady=15)
    bottom_products_listbox.configure(yscrollcommand=scrollbar2.set)
    scrollbar2.configure(command=bottom_products_listbox.yview)
    bottom_products_listbox.bind('<<ListboxSelect>>')
    back_button=tk.Button(supervisor_popular,text='Back',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont,command=lambda: [supervisor_popular.destroy(),create_supervisor_homepage()])
    back_button.grid(row=4,column=0,padx=15,pady=15)
    conn=sqlite3.connect(database_name)
    cur=conn.cursor()
    cur.execute('SELECT * FROM INVENTORY ORDER BY UNITS_PURCHASED DESC')
    table_data=cur.fetchall()
    conn.close()
    top_products_listbox.delete(0,tk.END)
    bottom_products_listbox.delete(0,tk.END)
    for top_records in table_data[:10]:
        top_products_listbox.insert(tk.END,top_records)
    for bottom_records in table_data[-1:-11:-1]:
        bottom_products_listbox.insert(tk.END,bottom_records)
    supervisor_popular.mainloop()

#this function creates the send message window.    
def create_supervisor_send_message():
    #this function gets details of the cashier selected by the user.
    def get_selected_employee_name(event):
        try:
            global selected_name
            indexnumber=employee_name_listbox.curselection()[0]
            selected_name=employee_name_listbox.get(indexnumber)[1]
            selected_employee_name_label.configure(text=employee_name_listbox.get(indexnumber)[0]+' : '+selected_name)
        except IndexError:
            pass
     
    #this function gets details of the messagebox number selected by the user.
    def get_selected_messagebox_number(event):
        try:
            global selected_msgbox_number
            indexnumber=messagebox_number_listbox.curselection()[0]
            selected_msgbox_number=messagebox_number_listbox.get(indexnumber)
            messagebox_number_label.configure(text=selected_msgbox_number)
        except IndexError:
            pass
    
    #this function gets details of filename selected by the user.
    def get_selected_file(event):
        try:
            global selected_file
            indexnumber=attach_file_listbox.curselection()[0]
            selected_file=attach_file_listbox.get(indexnumber)
            selected_file_label.configure(text='Selected file is: \n'+selected_file)
        except IndexError:
            pass
    
    #this function updates message details in corresponding cashier's record in employee table.
    def send_message_command():
        global selected_name, selected_msg_type, selected_msgbox_number, selected_file
        if selected_msgbox_number=='MSG1':
            conn=sqlite3.connect(database_name)
            cur=conn.cursor()
            cur.execute('UPDATE EMPLOYEE SET MSG1=?, ATC1=? WHERE NAME=?',(message_entry.get('1.0','end-1c'),selected_file,selected_name))
            conn.commit()
            conn.close()
        elif selected_msgbox_number=='MSG2':
            conn=sqlite3.connect(database_name)
            cur=conn.cursor()
            cur.execute('UPDATE EMPLOYEE SET MSG2=?, ATC2=? WHERE NAME=?',(message_entry.get('1.0','end-1c'),selected_file,selected_name))
            conn.commit()
            conn.close()
        elif selected_msgbox_number=='MSG3':
            conn=sqlite3.connect(database_name)
            cur=conn.cursor()
            cur.execute('UPDATE EMPLOYEE SET MSG3=?, ATC3=? WHERE NAME=?',(message_entry.get('1.0','end-1c'),selected_file,selected_name))
            conn.commit()
            conn.close()
        elif selected_msgbox_number=='MSG4':
            conn=sqlite3.connect(database_name)
            cur=conn.cursor()
            cur.execute('UPDATE EMPLOYEE SET MSG4=?, ATC4=? WHERE NAME=?',(message_entry.get('1.0','end-1c'),selected_file,selected_name))
            conn.commit()
            conn.close()
        elif selected_msgbox_number=='MSG5':
            conn=sqlite3.connect(database_name)
            cur=conn.cursor()
            cur.execute('UPDATE EMPLOYEE SET MSG5=?, ATC5=? WHERE NAME=?',(message_entry.get('1.0','end-1c'),selected_file,selected_name))
            conn.commit()
            conn.close()

    supervisor_send_message=tk.Tk()
    supervisor_send_message.title('SEND MESSAGE')
    supervisor_send_message.iconbitmap(icon_name)
    supervisor_send_message['background']=window_bg_color
    width=supervisor_send_message.winfo_screenwidth()-40
    height=supervisor_send_message.winfo_screenheight()-40
    supervisor_send_message.geometry('%dx%d'%(width,height))
    selectionfont=font.Font(family='Bahnschrift',size=15,weight='bold')
    buttonfont=font.Font(family='Bahnschrift',size=20,weight='bold')
    labelfont=font.Font(family='Bahnschrift',size=40,weight='bold',underline=1)
    header_label=tk.Label(supervisor_send_message,text='SEND MESSAGE TO EMPLOYEES',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=labelfont)
    header_label.grid(row=0,column=0,padx=15,pady=10,columnspan=4)
    employee_name_label=tk.Label(supervisor_send_message,text='Select Employee Name: ',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont)
    employee_name_label.grid(row=1,column=0,padx=15,pady=10)
    enter_message_label=tk.Label(supervisor_send_message,text='Enter Message: ',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont)
    enter_message_label.grid(row=2,column=0,padx=15,pady=10)
    employee_msgbox_number_label=tk.Label(supervisor_send_message,text='Select Message Box Number: ',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont)
    employee_msgbox_number_label.grid(row=3,column=0,padx=15,pady=10)
    employee_name_listbox=tk.Listbox(supervisor_send_message,fg=button_fg_color,borderwidth=0,font=selectionfont,height=3,width=20)
    employee_name_listbox.grid(row=1,column=1,padx=15,pady=10)
    scrollbar1=tk.Scrollbar(supervisor_send_message)
    scrollbar1.grid(row=1,column=2)
    employee_name_listbox.configure(yscrollcommand=scrollbar1.set)
    scrollbar1.configure(command=employee_name_listbox.yview)
    employee_name_listbox.bind('<<ListboxSelect>>',get_selected_employee_name)
    messagebox_number_listbox=tk.Listbox(supervisor_send_message,fg=button_fg_color,borderwidth=0,font=selectionfont,height=3,width=20)
    messagebox_number_listbox.grid(row=3,column=1,padx=15,pady=10)
    scrollbar3=tk.Scrollbar(supervisor_send_message)
    scrollbar3.grid(row=3,column=2)
    messagebox_number_listbox.configure(yscrollcommand=scrollbar3.set)
    scrollbar3.configure(command=messagebox_number_listbox.yview)
    messagebox_number_listbox.bind('<<ListboxSelect>>',get_selected_messagebox_number)
    attach_file_listbox=tk.Listbox(supervisor_send_message,fg=button_fg_color,borderwidth=0,font=selectionfont,height=3,width=20)
    attach_file_listbox.grid(row=2,column=3,padx=15,pady=10)
    scrollbar4=tk.Scrollbar(supervisor_send_message)
    scrollbar4.grid(row=2,column=4)
    attach_file_listbox.configure(yscrollcommand=scrollbar4.set)
    scrollbar4.configure(command=attach_file_listbox.yview)
    attach_file_listbox.bind('<<ListboxSelect>>',get_selected_file)
    message_entry=scrolledtext.ScrolledText(supervisor_send_message,font=selectionfont,height=2,width=25)
    message_entry.grid(row=2,column=1,padx=15,pady=10)
    send_button=tk.Button(supervisor_send_message,text='Send',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont,command=lambda: [messagebox.showinfo('Success','Your message has been sent'),send_message_command()])
    send_button.grid(row=4,column=1,padx=15,pady=10)
    back_button=tk.Button(supervisor_send_message,text='Back',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont,command=lambda: [supervisor_send_message.destroy(),create_supervisor_homepage()])
    back_button.grid(row=5,column=1,padx=15,pady=10)
    selected_employee_name_label=tk.Label(supervisor_send_message,text='',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont)
    selected_employee_name_label.grid(row=1,column=3,padx=15,pady=10)
    messagebox_number_label=tk.Label(supervisor_send_message,text='',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont)
    messagebox_number_label.grid(row=3,column=3,padx=15,pady=10)
    selected_file_label=tk.Label(supervisor_send_message,text='',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont)
    selected_file_label.grid(row=4,column=3,padx=15,pady=10)
    conn=sqlite3.connect(database_name)
    cur=conn.cursor()
    cur.execute('SELECT * FROM EMPLOYEE')
    record_data=cur.fetchall()
    conn.close()
    messagebox_number_listbox.delete(0,tk.END)
    for i in range(1,6):
        messagebox_number_listbox.insert(tk.END,'MSG'+str(i))
    employee_name_listbox.delete(0,tk.END)
    for records in record_data:
        employee_name_listbox.insert(tk.END,records[0:2])
    conn=sqlite3.connect(database_name)
    cur=conn.cursor()
    cur.execute('SELECT * FROM FILES')
    file_data=cur.fetchall()
    conn.close()
    attach_file_listbox.delete(0,tk.END)
    for file in file_data:
        attach_file_listbox.insert(tk.END,file[0]) 
    supervisor_send_message.mainloop()

#this function creates the cashier homepage.    
def create_cashier_homepage():
    cashier_homepage=tk.Tk()
    cashier_homepage.title('HOME - CASHIER ACCOUNT')
    cashier_homepage.iconbitmap(icon_name)
    cashier_homepage['background']=window_bg_color
    width=cashier_homepage.winfo_screenwidth()-40
    height=cashier_homepage.winfo_screenheight()-40
    cashier_homepage.geometry('%dx%d'%(width,height))
    labelfont=font.Font(family='Bahnschrift',size=40,weight='bold',underline=1)
    buttonfont=font.Font(family='Bahnschrift',size=34,weight='bold')
    header_label=tk.Label(cashier_homepage,text='CASHIER HOMEPAGE',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=labelfont)
    header_label.grid(row=0,column=0,padx=15,pady=15,columnspan=2)
    view_cashier_profile=tk.Button(cashier_homepage,text='VIEW PROFILE',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont,command=lambda: [cashier_homepage.destroy(),create_cashier_view_profile()])
    view_cashier_profile.grid(row=1,column=0,padx=15,pady=15)
    view_customer_data=tk.Button(cashier_homepage,text='VIEW CUSTOMER DATA',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont,command=lambda: [cashier_homepage.destroy(),create_cashier_customer_data()])
    view_customer_data.grid(row=2,column=0,padx=15,pady=15)
    billing_counter=tk.Button(cashier_homepage,text='BILLING COUNTER',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont,command=lambda: [cashier_homepage.destroy(),create_cashier_billing_counter()])
    billing_counter.grid(row=3,column=0,padx=15,pady=15)
    view_messages=tk.Button(cashier_homepage,text='VIEW MESSAGES',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont,command=lambda: [cashier_homepage.destroy(),create_cashier_view_message()])
    view_messages.grid(row=1,column=1,padx=15,pady=15)
    view_product_inventory=tk.Button(cashier_homepage,text='VIEW PRODUCT INVENTORY',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont,command=lambda: [cashier_homepage.destroy(),create_cashier_inventory()])
    view_product_inventory.grid(row=2,column=1,padx=15,pady=15)
    logout_button=tk.Button(cashier_homepage,text='LOGOUT',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont,command=cashier_homepage.destroy)
    logout_button.grid(row=3,column=1,padx=20,pady=15)
    cashier_homepage.mainloop()

#this function creates the cashier's product inventory page.
def create_cashier_inventory():
    #this function gets details of product selected by the user.
    def get_selected_product(event):
        try:
            global selected_cashier_product
            indexnumber=product_details_listbox.curselection()[0]
            selected_cashier_product=product_details_listbox.get(indexnumber)
            selected_product_id_label.configure(text=selected_cashier_product[0])
            product_name_entry.delete(0,tk.END)
            product_name_entry.insert(tk.END,selected_cashier_product[1])
            product_category_entry.delete(0,tk.END)
            product_category_entry.insert(tk.END,selected_cashier_product[2])
            selected_gst_rate_entry.delete(0,tk.END)
            selected_gst_rate_entry.insert(tk.END,selected_cashier_product[3])
            product_cost_entry.delete(0,tk.END)
            product_cost_entry.insert(tk.END,selected_cashier_product[4])
            product_unit_entry.delete(0,tk.END)
            product_unit_entry.insert(tk.END,selected_cashier_product[5])
            product_available_entry.delete(0,tk.END)
            product_available_entry.insert(tk.END,selected_cashier_product[6])
            product_purchased_entry.delete(0,tk.END)
            product_purchased_entry.insert(tk.END,selected_cashier_product[7])
        except IndexError:
            pass
    
    #this function clears all the entry fields.
    def clear_command():
        selected_product_id_label.configure(text='')
        product_name_entry.delete(0,tk.END)
        product_category_entry.delete(0,tk.END)
        selected_gst_rate_entry.delete(0,tk.END)
        product_cost_entry.delete(0,tk.END)
        product_unit_entry.delete(0,tk.END)
        product_available_entry.delete(0,tk.END)  
        product_purchased_entry.delete(0,tk.END) 
    
    #this function gets details of product category selected by the user.
    def get_selected_category(event):
        try:
            global selected_cashier_category
            indexnumber=category_listbox.curselection()[0]
            selected_cashier_category=category_listbox.get(indexnumber)
            selected_category_label.configure(text='Selected Category:\n'+selected_cashier_category)
        except IndexError:
            pass
    #this function displays details of all the products in a listbox.   
    def view_all_command():
        conn=sqlite3.connect(database_name)
        cur=conn.cursor()
        cur.execute('SELECT * FROM INVENTORY')
        product_details=cur.fetchall()
        conn.close()
        product_details_listbox.delete(0,tk.END)
        for record in product_details:
            product_details_listbox.insert(tk.END,record)
    
    #this function updates the product details in the inventory table.
    def update_command():
        conn=sqlite3.connect(database_name)
        cur=conn.cursor()
        cur.execute('UPDATE INVENTORY SET PROD_NAME=?,PROD_CATEGORY=?,GST_RATE=?,PROD_COST_PER_UNIT=?,UNIT_OF_MEASUREMENT=?,UNITS_AVAILABLE=?,UNITS_PURCHASED=? WHERE PROD_ID=?',(product_name_var.get().replace(' ','_'),product_category_var.get().replace(' ','_'),gst_rate_var.get(),float(product_cost_var.get()),product_unit_var.get().replace(' ','_'),int(product_available_var.get()),int(product_purchased_var.get()),selected_cashier_product[0]))
        conn.commit()
        conn.close()
    
    #this function deletes the product record from the inventory table.
    def delete_command():
        global selected_cashier_product
        conn=sqlite3.connect(database_name)
        cur=conn.cursor()
        cur.execute('DELETE FROM INVENTORY WHERE PROD_ID=?',(selected_cashier_product[0],))
        conn.commit()
        conn.close()

    #this function adds the product record to the inventory table.
    def add_command():
        conn=sqlite3.connect(database_name)
        cur=conn.cursor()
        cur.execute('SELECT * FROM INVENTORY')
        rows=cur.fetchall()
        conn.close()
        last_id=rows[-1][0]
        generated_prod_id='PR'+str(int(last_id.replace('PR',''))+1)
        conn=sqlite3.connect(database_name)
        cur=conn.cursor()
        cur.execute('INSERT INTO INVENTORY VALUES (?,?,?,?,?,?,?,?)',(generated_prod_id,product_name_var.get().replace(' ','_'),product_category_var.get().replace(' ','_'),gst_rate_var.get(),float(product_cost_var.get()),product_unit_var.get().replace(' ','_'),int(product_available_var.get()),int(product_purchased_var.get())))
        conn.commit()
        conn.close()
   
    #this function displays details of all products belonging to a particular category.
    def view_category_command():
        conn=sqlite3.connect(database_name)
        cur=conn.cursor()
        cur.execute('SELECT * FROM INVENTORY WHERE PROD_CATEGORY=?',(selected_cashier_category,))
        product_details=cur.fetchall()
        conn.close()
        product_details_listbox.delete(0,tk.END)
        for record in product_details:
            product_details_listbox.insert(tk.END,record)

    cashier_product_inventory=tk.Tk()
    cashier_product_inventory.title('PRODUCT INVENTORY')
    cashier_product_inventory.iconbitmap(icon_name)
    cashier_product_inventory['background']=window_bg_color
    width=cashier_product_inventory.winfo_screenwidth()-40
    height=cashier_product_inventory.winfo_screenheight()-40
    cashier_product_inventory.geometry('%dx%d'%(width,height))
    headerfont=font.Font(family='Bahnschrift',size=30,weight='bold',underline=1)
    buttonfont=font.Font(family='Bahnschrift',size=20,weight='bold')
    selectionfont=font.Font(family='Bahnschrift',size=12,weight='bold')
    header_label=tk.Label(cashier_product_inventory,text='PRODUCT INVENTORY',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=headerfont)
    header_label.grid(row=0,column=0,padx=10,pady=8,columnspan=4)
    view_all_button=tk.Button(cashier_product_inventory,text='View All Products',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont,command=view_all_command)
    view_all_button.grid(row=1,column=0,padx=10,pady=8)
    update_button=tk.Button(cashier_product_inventory,text='Update',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont,command=update_command)
    update_button.grid(row=1,column=1,padx=10,pady=8)
    delete_button=tk.Button(cashier_product_inventory,text='Delete',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont,command=delete_command)
    delete_button.grid(row=1,column=2,padx=10,pady=8)
    add_button=tk.Button(cashier_product_inventory,text='Add',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont,command=add_command)
    add_button.grid(row=1,column=3,padx=10,pady=8)
    clear_button=tk.Button(cashier_product_inventory,text='Clear Selection',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont,command=clear_command)
    clear_button.grid(row=1,column=4,padx=10,pady=8)
    view_category_button=tk.Button(cashier_product_inventory,text='View Products in\nSelected Category',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=selectionfont,command=view_category_command)
    view_category_button.grid(row=2,column=4,padx=10,pady=8)
    select_category_label=tk.Label(cashier_product_inventory,text='Select Category',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont)
    select_category_label.grid(row=2,column=0,padx=10,pady=8)
    product_id_label=tk.Label(cashier_product_inventory,text='Product ID',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont)
    product_id_label.grid(row=3,column=0,padx=10,pady=8)
    product_name_label=tk.Label(cashier_product_inventory,text='Product Name',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont)
    product_name_label.grid(row=4,column=0,padx=10,pady=8)
    product_category_label=tk.Label(cashier_product_inventory,text='Product Category',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont)
    product_category_label.grid(row=5,column=0,padx=10,pady=8)
    gst_rate_label=tk.Label(cashier_product_inventory,text='GST Rate',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont)
    gst_rate_label.grid(row=6,column=0,padx=10,pady=8)
    cost_label=tk.Label(cashier_product_inventory,text='Cost Per Unit',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont)
    cost_label.grid(row=7,column=0,padx=10,pady=8)
    unit_label=tk.Label(cashier_product_inventory,text='Unit of Measurement',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont)
    unit_label.grid(row=8,column=0,padx=10,pady=8)
    unit_available_label=tk.Label(cashier_product_inventory,text='Units Available',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont)
    unit_available_label.grid(row=9,column=0,padx=10,pady=8)
    unit_purchased_label=tk.Label(cashier_product_inventory,text='Total Units Purchased\nTill Date',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont)
    unit_purchased_label.grid(row=10,column=0,padx=10,pady=8)
    selected_product_id_label=tk.Label(cashier_product_inventory,text='',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont)
    selected_product_id_label.grid(row=3,column=1,padx=10,pady=8)
    product_name_var=tk.StringVar()
    product_name_entry=tk.Entry(cashier_product_inventory,textvariable=product_name_var,font=buttonfont)
    product_name_entry.grid(row=4,column=1,padx=10,pady=8)
    product_category_var=tk.StringVar()
    product_category_entry=tk.Entry(cashier_product_inventory,textvariable=product_category_var,font=buttonfont)
    product_category_entry.grid(row=5,column=1,padx=10,pady=8)
    gst_rate_var=tk.StringVar()
    selected_gst_rate_entry=tk.Entry(cashier_product_inventory,textvariable=gst_rate_var,font=buttonfont)
    selected_gst_rate_entry.grid(row=6,column=1,padx=10,pady=8)
    product_cost_var=tk.StringVar()
    product_cost_entry=tk.Entry(cashier_product_inventory,textvariable=product_cost_var,font=buttonfont)
    product_cost_entry.grid(row=7,column=1,padx=10,pady=8)
    product_unit_var=tk.StringVar()
    product_unit_entry=tk.Entry(cashier_product_inventory,textvariable=product_unit_var,font=buttonfont)
    product_unit_entry.grid(row=8,column=1,padx=10,pady=8)
    product_available_var=tk.StringVar()
    product_available_entry=tk.Entry(cashier_product_inventory,textvariable=product_available_var,font=buttonfont)
    product_available_entry.grid(row=9,column=1,padx=10,pady=8)
    product_purchased_var=tk.StringVar()
    product_purchased_entry=tk.Entry(cashier_product_inventory,textvariable=product_purchased_var,font=buttonfont)
    product_purchased_entry.grid(row=10,column=1,padx=10,pady=8)
    selected_category_label=tk.Label(cashier_product_inventory,text='',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=selectionfont)
    selected_category_label.grid(row=2,column=3,padx=10,pady=8)
    category_listbox=tk.Listbox(cashier_product_inventory,fg=button_fg_color,borderwidth=0,font=selectionfont,height=3,width=20)
    category_listbox.grid(row=2,column=1,pady=8)
    scrollbar1=tk.Scrollbar(cashier_product_inventory)
    scrollbar1.grid(row=2,column=2,pady=8)
    category_listbox.configure(yscrollcommand=scrollbar1.set)
    scrollbar1.configure(command=category_listbox.yview)
    category_listbox.bind('<<ListboxSelect>>',get_selected_category)
    conn=sqlite3.connect(database_name)
    cur=conn.cursor()
    cur.execute('SELECT PROD_CATEGORY FROM INVENTORY')
    category_list=cur.fetchall()
    conn.close()
    final_categories=[]
    category_listbox.delete(0,tk.END)
    for i in category_list:
        if i[0] not in final_categories:
            final_categories.append(i[0])
    for category in final_categories:
        category_listbox.insert(tk.END,category)
    product_details_listbox=tk.Listbox(cashier_product_inventory,fg=button_fg_color,borderwidth=0,font=selectionfont,height=15,width=55)
    product_details_listbox.grid(row=3,column=2,pady=8,rowspan=8,columnspan=3)
    scrollbar2=tk.Scrollbar(cashier_product_inventory)
    scrollbar2.grid(row=3,column=5,rowspan=8,pady=8)
    product_details_listbox.configure(yscrollcommand=scrollbar2.set)
    scrollbar2.configure(command=product_details_listbox.yview)
    product_details_listbox.bind('<<ListboxSelect>>',get_selected_product)
    back_button=tk.Button(cashier_product_inventory,text='Back',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont,command=lambda: [cashier_product_inventory.destroy(),create_cashier_homepage()])
    back_button.grid(row=11,column=3,pady=8)
    cashier_product_inventory.mainloop()

#this function creates the view customer details window.    
def create_cashier_customer_data():
    #this function gets details of customer selected by user.
    def get_selected_customer(event):
        try:
            global selected_customer_by_cashier
            indexnumber=cust_details_listbox.curselection()[0]
            selected_customer_by_cashier=cust_details_listbox.get(indexnumber)
            selected_id_label.configure(text=selected_customer_by_cashier[0])
            name_entry.delete(0,tk.END)
            name_entry.insert(tk.END,selected_customer_by_cashier[1])
            number_entry.delete(0,tk.END)
            number_entry.insert(tk.END,selected_customer_by_cashier[2])
            email_entry.delete(0,tk.END)
            email_entry.insert(tk.END,selected_customer_by_cashier[3])
            
        except IndexError:
            pass
    
    #this function displays details of all customers in a listbox.
    def view_command():
        conn=sqlite3.connect(database_name)
        cur=conn.cursor()
        cur.execute('SELECT * FROM CUSTOMER')
        customer_details=cur.fetchall()
        conn.close()
        cust_details_listbox.delete(0,tk.END)
        for record in customer_details:
            cust_details_listbox.insert(tk.END,record)
    
    #this function adds the record to the customer table.
    def add_command():
        conn=sqlite3.connect(database_name)
        cur=conn.cursor()
        cur.execute('SELECT * FROM CUSTOMER')
        rows=cur.fetchall()
        conn.close()
        last_id=rows[-1][0]
        generated_cust_id='CT'+str(int(last_id.replace('CT',''))+1)
        conn=sqlite3.connect(database_name)
        cur=conn.cursor()
        cur.execute('INSERT INTO CUSTOMER VALUES (?,?,?,?)',(generated_cust_id,name_var.get(),int(number_var.get()),email_var.get()))
        conn.commit()
        conn.close()
    
    #this function deletes the record from the customer table.
    def delete_command():
        global selected_customer_by_cashier
        conn=sqlite3.connect(database_name)
        cur=conn.cursor()
        cur.execute('DELETE FROM CUSTOMER WHERE CUST_ID=?',(selected_customer_by_cashier[0],))
        conn.commit()
        conn.close()

    #this function updates customer details in customer table.
    def update_command():
        global selected_customer_by_cashier
        conn=sqlite3.connect(database_name)
        cur=conn.cursor()
        cur.execute('UPDATE CUSTOMER SET NAME=?,PH_NO=?,EMAIL_ID=? WHERE CUST_ID=?',(name_var.get(),int(number_var.get()),email_var.get(),selected_customer_by_cashier[0]))
        conn.commit()
        conn.close()
    
    #this function clears all the entry fields.
    def clear_command():
        selected_id_label.configure(text='')
        name_entry.delete(0,tk.END)
        number_entry.delete(0,tk.END)
        email_entry.delete(0,tk.END)

    cashier_customer_data=tk.Tk()
    cashier_customer_data.title('CUSTOMER DATA')
    cashier_customer_data.iconbitmap(icon_name)
    cashier_customer_data['background']=window_bg_color
    width=cashier_customer_data.winfo_screenwidth()-40
    height=cashier_customer_data.winfo_screenheight()-40
    cashier_customer_data.geometry('%dx%d'%(width,height))
    headerfont=font.Font(family='Bahnschrift',size=30,weight='bold',underline=1)
    buttonfont=font.Font(family='Bahnschrift',size=20,weight='bold')
    selectionfont=font.Font(family='Bahnschrift',size=12,weight='bold')
    header_label=tk.Label(cashier_customer_data,text='CUSTOMER DATA',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=headerfont)
    header_label.grid(row=0,column=0,columnspan=3,padx=8,pady=5)
    id_label=tk.Label(cashier_customer_data,text='Customer ID: ',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont)
    id_label.grid(row=1,column=0,padx=8,pady=5)
    name_label=tk.Label(cashier_customer_data,text='Name: ',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont)
    name_label.grid(row=2,column=0,padx=8,pady=5)
    number_label=tk.Label(cashier_customer_data,text='Phone Number: ',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont)
    number_label.grid(row=3,column=0,padx=8,pady=5)
    email_label=tk.Label(cashier_customer_data,text='Email ID: ',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont)
    email_label.grid(row=4,column=0,padx=8,pady=5)
    selected_id_label=tk.Label(cashier_customer_data,text='',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont)
    selected_id_label.grid(row=1,column=1,padx=8,pady=5)
    name_var=tk.StringVar()
    name_entry=tk.Entry(cashier_customer_data,textvariable=name_var,font=buttonfont)
    name_entry.grid(row=2,column=1,padx=8,pady=5)
    number_var=tk.StringVar()
    number_entry=tk.Entry(cashier_customer_data,textvariable=number_var,font=buttonfont)
    number_entry.grid(row=3,column=1,padx=8,pady=5)
    email_var=tk.StringVar()
    email_entry=tk.Entry(cashier_customer_data,textvariable=email_var,font=buttonfont)
    email_entry.grid(row=4,column=1,padx=8,pady=5)
    view_button=tk.Button(cashier_customer_data,text='View',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont,command=view_command)
    view_button.grid(row=5,column=0,padx=8,pady=5)
    add_button=tk.Button(cashier_customer_data,text='Add',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont,command=add_command)
    add_button.grid(row=5,column=1,padx=8,pady=5)
    delete_button=tk.Button(cashier_customer_data,text='Delete',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont,command=delete_command)
    delete_button.grid(row=6,column=1,padx=8,pady=5)
    update_button=tk.Button(cashier_customer_data,text='Update',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont,command=update_command)
    update_button.grid(row=6,column=0,padx=8,pady=5)
    clear_button=tk.Button(cashier_customer_data,text='Clear Selection',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont,command=clear_command)
    clear_button.grid(row=7,column=0,padx=8,pady=5)
    cust_details_listbox=tk.Listbox(cashier_customer_data,fg=button_fg_color,borderwidth=0,font=selectionfont,height=12,width=60)
    cust_details_listbox.grid(row=1,column=2,padx=8,pady=5,rowspan=4)
    scrollbar1=tk.Scrollbar(cashier_customer_data)
    scrollbar1.grid(row=1,column=3,pady=5,rowspan=4)
    cust_details_listbox.configure(yscrollcommand=scrollbar1.set)
    scrollbar1.configure(command=cust_details_listbox.yview)
    scrollbar2=tk.Scrollbar(cashier_customer_data,orient=tk.HORIZONTAL)
    scrollbar2.grid(row=5,column=2,pady=5)
    cust_details_listbox.configure(xscrollcommand=scrollbar2.set)
    scrollbar2.configure(command=cust_details_listbox.xview)
    cust_details_listbox.bind('<<ListboxSelect>>',get_selected_customer)
    back_button=tk.Button(cashier_customer_data,text='Back',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont,command=lambda: [cashier_customer_data.destroy(),create_cashier_homepage()])
    back_button.grid(row=7,column=1,padx=8,pady=5)
    cashier_customer_data.mainloop()

#this function creates the cashier's view profile page.    
def create_cashier_view_profile():
    cashier_view_profile=tk.Tk()
    cashier_view_profile.title('PROFILE')
    cashier_view_profile.iconbitmap(icon_name)
    cashier_view_profile['background']=window_bg_color
    width=cashier_view_profile.winfo_screenwidth()-40
    height=cashier_view_profile.winfo_screenheight()-40
    cashier_view_profile.geometry('%dx%d'%(width,height))
    headerfont=font.Font(family='Bahnschrift',size=30,weight='bold',underline=1)
    buttonfont=font.Font(family='Bahnschrift',size=20,weight='bold')
    header_label=tk.Label(cashier_view_profile,text='PROFILE',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=headerfont)
    header_label.grid(row=0,column=0,padx=15,pady=8,columnspan=2)
    cashier_id_label=tk.Label(cashier_view_profile,text='Employee ID: ',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont)
    cashier_id_label.grid(row=1,column=0,padx=15,pady=8)
    cashier_name_label=tk.Label(cashier_view_profile,text='Name: ',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont)
    cashier_name_label.grid(row=2,column=0,padx=15,pady=8)
    cashier_DOB_label=tk.Label(cashier_view_profile,text='Date of Birth: ',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont)
    cashier_DOB_label.grid(row=3,column=0,padx=15,pady=8)
    cashier_age_label=tk.Label(cashier_view_profile,text='Age: ',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont)
    cashier_age_label.grid(row=4,column=0,padx=15,pady=8)
    cashier_gender_label=tk.Label(cashier_view_profile,text='Gender: ',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont)
    cashier_gender_label.grid(row=5,column=0,padx=15,pady=8)
    cashier_address_label=tk.Label(cashier_view_profile,text='Address: ',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont)
    cashier_address_label.grid(row=6,column=0,padx=15,pady=8)
    cashier_number_label=tk.Label(cashier_view_profile,text='Phone Number: ',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont)
    cashier_number_label.grid(row=7,column=0,padx=15,pady=8)
    cashier_email_label=tk.Label(cashier_view_profile,text='Email ID: ',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont)
    cashier_email_label.grid(row=8,column=0,padx=15,pady=8)
    cashier_username_label=tk.Label(cashier_view_profile,text='Username: ',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont)
    cashier_username_label.grid(row=9,column=0,padx=15,pady=8)
    cashier_password_label=tk.Label(cashier_view_profile,text='Password: ',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont)
    cashier_password_label.grid(row=10,column=0,padx=15,pady=8)
    conn=sqlite3.connect(database_name)
    cur=conn.cursor()
    cur.execute('SELECT * FROM EMPLOYEE WHERE EMP_ID=?',(current_cashier_user,))
    cashier_record=cur.fetchall()[0]
    conn.close()
    displayed_cashier_id_label=tk.Label(cashier_view_profile,text=cashier_record[0],bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont)
    displayed_cashier_id_label.grid(row=1,column=1,padx=15,pady=8)
    displayed_name_label=tk.Label(cashier_view_profile,text=cashier_record[1],bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont)
    displayed_name_label.grid(row=2,column=1,padx=15,pady=8)
    displayed_DOB_label=tk.Label(cashier_view_profile,text=cashier_record[2],bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont)
    displayed_DOB_label.grid(row=3,column=1,padx=15,pady=8)
    displayed_age_label=tk.Label(cashier_view_profile,text=cashier_record[3],bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont)
    displayed_age_label.grid(row=4,column=1,padx=15,pady=8)
    displayed_gender_label=tk.Label(cashier_view_profile,text=cashier_record[4],bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont)
    displayed_gender_label.grid(row=5,column=1,padx=15,pady=8)
    displayed_address_label=tk.Label(cashier_view_profile,text=cashier_record[5],bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont)
    displayed_address_label.grid(row=6,column=1,padx=15,pady=8)
    displayed_number_label=tk.Label(cashier_view_profile,text=cashier_record[6],bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont)
    displayed_number_label.grid(row=7,column=1,padx=15,pady=8)
    displayed_email_label=tk.Label(cashier_view_profile,text=cashier_record[7],bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont)
    displayed_email_label.grid(row=8,column=1,padx=15,pady=8)
    displayed_username_label=tk.Label(cashier_view_profile,text=cashier_record[8],bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont)
    displayed_username_label.grid(row=9,column=1,padx=15,pady=8)
    displayed_password_label=tk.Label(cashier_view_profile,text=cashier_record[9],bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont)
    displayed_password_label.grid(row=10,column=1,padx=15,pady=8)
    back_button=tk.Button(cashier_view_profile,text='Back',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont,command=lambda: [cashier_view_profile.destroy(),create_cashier_homepage()])
    back_button.grid(row=11,column=1,padx=15,pady=8)
    cashier_view_profile.mainloop()

#this function creates the billing counter page.
def create_cashier_billing_counter():
    #this function gets details of customer selected by the user.
    def get_selected_customer(event):
        try:
            global selected_customer_by_cashier
            indexnumber=cust_details_listbox.curselection()[0]
            selected_customer_by_cashier=cust_details_listbox.get(indexnumber)
            displayed_customer_id_label.configure(text=selected_customer_by_cashier[0])
            displayed_customer_name_label.configure(text=selected_customer_by_cashier[1])
            displayed_customer_phone_label.configure(text=selected_customer_by_cashier[2])
        except IndexError:
            pass
    
    #this function gets details of product category selected by the user.
    def get_selected_category(event):
        try:
            global selected_cashier_category
            indexnumber=category_listbox.curselection()[0]
            selected_cashier_category=category_listbox.get(indexnumber)
            selected_category_label.configure(text='Selected Category:\n'+selected_cashier_category)
            conn=sqlite3.connect(database_name)
            cur=conn.cursor()
            cur.execute('SELECT * FROM INVENTORY WHERE PROD_CATEGORY=?',(selected_cashier_category,))
            product_details=cur.fetchall()
            conn.close()
            product_details_listbox.delete(0,tk.END)
            for record in product_details:
                product_details_listbox.insert(tk.END,record[0:2])
        except IndexError:
            pass
    
    #this function gets details of product selected by the user.
    def get_selected_product(event):
        try:
            global selected_cashier_product
            indexnumber=product_details_listbox.curselection()[0]
            selected_cashier_product=product_details_listbox.get(indexnumber)
            selected_product_label.configure(text='Selected Product:\n'+selected_cashier_product[1])
        except IndexError:
            pass
    
    #this function gets details of product selected from listbox.
    def get_selected_bill_product(event):
        try:
            global selected_bill_product
            indexnumber=bill_listbox.curselection()[0]
            selected_bill_product=bill_listbox.get(indexnumber)
        except IndexError:
            pass
    
    #this function adds the product details to the listbox to eventually create the bill.
    def add_command():
        global total_bill_cost,total_bill_gst,total_bill_discount,total_bill_gtotal, bill_products, selected_cashier_product
        conn=sqlite3.connect(database_name)
        cur=conn.cursor()
        cur.execute('SELECT PROD_COST_PER_UNIT,GST_RATE FROM INVENTORY WHERE PROD_ID=?',(selected_cashier_product[0],))
        prod_record=cur.fetchall()[0]
        cost=prod_record[0]
        gst_rate=prod_record[1]
        conn.close()
        bill_products.append([selected_cashier_product[0],'-',selected_cashier_product[1],'-',str(cost),'-',str(count_var.get()),'-',str(round(cost*int(count_var.get()),1)),'-',str(round(gst_rate/100*cost*int(count_var.get()),1))])
        bill_listbox.delete(0,tk.END)
        for product in bill_products:
            bill_listbox.insert(tk.END,product)
        conn=sqlite3.connect(database_name)
        cur=conn.cursor()
        cur.execute('UPDATE INVENTORY SET UNITS_AVAILABLE=UNITS_AVAILABLE-?,UNITS_PURCHASED=UNITS_PURCHASED+? WHERE PROD_ID=?',(int(count_var.get()),int(count_var.get()),selected_cashier_product[0]))
        conn.commit()
        conn.close()
        total_bill_cost+=round(int(count_var.get())*cost,1)
        total_bill_gst+=round(int(gst_rate)/100*cost*int(count_var.get()),1)
        total_bill_discount=round(total_bill_cost*disc_rate/100,1)
        total_bill_gtotal=round(total_bill_cost+total_bill_gst-total_bill_discount,1)
        calculated_bill_total_label.configure(text='Rs. '+ str(total_bill_cost))
        calculated_bill_gst_label.configure(text='Rs. '+ str(total_bill_gst))
        calculated_bill_discount_label.configure(text='Rs. '+ str(total_bill_discount))
        calculated_bill_gtotal_label.configure(text='Rs. '+ str(total_bill_gtotal))
    
    #this function deletes the selected product from the bill (listbox).
    def delete_command():
        global total_bill_cost,total_bill_gst,total_bill_discount,total_bill_gtotal , selected_bill_product, bill_products
        conn=sqlite3.connect(database_name)
        cur=conn.cursor()
        cur.execute('UPDATE INVENTORY SET UNITS_AVAILABLE=UNITS_AVAILABLE+?,UNITS_PURCHASED=UNITS_PURCHASED-? WHERE PROD_ID=?',(int(count_var.get()),int(count_var.get()),selected_bill_product[0]))
        conn.commit()
        conn.close()
        for i in bill_products:
            if selected_bill_product[0] in i:
                bill_products.remove(i)
        bill_listbox.delete(0,tk.END)
        for product in bill_products:
            bill_listbox.insert(tk.END,product)
        conn=sqlite3.connect(database_name)
        cur=conn.cursor()
        cur.execute('SELECT GST_RATE FROM INVENTORY WHERE PROD_ID=?',(selected_bill_product[0],))
        prod_record=cur.fetchall()[0]
        gst_rate=prod_record[0]
        conn.close()
        del_cost=float(selected_bill_product[4])
        del_count=int(selected_bill_product[6])
        total_bill_cost-=round(float(del_count*del_cost),1)
        total_bill_gst-=round(float(gst_rate/100*del_cost*del_count),1)
        total_bill_discount=round(total_bill_cost*disc_rate/100,1)
        total_bill_gtotal=round(total_bill_cost+total_bill_gst-total_bill_discount,1)
        calculated_bill_total_label.configure(text='Rs. '+ str(total_bill_cost))
        calculated_bill_gst_label.configure(text='Rs. '+ str(total_bill_gst))
        calculated_bill_discount_label.configure(text='Rs. '+ str(total_bill_discount))
        calculated_bill_gtotal_label.configure(text='Rs. '+ str(total_bill_gtotal))
    
    #this function generates the bill.
    def generate_command():
        global current_cashier_user , selected_customer_by_cashier , bill_products , total_bill_cost,total_bill_gst,total_bill_discount,total_bill_gtotal
        date_data=dt.datetime.now()
        date=''
        time=''
        date_list=[date_data.day,date_data.month]
        time_list=[date_data.hour,date_data.minute,date_data.second]
        for i in date_list:
            if i<10:
                date+='0'+str(i)+'-'
            else:
                date+=str(i)+'-'
        date+=str(date_data.year)
        c=0
        for j in time_list:
            if j<10 and c<2:
                time+='0'+str(j)+':'
            elif j<10 and c==2:
                time+='0'+str(j)
            elif j>10 and c<2:
                time+=str(j)+':'
            elif j>10 and c==2:
                time+=str(j)
            c+=1
        conn=sqlite3.connect(database_name)
        cur=conn.cursor()
        cur.execute('SELECT NAME FROM EMPLOYEE WHERE EMP_ID=?',(current_cashier_user,))
        cashier_name=cur.fetchall()[0][0]
        conn.close()
        generated_billname='generated_bills\\'+current_cashier_user+'_'+selected_customer_by_cashier[0]+'_'+'bill.txt'
        f=open(generated_billname,'w')
        headerborder='+'+10*'-'+'+'+30*'-'+'+'+10*'-'+'+'+5*'-'+'+'+10*'-'+'+'+10*'-'+'+'+8*'-'+'+'
        l_prod_id=10
        l_prod_name=30
        l_unit_cost=10
        l_qty=5
        l_unit=10
        l_total=10
        l_gst=8
        billtext='''
BILL
Date: %s
Time: %s
Cashier ID: %s
Cashier Name: %s
Customer ID: %s
Customer Name: %s
Customer Phone Number: %s
\n'''%(date,time,current_cashier_user,cashier_name,selected_customer_by_cashier[0],selected_customer_by_cashier[1],selected_customer_by_cashier[2])
        f.write(billtext)
        f.close()
        f=open(generated_billname,'a')
        header_prod_id=bill_products[0][0]
        header_prod_name=bill_products[0][2]
        header_unit_cost=bill_products[0][4]
        header_qty=bill_products[0][6]
        header_unit='Unit'
        header_total=bill_products[0][8]
        header_gst=bill_products[0][10]
        headertext='|'+header_prod_id+' '*(l_prod_id-len(header_prod_id))+'|'+header_prod_name+' '*(l_prod_name-len(header_prod_name))+'|'+header_unit_cost+' '*(l_unit_cost-len(header_unit_cost))+'|'+header_qty+' '*(l_qty-len(header_qty))+'|'+header_unit+' '*(l_unit-len(header_unit))+'|'+header_total+' '*(l_total-len(header_total))+'|'+header_gst+' '*(l_gst-len(header_gst))+'|'+'\n'
        f.write(headerborder+'\n')
        f.write(headertext)
        f.write(headerborder+'\n')
        for i in bill_products[1:]:
            prod_id=i[0]
            conn=sqlite3.connect(database_name)
            cur=conn.cursor()
            cur.execute('SELECT UNIT_OF_MEASUREMENT FROM INVENTORY WHERE PROD_ID=?',(prod_id,))
            unit=cur.fetchall()[0][0]
            conn.close()
            prod_name=i[2]
            unit_cost=i[4]
            qty=i[6]
            total=i[8]
            gst=i[10]
            tabletext='|'+prod_id+' '*(l_prod_id-len(prod_id))+'|'+prod_name+' '*(l_prod_name-len(prod_name))+'|'+unit_cost+' '*(l_unit_cost-len(unit_cost))+'|'+qty+' '*(l_qty-len(qty))+'|'+unit+' '*(l_unit-len(unit))+'|'+total+' '*(l_total-len(total))+'|'+gst+' '*(l_gst-len(gst))+'|'+'\n'
            f.write(tabletext)
        f.write(headerborder)
        f.write('\n')
        calculationtext='''
Total: Rs. %s
GST: Rs. %s
Discount: Rs. %s
Grand Total: Rs. %s'''%(total_bill_cost,total_bill_gst,total_bill_discount,total_bill_gtotal)
        f.write(calculationtext)
        f.close()
        month=date[3:5]
        conn=sqlite3.connect(database_name)
        cur=conn.cursor()
        if month=='01':
            cur.execute('UPDATE SALES2022 SET JAN_22=JAN_22+? WHERE EMP_ID=?',(total_bill_gtotal,current_cashier_user))
        elif month=='02':
            cur.execute('UPDATE SALES2022 SET FEB_22=FEB_22+? WHERE EMP_ID=?',(total_bill_gtotal,current_cashier_user))
        elif month=='03':
            cur.execute('UPDATE SALES2022 SET MAR_22=MAR_22+? WHERE EMP_ID=?',(total_bill_gtotal,current_cashier_user))
        elif month=='04':
            cur.execute('UPDATE SALES2022 SET APR_22=APR_22+? WHERE EMP_ID=?',(total_bill_gtotal,current_cashier_user))
        elif month=='05':
            cur.execute('UPDATE SALES2022 SET MAY_22=MAY_22+? WHERE EMP_ID=?',(total_bill_gtotal,current_cashier_user))
        elif month=='06':
            cur.execute('UPDATE SALES2022 SET JUN_22=JUN_22+? WHERE EMP_ID=?',(total_bill_gtotal,current_cashier_user))
        elif month=='07':
            cur.execute('UPDATE SALES2022 SET JUL_22=JUL_22+? WHERE EMP_ID=?',(total_bill_gtotal,current_cashier_user))
        elif month=='08':
            cur.execute('UPDATE SALES2022 SET AUG_22=AUG_22+? WHERE EMP_ID=?',(total_bill_gtotal,current_cashier_user))
        elif month=='09':
            cur.execute('UPDATE SALES2022 SET SEP_22=SEP_22+? WHERE EMP_ID=?',(total_bill_gtotal,current_cashier_user))
        elif month=='10':
            cur.execute('UPDATE SALES2022 SET OCT_22=OCT_22+? WHERE EMP_ID=?',(total_bill_gtotal,current_cashier_user))
        elif month=='11':
            cur.execute('UPDATE SALES2022 SET NOV_22=NOV_22+? WHERE EMP_ID=?',(total_bill_gtotal,current_cashier_user))
        elif month=='12':
            cur.execute('UPDATE SALES2022 SET DEC_22=DEC_22+? WHERE EMP_ID=?',(total_bill_gtotal,current_cashier_user))
        conn.commit()
        conn.close()
    date_data=dt.datetime.now()
    date=''
    time=''
    date_list=[date_data.day,date_data.month]
    time_list=[date_data.hour,date_data.minute,date_data.second]
    for i in date_list:
        if i<10:
            date+='0'+str(i)+'-'
        else:
            date+=str(i)+'-'
    date+=str(date_data.year)
    c=0
    for j in time_list:
        if j<10 and c<2:
            time+='0'+str(j)+':'
        elif j<10 and c==2:
            time+='0'+str(j)
        elif j>10 and c<2:
            time+=str(j)+':'
        elif j>10 and c==2:
            time+=str(j)
        c+=1
    global current_cashier_user , selected_customer_by_cashier , bill_products , total_bill_cost,total_bill_gst,total_bill_discount,total_bill_gtotal
    cashier_billing_counter=tk.Tk()
    cashier_billing_counter.title('BILLING COUNTER')
    cashier_billing_counter.iconbitmap(icon_name)
    cashier_billing_counter['background']=window_bg_color
    width=cashier_billing_counter.winfo_screenwidth()-40
    height=cashier_billing_counter.winfo_screenheight()-40
    cashier_billing_counter.geometry('%dx%d'%(width,height))
    headerfont=font.Font(family='Bahnschrift',size=28,weight='bold',underline=1)
    buttonfont=font.Font(family='Bahnschrift',size=18,weight='bold')
    selectionfont=font.Font(family='Bahnschrift',size=12,weight='bold')
    header_label=tk.Label(cashier_billing_counter,text='Billing Counter',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=headerfont)
    header_label.grid(row=0,column=0,padx=7,pady=4,columnspan=6)
    conn=sqlite3.connect(database_name)
    cur=conn.cursor()
    cur.execute('SELECT NAME FROM EMPLOYEE WHERE EMP_ID=?',(current_cashier_user,))
    employee_name=cur.fetchall()[0][0]
    cashier_id_label=tk.Label(cashier_billing_counter,text='Cashier ID: ',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont)
    cashier_id_label.grid(row=1,column=0,padx=7,pady=4)
    displayed_cashier_id_label=tk.Label(cashier_billing_counter,text=current_cashier_user,bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont)
    displayed_cashier_id_label.grid(row=1,column=1,padx=7,pady=4)
    cashier_name_label=tk.Label(cashier_billing_counter,text='Cashier Name: ',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont)
    cashier_name_label.grid(row=2,column=0,padx=7,pady=4)
    displayed_cashier_name_label=tk.Label(cashier_billing_counter,text=employee_name,bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont)
    displayed_cashier_name_label.grid(row=2,column=1,padx=7,pady=4)
    datetime_label=tk.Label(cashier_billing_counter,text='Date\nTime',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont)
    datetime_label.grid(row=3,column=0,padx=7,pady=4)
    displayed_datetime_label=tk.Label(cashier_billing_counter,text=date+'\n'+time,bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont)
    displayed_datetime_label.grid(row=3,column=1,padx=7,pady=4)
    customer_id_label=tk.Label(cashier_billing_counter,text='Customer ID: ',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont)
    customer_id_label.grid(row=4,column=0,padx=7,pady=4)
    displayed_customer_id_label=tk.Label(cashier_billing_counter,text='',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont)
    displayed_customer_id_label.grid(row=4,column=1,padx=7,pady=4)
    customer_name_label=tk.Label(cashier_billing_counter,text='Customer Name: ',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont)
    customer_name_label.grid(row=5,column=0,padx=7,pady=4)
    displayed_customer_name_label=tk.Label(cashier_billing_counter,text='',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont)
    displayed_customer_name_label.grid(row=5,column=1,padx=7,pady=4)
    customer_phone_label=tk.Label(cashier_billing_counter,text='Customer Phone Number: ',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont)
    customer_phone_label.grid(row=6,column=0,padx=7,pady=4)
    displayed_customer_phone_label=tk.Label(cashier_billing_counter,text='',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont)
    displayed_customer_phone_label.grid(row=6,column=1,padx=7,pady=4)
    customer_details_label=tk.Label(cashier_billing_counter,text='Customer Details: ',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont)
    customer_details_label.grid(row=3,column=3,padx=7,pady=4)
    selected_products_label=tk.Label(cashier_billing_counter,text='Selected Products: ',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont)
    selected_products_label.grid(row=1,column=4,padx=7,pady=4,columnspan=2)
    cust_details_listbox=tk.Listbox(cashier_billing_counter,fg=button_fg_color,borderwidth=0,font=selectionfont,height=4,width=20)
    cust_details_listbox.grid(row=4,column=3,padx=7,pady=4,rowspan=3)
    scrollbar1=tk.Scrollbar(cashier_billing_counter)
    scrollbar1.grid(row=4,column=2,pady=4,rowspan=3)
    cust_details_listbox.configure(yscrollcommand=scrollbar1.set)
    scrollbar1.configure(command=cust_details_listbox.yview)
    cust_details_listbox.bind('<<ListboxSelect>>',get_selected_customer)
    conn=sqlite3.connect(database_name)
    cur=conn.cursor()
    cur.execute('SELECT * FROM CUSTOMER')
    customer_details=cur.fetchall()
    conn.close()
    cust_details_listbox.delete(0,tk.END)
    for record in customer_details:
        cust_details_listbox.insert(tk.END,record)
    category_listbox=tk.Listbox(cashier_billing_counter,fg=button_fg_color,borderwidth=0,font=selectionfont,height=3,width=20)
    category_listbox.grid(row=7,column=1,padx=7,pady=4)
    scrollbar2=tk.Scrollbar(cashier_billing_counter)
    scrollbar2.grid(row=7,column=2,padx=7,pady=4)
    category_listbox.configure(yscrollcommand=scrollbar2.set)
    scrollbar2.configure(command=category_listbox.yview)
    category_listbox.bind('<<ListboxSelect>>',get_selected_category)
    conn=sqlite3.connect(database_name)
    cur=conn.cursor()
    cur.execute('SELECT PROD_CATEGORY FROM INVENTORY')
    category_list=cur.fetchall()
    conn.close()
    final_categories=[]
    category_listbox.delete(0,tk.END)
    for i in category_list:
        if i[0] not in final_categories:
            final_categories.append(i[0])
    for category in final_categories:
        category_listbox.insert(tk.END,category)
    product_details_listbox=tk.Listbox(cashier_billing_counter,fg=button_fg_color,borderwidth=0,font=selectionfont,height=5,width=30)
    product_details_listbox.grid(row=8,column=1,padx=7,pady=4)
    scrollbar3=tk.Scrollbar(cashier_billing_counter)
    scrollbar3.grid(row=8,column=2,padx=7,pady=4)
    product_details_listbox.configure(yscrollcommand=scrollbar3.set)
    scrollbar3.configure(command=product_details_listbox.yview)
    scrollbar3n=tk.Scrollbar(cashier_billing_counter,orient=tk.HORIZONTAL)
    scrollbar3n.grid(row=9,column=1)
    product_details_listbox.configure(xscrollcommand=scrollbar3n.set)
    scrollbar3n.configure(command=product_details_listbox.xview)
    product_details_listbox.bind('<<ListboxSelect>>',get_selected_product)
    category_label=tk.Label(cashier_billing_counter,text='Select Category: ',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont)
    category_label.grid(row=7,column=0,padx=7,pady=4)
    selected_category_label=tk.Label(cashier_billing_counter,text='',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont)
    selected_category_label.grid(row=7,column=3,padx=7,pady=4)
    product_label=tk.Label(cashier_billing_counter,text='Select Product: ',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont)
    product_label.grid(row=8,column=0,padx=7,pady=4)
    selected_product_label=tk.Label(cashier_billing_counter,text='',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont)
    selected_product_label.grid(row=8,column=3,padx=7,pady=4)
    count_var=tk.StringVar()
    count_entry=tk.Entry(cashier_billing_counter,textvariable=count_var,font=buttonfont)
    count_entry.grid(row=10,column=1)
    count_label=tk.Label(cashier_billing_counter,text='Enter Count: ',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont)
    count_label.grid(row=10,column=0,padx=7,pady=4)
    add_button=tk.Button(cashier_billing_counter,text='Add Product',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont,command=add_command)
    add_button.grid(row=11,column=0,padx=7,pady=4)
    bill_products=[['PROD_ID','-','PROD_NAME','-','UNIT_COST','-','COUNT','-','TOTAL_COST','-','GST'],]
    bill_listbox=tk.Listbox(cashier_billing_counter,fg=button_fg_color,borderwidth=0,font=selectionfont,height=15,width=50)
    bill_listbox.grid(row=2,column=4,padx=7,pady=4,rowspan=7)
    scrollbar4=tk.Scrollbar(cashier_billing_counter)
    scrollbar4.grid(row=2,column=5,padx=7,pady=4,rowspan=7)
    bill_listbox.configure(yscrollcommand=scrollbar4.set)
    scrollbar4.configure(command=bill_listbox.yview)
    scrollbar4n=tk.Scrollbar(cashier_billing_counter,orient=tk.HORIZONTAL)
    scrollbar4n.grid(row=9,column=4)
    bill_listbox.configure(xscrollcommand=scrollbar4n.set)
    scrollbar4n.configure(command=bill_listbox.xview)
    bill_listbox.bind('<<ListboxSelect>>',get_selected_bill_product)
    delete_button=tk.Button(cashier_billing_counter,text='Delete Selected',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont,command=delete_command)
    delete_button.grid(row=11,column=4,padx=7,pady=4)
    conn=sqlite3.connect(database_name)
    cur=conn.cursor()
    cur.execute('SELECT * FROM RATE')
    disc_rate=cur.fetchall()[0][0]
    conn.close()
    total_bill_cost=0
    total_bill_gst=0
    bill_total_label=tk.Label(cashier_billing_counter,text='Total: ',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont)
    bill_total_label.grid(row=12,column=0,padx=7,pady=4)
    calculated_bill_total_label=tk.Label(cashier_billing_counter,text='',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont)
    calculated_bill_total_label.grid(row=13,column=0,padx=7,pady=4)
    bill_gst_label=tk.Label(cashier_billing_counter,text='GST: ',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont)
    bill_gst_label.grid(row=12,column=1,padx=7,pady=4)
    calculated_bill_gst_label=tk.Label(cashier_billing_counter,text='',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont)
    calculated_bill_gst_label.grid(row=13,column=1,padx=7,pady=4)
    bill_discount_label=tk.Label(cashier_billing_counter,text='Discount: ',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont)
    bill_discount_label.grid(row=12,column=3,padx=7,pady=4)
    calculated_bill_discount_label=tk.Label(cashier_billing_counter,text='',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont)
    calculated_bill_discount_label.grid(row=13,column=3,padx=7,pady=4)
    bill_gtotal_label=tk.Label(cashier_billing_counter,text='Grand Total: ',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont)
    bill_gtotal_label.grid(row=12,column=4,padx=7,pady=4)
    calculated_bill_gtotal_label=tk.Label(cashier_billing_counter,text='',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont)
    calculated_bill_gtotal_label.grid(row=13,column=4,padx=7,pady=4)
    generate_button=tk.Button(cashier_billing_counter,text='Generate Bill',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont,command=lambda: [generate_command(),messagebox.showinfo('Success','Bill was successfully generated!')])
    generate_button.grid(row=14,column=0,padx=7,pady=4)
    back_button=tk.Button(cashier_billing_counter,text='Back',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont,command=lambda: [cashier_billing_counter.destroy(),create_cashier_homepage()])
    back_button.grid(row=14,column=4,padx=7,pady=4)
    cashier_billing_counter.mainloop()
    
#this function creates the view messagtes page.    
def create_cashier_view_message():
    global current_cashier_user,emp_filename
    #this function displays the details of message 1.
    def open_message1():
        global current_cashier_user,foldername
        conn=sqlite3.connect(database_name)
        cur=conn.cursor()
        cur.execute('SELECT MSG1 FROM EMPLOYEE WHERE EMP_ID=?',(current_cashier_user,))
        messagebox_content=cur.fetchone()[0]
        messagebox.showinfo('Message 1',messagebox_content)
        conn.close()
        
    #this function displays the details of message 2.
    def open_message2():
        global current_cashier_user,foldername,database_name
        conn=sqlite3.connect(database_name)
        cur=conn.cursor()
        cur.execute('SELECT MSG2 FROM EMPLOYEE WHERE EMP_ID=?',(current_cashier_user,))
        messagebox_content=cur.fetchone()[0]
        messagebox.showinfo('Message 2',messagebox_content)
        conn.close()
        
    #this function displays the details of message 3.
    def open_message3():
        global current_cashier_user
        conn=sqlite3.connect(database_name)
        cur=conn.cursor()
        cur.execute('SELECT MSG3 FROM EMPLOYEE WHERE EMP_ID=?',(current_cashier_user,))
        messagebox_content=cur.fetchone()[0]
        messagebox.showinfo('Message 3',messagebox_content)
        conn.close()
    
    #this function displays the details of message 4.
    def open_message4():
        global current_cashier_user
        conn=sqlite3.connect(database_name)
        cur=conn.cursor()
        cur.execute('SELECT MSG4 FROM EMPLOYEE WHERE EMP_ID=?',(current_cashier_user,))
        messagebox_content=cur.fetchone()[0]
        messagebox.showinfo('Message 4',messagebox_content)
        conn.close()
    
    #this function displays the details of message 5.
    def open_message5():
        global current_cashier_user
        conn=sqlite3.connect(database_name)
        cur=conn.cursor()
        cur.execute('SELECT MSG5 FROM EMPLOYEE WHERE EMP_ID=?',(current_cashier_user,))
        messagebox_content=cur.fetchone()[0]
        messagebox.showinfo('Message 5',messagebox_content)
        conn.close()
    
    #this function displays the details of attachment 1.
    def open_attachment1():
        global current_cashier_user
        conn=sqlite3.connect(database_name)
        cur=conn.cursor()
        cur.execute('SELECT ATC1 FROM EMPLOYEE WHERE EMP_ID=?',(current_cashier_user,))
        filename=emp_filename+cur.fetchone()[0]
        conn.close()
        buttonfont=font.Font(family='Bahnschrift',size=30,weight='bold')
        f=open(filename)
        file_contents=f.read()
        cashier_view_message.destroy()
        attachment1_window=tk.Tk()
        attachment1_window.title('Attachment1')
        display_contents=tk.Text(attachment1_window,font=buttonfont)
        display_contents.grid(row=0,column=0)
        display_contents.delete(tk.END)
        display_contents.insert(tk.END,file_contents)
        attachment1_window.mainloop()
    
    #this function displays the details of attachment 2.
    def open_attachment2():
        global current_cashier_user
        conn=sqlite3.connect(database_name)
        cur=conn.cursor()
        cur.execute('SELECT ATC2 FROM EMPLOYEE WHERE EMP_ID=?',(current_cashier_user,))
        filename=emp_filename+cur.fetchone()[0]
        conn.close()
        buttonfont=font.Font(family='Bahnschrift',size=30,weight='bold')
        f=open(filename)
        file_contents=f.read()
        cashier_view_message.destroy()
        attachment2_window=tk.Tk()
        attachment2_window.title('Attachment2')
        display_contents=tk.Text(attachment2_window,font=buttonfont)
        display_contents.grid(row=0,column=0)
        display_contents.delete(tk.END)
        display_contents.insert(tk.END,file_contents)
        attachment2_window.mainloop()
    
    #this function displays the details of attachment 3.
    def open_attachment3():
        global current_cashier_user
        conn=sqlite3.connect(database_name)
        cur=conn.cursor()
        cur.execute('SELECT ATC3 FROM EMPLOYEE WHERE EMP_ID=?',(current_cashier_user,))
        filename=emp_filename+cur.fetchone()[0]
        conn.close()
        buttonfont=font.Font(family='Bahnschrift',size=30,weight='bold')
        f=open(filename)
        file_contents=f.read()
        cashier_view_message.destroy()
        attachment3_window=tk.Tk()
        attachment3_window.title('Attachment1')
        display_contents=tk.Text(attachment3_window,font=buttonfont)
        display_contents.grid(row=0,column=0)
        display_contents.delete(tk.END)
        display_contents.insert(tk.END,file_contents)
        attachment3_window.mainloop()
    
    #this function displays the details of attachment 4.
    def open_attachment4():
        global current_cashier_user
        conn=sqlite3.connect(database_name)
        cur=conn.cursor()
        cur.execute('SELECT ATC4 FROM EMPLOYEE WHERE EMP_ID=?',(current_cashier_user,))
        filename=emp_filename+cur.fetchone()[0]
        conn.close()
        buttonfont=font.Font(family='Bahnschrift',size=30,weight='bold')
        f=open(filename)
        file_contents=f.read()
        cashier_view_message.destroy()
        attachment4_window=tk.Tk()
        attachment4_window.title('Attachment4')
        display_contents=tk.Text(attachment4_window,font=buttonfont)
        display_contents.grid(row=0,column=0)
        display_contents.delete(tk.END)
        display_contents.insert(tk.END,file_contents)
        attachment4_window.mainloop()
    
    #this function displays the details of attachment 5.
    def open_attachment5():
        global current_cashier_user
        conn=sqlite3.connect(database_name)
        cur=conn.cursor()
        cur.execute('SELECT ATC5 FROM EMPLOYEE WHERE EMP_ID=?',(current_cashier_user,))
        filename=emp_filename+cur.fetchone()[0]
        conn.close()
        buttonfont=font.Font(family='Bahnschrift',size=30,weight='bold')
        f=open(filename)
        file_contents=f.read()
        cashier_view_message.destroy()
        attachment5_window=tk.Tk()
        attachment5_window.title('Attachment5')
        display_contents=tk.Text(attachment5_window,font=buttonfont)
        display_contents.grid(row=0,column=0)
        display_contents.delete(tk.END)
        display_contents.insert(tk.END,file_contents)
        attachment5_window.mainloop()
        
    cashier_view_message=tk.Tk()
    cashier_view_message.title('VIEW MESSAGES')
    cashier_view_message.iconbitmap(icon_name)
    cashier_view_message['background']=window_bg_color
    width=cashier_view_message.winfo_screenwidth()-40
    height=cashier_view_message.winfo_screenheight()-40
    cashier_view_message.geometry('%dx%d'%(width,height))
    buttonfont=font.Font(family='Bahnschrift',size=30,weight='bold')
    labelfont=font.Font(family='Bahnschrift',size=40,weight='bold',underline=1)
    selected_file_label=tk.Label(cashier_view_message,text='VIEW MESSAGES',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=labelfont)
    selected_file_label.grid(row=0,column=0,padx=15,pady=10,columnspan=3)
    box1_label=tk.Label(cashier_view_message,text='BOX 1',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont)
    box1_label.grid(row=1,column=0,padx=15,pady=10)
    box2_label=tk.Label(cashier_view_message,text='BOX 2',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont)
    box2_label.grid(row=2,column=0,padx=15,pady=10)
    box3_label=tk.Label(cashier_view_message,text='BOX 3',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont)
    box3_label.grid(row=3,column=0,padx=15,pady=10)
    box4_label=tk.Label(cashier_view_message,text='BOX 4',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont)
    box4_label.grid(row=4,column=0,padx=15,pady=10)
    box5_label=tk.Label(cashier_view_message,text='BOX 5',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont)
    box5_label.grid(row=5,column=0,padx=15,pady=10)
    box1_msg_button=tk.Button(cashier_view_message,text='Open Message',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont,command=open_message1)
    box1_msg_button.grid(row=1,column=1,padx=15,pady=10)
    box2_msg_button=tk.Button(cashier_view_message,text='Open Message',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont,command=open_message2)
    box2_msg_button.grid(row=2,column=1,padx=15,pady=10)
    box3_msg_button=tk.Button(cashier_view_message,text='Open Message',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont,command=open_message3)
    box3_msg_button.grid(row=3,column=1,padx=15,pady=10)
    box4_msg_button=tk.Button(cashier_view_message,text='Open Message',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont,command=open_message4)
    box4_msg_button.grid(row=4,column=1,padx=15,pady=10)
    box5_msg_button=tk.Button(cashier_view_message,text='Open Message',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont,command=open_message5)
    box5_msg_button.grid(row=5,column=1,padx=15,pady=10)
    box1_atc_button=tk.Button(cashier_view_message,text='Open Attachment',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont,command=open_attachment1)
    box1_atc_button.grid(row=1,column=2,padx=15,pady=10)
    box2_atc_button=tk.Button(cashier_view_message,text='Open Attachment',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont,command=open_attachment2)
    box2_atc_button.grid(row=2,column=2,padx=15,pady=10)
    box3_atc_button=tk.Button(cashier_view_message,text='Open Attachment',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont,command=open_attachment3)
    box3_atc_button.grid(row=3,column=2,padx=15,pady=10)
    box4_atc_button=tk.Button(cashier_view_message,text='Open Attachment',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont,command=open_attachment4)
    box4_atc_button.grid(row=4,column=2,padx=15,pady=10)
    box5_atc_button=tk.Button(cashier_view_message,text='Open Attachment',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont,command=open_attachment5)
    box5_atc_button.grid(row=5,column=2,padx=15,pady=10)
    back_button=tk.Button(cashier_view_message,text='Back',bg=button_bg_color,fg=button_fg_color,borderwidth=0,font=buttonfont,command=lambda: [cashier_view_message.destroy(),create_cashier_homepage()])
    back_button.grid(row=6,column=1)
    cashier_view_message.mainloop()

create_main_login_window()


