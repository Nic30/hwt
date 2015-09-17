import os, re


subs = {
        #"/static/template/bower_components/":"/static/bower_components/",
        "../bower_components/":"/static/bower_components/",
        "../js/":"/static/template/js/",
        "../dist/":"/static/template/dist/"
        }



def fix(filename):
    with open(filename) as f:
        s = f.read()
    for k,v in subs.items():
        s = s.replace(k, v)
        
    #print(s)
    with open(filename, mode='w') as f:
        f.write(s)
    
    
    
    
    
if __name__ == "__main__":
    fix("templates/index.html")