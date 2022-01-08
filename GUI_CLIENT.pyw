import socket
import threading
from tkinter import *
from tkinter import Listbox
from tkinter import messagebox

win=Tk()
win.geometry('800x530')
win.title("Let's Chat")
win.resizable(False, False)
win.config(bg='black')

frame=Frame(win,bg='red')
my_scrollbar=Scrollbar(frame,orient=VERTICAL)

list_box=Listbox(frame,width=67,height=15,activestyle='none',yscrollcommand=my_scrollbar.set,bg="black",fg="white",font=('Ariel','15','bold'),selectbackground='green')
my_scrollbar.config(command=list_box.yview)
my_scrollbar.pack(side=RIGHT,fill=Y)
frame.place(x=20,y=70)
list_box.pack()

l1=Label(win,text='Client Name:',bg='black',fg='white',font=('Helvetica','20','bold'))
l1.place(x=30,y=16)

namebox=Entry(win,font=('Ariel','20','bold'),width=20,fg='black')
namebox.pack(pady=15)

btn=Button(win,text='Connect',bg='white',fg='black',font=('Ariel','14','bold'),command=lambda:connect(namebox.get()))
btn.place(x=600,y=15)

l2=Label(win,text='Type your message here...',bg='black',fg='white',font=('Ariel','12','bold'))
l2.place(x=20,y=453)

textbox=Entry(win,font=('Ariel','20','bold'),width=50,fg='black')
textbox.config(state='disabled')
textbox.place(x=20,y=480)

textbox.bind('<Return>',(lambda event:client_send(textbox.get())))

def connect(alias):
    global name
    global client
    name=alias
    host='13.67.186.135'
    port=9999
    if len(name)<1:
        messagebox.showerror(title="ERROR!!!", message="You must enter client name <e.g. John>")
    else:
        client=socket.socket()
        client.connect((host,port))
        client.send(name.encode('utf-8'))
        btn.config(state=DISABLED)
        textbox.config(state='normal')
        threading.Thread(target=client_receive).start()

def client_receive():
    global name
    global client
    while True:
        try:
            message=client.recv(1024).decode('utf-8')
            list_box.insert(END,message)
            list_box.see(END)
        except:
            list_box.insert(END,'Some error occur!')
            list_box.see(END)
            client.close()
            break

def client_send(msg):
    global name
    global client
    message = name+'> '+msg
    textbox.delete(0,END)
    client.send(message.encode('utf-8'))

win.mainloop()