import os
import shutil
from collections import defaultdict
import time
import datetime

dirs = 'audio video images docs pdfs spreadsheets executables compressed others'.split()
directories = []
audiolist = tuple('.wav .mp3 .wma .ogg'.split())
videolist = tuple('.avi .wmv .mov .mp4 .flv .ogv .mkv .rmvb .mpg .mpeg .m2v .3gp'.split())
imageslist = tuple('.jpg .jpeg .img .gif .tif .tiff .bmp .png'.split())
docslist = tuple('.doc .docx .rtf .txt'.split())
pdfslist = tuple(['.pdf'])
spreadsheetslist = tuple('.xlsx .xls .xlx .xlsm .xltx .xltm'.split())
executables = tuple(['.exe'])
compressed = tuple('.zip .rar .tar .7z .jar .cab .tgz .tar.gz .zipx'.split())
typelist = [audiolist,videolist,imageslist,docslist,pdfslist,spreadsheetslist,executables,compressed]
#CUSTOMIZE THE DIRECTORY BELOW FOR EACH PERSON
os.chdir('D:\\Downloads')

#Create the necessary folders.
for dname in dirs:
    dnameroot = dname
    n=1
    #check if path exists and is a directory, create if false.
    while True:
        if os.path.exists(os.path.join(os.getcwd(),dname)):
            if os.path.isdir(os.path.join(os.getcwd(),dname)):
                directories.append(dname)
                break
            else:
                dname = dnameroot+f' ({n})'
                n+=1
                continue
        else:
            os.mkdir(os.path.join(os.getcwd(),dname))
            directories.append(dname)
            break
#Define the Others folder.            
distdict= defaultdict((lambda : directories[-1]),{tuple(i):j for i,j in list(zip(typelist,directories))})

    
def organizer():

    """
    Checks new files every second and move them to their corresponding directory/ies, all 
    transfers are recorded in a dedicated sheet. Excluding shortcuts, folders and the sheet of transfer records.
    """
    
    #Sort the files and move them by category.
    for f in os.listdir():
        fname = os.path.splitext(f)[0]
        extension = os.path.splitext(f)[-1].lower()
        found=False
        if (extension != '') & (extension != '.lnk') & (fname != 'transfer_log'):
            for i in typelist:
                if extension in i:
                    newpath = os.path.join(os.getcwd(),distdict[i])
                    #Check for name duplication in the new path.
                    c=0
                    while True:
                        if f in os.listdir(newpath):
                            c+=1
                            suf = f' ({c})'
                            f = fname+suf+extension
                            continue
                        else:
                            shutil.move(os.path.join(os.getcwd(),fname+extension),os.path.join(newpath,f))
                            timetag = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                            with open('transfer_log.txt',mode='a',encoding='utf-16') as log:
                                log.write(f'[{timetag}]: transferred "{fname+extension}" from "{os.getcwd()}" to "{os.path.join(newpath,f)}"\n')

                            break
                    found = not found
                    break
            if found:
                continue
            else:
                #check for name duplication in the new path.
                c=0
                while True:
                    if f in os.listdir(os.path.join(os.getcwd(),distdict[f])):
                        c+=1
                        suf = f' ({c})'
                        f = fname+suf+extension
                        continue
                    else:
                        shutil.move(os.path.join(os.getcwd(),fname+extension),os.path.join(os.path.join(os.getcwd(),distdict[f]),f))
                        timetag = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                        with open('transfer_log.txt',mode='a',encoding='utf-16') as log:
                            log.write(f'[{timetag}]: transferred "{fname+extension}" from "{os.getcwd()}" to "{os.path.join(os.path.join(os.getcwd(),distdict[f]),f)}"\n')

                        break

if __name__ == '__main__':
    
    while True:
        organizer()
        time.sleep(1)
        continue
