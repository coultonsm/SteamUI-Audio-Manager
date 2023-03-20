#Written by coulton64
import os
import shutil
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from tkinter import INSERT
import json

def trymovefiles(steamuidir,pathList,dirList,sel):
  #keep old files
  os.chdir(steamuidir)
  try: os.makedirs('old')
  except: 
    shutil.rmtree('old')
    os.makedirs('old')
  print('Moving old files')
  for file in os.scandir(steamuidir):
    if file.is_file():
      if file.name.endswith('.wav') or file.name.endswith('.m4a'):
        try:
          shutil.move(f'{os.getcwd()}/{file.name}', 'old')
        except:
          messagebox.showerror("Error",'Could not successfully move files. Are you running as administrator?')
          break
  #move new files
  os.chdir(pathList[sel])
  files={}
  filePath={}
  fileEntry=1
  errorCount=0
  print('Moving new files')
  for i in os.scandir(pathList[sel]):
    if i.is_file():
      files[fileEntry]=i.name
      filePath[fileEntry]=os.path.abspath(i)
      try:
        shutil.copy(filePath[fileEntry],f'{steamuidir}/')
        fileEntry=+1
      except:
        messagebox.showerror("Error", f'Could not move file: {files[fileEntry]} {filePath[fileEntry]}')
  messagebox.showinfo("Complete", f'operation has completed. Errors:{errorCount}')

def selected_item(listbox):
    # Traverse the tuple returned by
    # curselection method and print
    # corresponding value(s) in the listbox
    for i in listbox.curselection():
      res = listbox.get(i)
    return res[0]

def folderDialog():
  return filedialog.askdirectory(title="Select SteamUI folder")
def folderDialogButton(sdTB):
  a=filedialog.askdirectory(title="Select SteamUI folder")
  sdTB.insert(INSERT,a)


window = tk.Tk()
window.title("SteamUI Sound Manager")
window.geometry("400x400")

##Check packs
try:
  f = open("config.json")
  data=json.load(f)
  steamuidir = data["steamui_path"]
except:
  messagebox.showinfo("first run", "Please select steamUI folder.")
  doutput={"steamui_path": f'{folderDialog()}'}
  json_ob=json.dumps(doutput,indent=4)
  with open("config.json","w") as outfile:
    outfile.write(json_ob)
  steamuidir = doutput["steamui_path"]

sdTB = tk.Text(window, height=1)
if steamuidir != '': sdTB.insert(INSERT,steamuidir)
sdTB.pack()

sdtbButton=tk.Button(text="Browse",command=lambda: folderDialogButton(sdTB))
sdtbButton.pack()

rootdir='Packs'
dirList={}
direntry=0
pathList={}
os.chdir(steamuidir)
try:
    for it in os.scandir(rootdir):
        if it.is_dir():
            dirList[direntry]=it.name
            pathList[direntry]=os.path.abspath(it)
            direntry+=1
except:
    messagebox.showinfo("Missing folder", "Missing packs folder. Creating one now. Please restart afterward")
    os.makedirs("Packs")
dirListTuple = [(k, v) for k, v in dirList.items()]
var = tk.Variable(value=dirListTuple)
listbox = tk.Listbox(
  window,
  listvariable=var,
  height=6
)
listbox.pack()
# button = tk.Button(text="Check", command=lambda:print(selected_item(listbox)))
# button.pack()
installButton=tk.Button(text="Install",command=lambda:trymovefiles(steamuidir,pathList,dirList,selected_item(listbox)))
installButton.pack()

tk.mainloop()