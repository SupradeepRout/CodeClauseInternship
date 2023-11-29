from tkinter import *
from tkinter import messagebox,filedialog
import os
import speech_recognition as sr
#import pyttsx3
from pygame import mixer
from email.message import EmailMessage
import smtplib
import imghdr
import pandas 
check=False
##########################################################################
def speak():     # this function is associated with the speak button
    mixer.init()
    mixer.music.load('Tkinter//image//music.mp3')
    mixer.music.play()
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        try:
           recognizer.adjust_for_ambient_noise(source,duration=1)
           audio = recognizer.listen(source)
           text = recognizer.recognize_google(audio)
           text_area.insert(END,text+'.')
        except:
           pass
####################################################################################
def exit(): # this function is attached with the exit button 
    result=messagebox.askyesno("notification",'Do you want to exit ?')
    if result:
        root.destroy()  # it close the popup window
    else:
        pass
######################################################################################
def clear():   # this fn is associated with the erase button 
    mail_entryfill.delete(0,END)
    sub_entryfill.delete(0,END)
    text_area.delete(1.0,END)
#####################################################################################
def send():                # it is associated with send button ,here we check all entry are fill or not , then call the "send_email()" fn 
    
     if(mail_entryfill.get()=='' or sub_entryfill.get()=='' or text_area.get(1.0,END)=='\n'):
            messagebox.showerror('Error !!!','Enpty field not allow !',parent=root)

     else:
        if(choice.get()=='single'):
           result= send_email(mail_entryfill.get(),sub_entryfill.get(),text_area.get(1.0,END))  # here we call the send_mail()  function
           if(result=='sent'):
                messagebox.showinfo('Information','Email is sent successfully ✓✓',parent=root)
           if(result=='failed'):
                messagebox.showerror('Error','Email is not sent successfully ✕ ✕ ✕',parent=root)


        if(choice.get()=='multiple'):
            sent=0
            failed=0
            for x in final_emails:
               result= send_email(x,sub_entryfill.get(),text_area.get(1.0,END))
               if(result=='sent'):
                   sent+=1
               if(result=='failed'):
                   failed+=1

               total_label.config(text='')
               sent_label.config(text=' Sent: '+ str(sent))
               left_label.config(text=' Left: '+str((len(final_emails)-(sent+failed))))
               faild_label.config(text=' Faild: '+str(failed))

               total_label.update()
               sent_label.update()
               left_label.update()
               faild_label.update()

            messagebox.showinfo('Information','Email is sent successfully ✓✓',parent=root)

#######################################################################################
def send_email(address,sub,body):   # it is associated with the 'def attach ()' function 
    file=open('gmail.txt','r')
    for i in file:
        info=i.split('-')
    print('info',info)
    message=EmailMessage()
    message['to']=address
    message['subject']=sub
    message['from']=info[0]
    message.set_content(body)
    if (check):
        if(file_type=='png' or file_type=='jpg' or file_type=='jpeg'):
            f=open(file_path,'rb')
            file_data=f.read()
            sub_type=imghdr.what(file_path)
            message.add_attachment(file_data,maintype='image',subtype=sub_type,filename=file_name)
        else:
            f=open(file_path,'rb')
            file_data=f.read()
            message.add_attachment(file_data,maintype='application',subtype='octet-stream',filename=file_name)
    
    s=smtplib.SMTP('smtp.gmail.com',587)
    s.starttls()    # secure the connectivity between clint and server 
    s.login(info[0],info[1])
    s.send_message(message)
    x=s.ehlo()
    if x[0]==250:
        return "sent"
    else:
        return "failed"
    
    # messagebox.showinfo('Information','Email is sent successfully ✓✓',parent=root)
###################################################################################
def attach():
    global file_name,file_type,file_path,check
    check=True
    file_path=filedialog.askopenfilename(title='Select file')
    if file_path:
        file_name=os.path.basename(file_path)      # it only take the file name as path not the hole path
        text_area.insert(END,f'\n{file_name}\n')   # it insert the file name inside the text area 
        file_list=file_path.split('.')             # it split the file path and the file type with respect to '.' operator
        file_type=file_list[1]
        print(f'type={file_type}')
######################################################################################
def radio_button_check():
    if choice.get()=='single':
        browse_Button.config(state=DISABLED)
        mail_entryfill.config(state=NORMAL)
    if choice.get()=='multiple':
        browse_Button.config(state=NORMAL)
        mail_entryfill.config(state='readonly')
#######################################################################################
def browse():             # this function is assoiated with the browse button 
    global final_emails
    path=filedialog.askopenfilename(title='Select Excel file ')
    if not path:
        messagebox.showerror('Error','please select the Excel file'+ '\n' +'that contain the Email address',parent=root)
    else:
        data=pandas.read_excel(path)
        if 'Email' in data.columns:
            emails=list(data['Email'])
            final_emails=[]
            for i in emails:
             if pandas.isnull(i)==False:
                 final_emails.append(i)
            print(f'email={final_emails}')
        if(len(final_emails)==0):
            messagebox.showerror('Error',"File doesn't contain Email address !!!!")
        else:
            mail_entryfill.config(state='normal')
            mail_entryfill.insert(0,os.path.basename(path))
            mail_entryfill.config(state='readonly') 
            total_label.config(text=f'Total: {len(final_emails)} .')
            sent_label.config(text=' Sent: ')
            left_label.config(text=' Left: ')
            faild_label.config(text=' Faild: ')


########################################################################################
def setting():   # this fn is associated with setting button
    def clear1():
        mail1_entryfill.delete(0,END)
        pass_entryfill.delete(0,END)
    #####################################
    def save():
        if(mail1_entryfill.get()=='' or pass_entryfill.get()==''):
            messagebox.showerror('Error !!!','Enpty field not allow !',parent=root1)
        else:
            file=open('gmail.txt','w')
            file.write(mail1_entryfill.get()+'-'+pass_entryfill.get())
            file.close()
            messagebox.showinfo('Information','Saved successfully',parent=root1)
            root1.destroy()

    root1=Toplevel()
    root1.title("Settings")
    root1.geometry('500x300+300+90')
    root1.config(bg='antiquewhite')
    ###############################################################################################


    title_Lable=Label(root1,text="Credential Setting",image=logo,compound=LEFT,font=('Goudy Old Style',28,'bold'),bg='white',fg='dodger blue2',padx=10)
    title_Lable.grid(row=0,column=0,padx=60)

    From_lable_frame=LabelFrame(root1,text='From(Email Address)',font=('times new roman',16,'bold'),bd=2,fg='black',bg='antiquewhite')
    From_lable_frame.grid(row=1,column=0,pady=5,padx=30)

    mail1_entryfill=Entry(From_lable_frame,font=('times new roman',18,),width=30)
    mail1_entryfill.grid(row=0,column=0,padx=5,pady=2 )

    pass_lable_frame=LabelFrame(root1,text='password',font=('times new roman',16,'bold'),bd=2,fg='black',bg='antiquewhite')
    pass_lable_frame.grid(row=2,column=0,pady=5,padx=30)

    pass_entryfill=Entry(pass_lable_frame,font=('times new roman',18,),width=20,show="*")
    pass_entryfill.grid(row=0,column=0,padx=5,pady=2 )

    save_Button=Button(root1,bd=1,text=' save ',font=('times new roman',15,'bold'),bg='gold2',fg='black',activebackground='gold2',cursor='hand2',command=save)
    save_Button.place(x=100,y=240) 

    change_Button=Button(root1,bd=1,text="change",font=('times new roman',15,'bold'),bg='gold2',fg='black',activebackground='gold2',cursor='hand2',command=clear1)
    change_Button.place(x=300,y=240) 

    f=open('gmail.txt','r')
    for i  in f:
        a,b =i.split('-')
        mail1_entryfill.insert(0,a)
        pass_entryfill.insert(0,b)
    
    #if(mail1_entryfill.get() and pass_entryfill.get()):
    #    save_Button.config(state='disabled')
    #else:
    #    save_Button.config(state='active')    
    root1.mainloop()

########################################################################################
root = Tk()
root.title("My Email Sender App")
root.geometry("780x620+50+100")
root.resizable(0,0)  # it not allow us to resize the winow
root.config(bg='antiquewhite')
####################################################################################################
title_Frame=Frame(root,bg='antiquewhite')
title_Frame.grid(row=0,column=0,padx=150,pady=5)

logo=PhotoImage(file='Tkinter//image//mail1.png')
title_Lable=Label(title_Frame,text="  Email Sender",image=logo,compound=LEFT,font=('Goudy Old Style',28,'bold'),bg='white',fg='dodger blue2',padx=10)
title_Lable.grid(row=0,column=0)

logo2=PhotoImage(file='Tkinter//image//set3 (1).png')
settings_Button=Button(title_Frame,image=logo2,bd=0,bg='white',activebackground='white',cursor='hand2',padx=20,command=setting)
settings_Button.grid(row=0,column=1)

###########################################################################################

chose_frame=Frame(root,bg='antiquewhite')
chose_frame.grid(row=1,column=0)

choice=StringVar()
choice.set('single')
single_radio_button=Radiobutton(chose_frame,text='Single',font=('times new roman',20,'bold',),variable=choice,value='single',bg='antiquewhite',activebackground='antiquewhite',command=radio_button_check)
single_radio_button.grid(row=0,column=0,padx=30)

multiple_radio_button2=Radiobutton(chose_frame,text='Multiple',font=('times new roman',20,'bold',),variable=choice,value='multiple',bg='antiquewhite',activebackground='antiquewhite',command=radio_button_check)
multiple_radio_button2.grid(row=0,column=1,padx=30)

################################################################################################
lable_frame1=LabelFrame(root,text='To(Email Address)',font=('times new roman',16,'bold'),bd=2,fg='black',bg='antiquewhite')
lable_frame1.grid(row=2,column=0,pady=5,padx=60)

mail_entryfill=Entry(lable_frame1,font=('times new roman',18,'bold'),width=40)
mail_entryfill.grid(row=0,column=0,padx=5)

logo3=PhotoImage(file='Tkinter//image//browse (2).png')
browse_Button = Button(lable_frame1,image=logo3,compound=LEFT,text='Browse',font=('arial',12,'bold'),bd=0,bg='antiquewhite',activebackground='antiquewhite',cursor='hand2',command=browse)
browse_Button.grid(row=0,column=1,padx=10)
browse_Button.config(state=DISABLED)

##############################################################################################################################
lable_frame2=LabelFrame(root,text='Subject',font=('times new roman',16,'bold'),bd=2,fg='black',bg='antiquewhite')
lable_frame2.grid(row=3,column=0,pady=10,padx=60)

sub_entryfill=Entry(lable_frame2,font=('times new roman',18,'bold'),width=40)
sub_entryfill.grid(row=0,column=0,padx=10,pady=5)

#######################################################################################################33

lable_frame3=LabelFrame(root,text='Compose Email',font=('times new roman',16,'bold'),bd=2,fg='black',bg='antiquewhite')
lable_frame3.grid(row=4,column=0,pady=5,padx=10)

logo_mic=PhotoImage(file='Tkinter//image//mic (2).png')
mic_Button=Button(lable_frame3,image=logo_mic,compound=LEFT,text='speek',font=('arial',12,'bold'),bd=0,bg='antiquewhite',activebackground='antiquewhite',cursor='hand2',command=speak)
mic_Button.grid(row=0,column=0,padx=0)

logo_attach=PhotoImage(file='Tkinter//image//attachment (2).png')
attach_Button=Button(lable_frame3,image=logo_attach,compound=LEFT,text='attachment',font=('arial',12,'bold'),bd=0,bg='antiquewhite',activebackground='antiquewhite',cursor='hand2',command=attach)
attach_Button.grid(row=0,column=1,padx=0)

text_area=Text(lable_frame3,font=('times new roman',14),bd=0,height=8,width=80)
text_area.grid(row=1,column=0,columnspan=2,padx=5,pady=5)

###################################################################################################################

logo_send=PhotoImage(file='Tkinter//image//send.png')
send_Button=Button(root,image=logo_send,bd=0,bg='antiquewhite',activebackground='antiquewhite',cursor='hand2',command=send)
send_Button.place(x=520,y=570)

logo_erase=PhotoImage(file='Tkinter//image//erase.png')
erase_Button=Button(root,image=logo_erase,bd=0,bg='antiquewhite',activebackground='antiquewhite',cursor='hand2',command=clear)
erase_Button.place(x=600,y=570)

logo_exit=PhotoImage(file='Tkinter//image//exit.png')
exit_Button=Button(root,image=logo_exit,bd=0,bg='antiquewhite',activebackground='antiquewhite',cursor='hand2',command=exit)
exit_Button.place(x=690,y=570) 

#############################################################################################################

total_label=Label(root,text='',font=('times new roman',18,'bold'),bg='antiquewhite',fg='red')
total_label.place(x=10,y=560)

sent_label=Label(root,text='',font=('times new roman',18,'bold'),bg='antiquewhite',fg='red')
sent_label.place(x=100,y=560)

faild_label=Label(root,text='',font=('times new roman',18,'bold'),bg='antiquewhite',fg='red')
faild_label.place(x=190,y=560)

left_label=Label(root,text='',font=('times new roman',18,'bold'),bg='antiquewhite',fg='red')
left_label.place(x=280,y=560)

###################################################################
root.mainloop()