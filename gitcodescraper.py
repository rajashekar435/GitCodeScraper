import sys
import os
import shutil
import requests
from github import Github


#Always have a minimum of 3 arguments to search
if len(sys.argv) >= 3:
    #Keyword to search
    keyword = sys.argv[1]
    dir_name = sys.argv[2]
    if(len(sys.argv) == 4):
        limit = int(sys.argv[3])
    else:
        limit = float('inf')

    g = Github("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")

    codes = g.search_code(keyword)
    details = []
    file_names = dict()
    for i,code in enumerate(codes):
        if i == limit:
            break
        temp = code.download_url
        file_name = temp[temp.rindex("/")+1:]
        try:
            file_ext = file_name[file_name.rindex(".")+1:]
            file_name = file_name[:file_name.rindex(".")]
        except:
            file_ext = "txt"
        details.append([temp,file_name,file_ext])
        file_name_with_ext = file_name +"."+file_ext
        if(file_name_with_ext in file_names):
            file_names[file_name_with_ext] += 1
        else:
            file_names[file_name_with_ext] = 1
    if os.path.exists(dir_name):
        shutil.rmtree(dir_name)
    os.mkdir(dir_name)

    if dir_name[-1] != "/":
        dir_name += "/"

    print(len(details))
    for detail in details:
        print("Downloading "+detail[0])
        file_name_with_ext = detail[1]+"."+detail[2]
        file_name_count = file_names[file_name_with_ext]
        if( file_name_count > 1):
            file_name_with_path = dir_name + detail[1] + "." + detail[2]+" ("+str(file_name_count)+")"
            file_name_count -=1
            file_names[file_name_with_ext] = file_name_count
        else:
            file_name_with_path = dir_name + detail[1] + "." + detail[2]
        r = requests.get(detail[0])
        open(file_name_with_path,'w+',encoding="utf-8").write(r.text)
    
    print("Finished")