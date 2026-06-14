import os

#check day 9 directory is already exists
dirname="log"

os.makedirs(dirname, exist_ok=True)    
#os.removedirs(dirname)
cwd=os.getcwd()

file_path=os.path.join(cwd,dirname,"app.log")
file=open(file_path,"w")
file.write("This is log file")

print(os.getpid())

print(os.listdir("d:/"))
file_path=os.path.join("d:/","LLM","WWWWWWWWWWW.txt")
#file=open(file_path,"w")
#file.write("This is dummy file")
print(os.path.exists(file_path))
print(os.name)