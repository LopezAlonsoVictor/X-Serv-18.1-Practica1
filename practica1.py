#!/usr/bin/python3

import webapp

paginas={}

paginasinv={}

formulario = '''
            <form action="" Method="POST">
            Introduce URL:<br>
            <input type="text" name="URL" placeholder="For Example: 'www.gooogle.es'"><br>
            <input type="submit" value="Enviar">
</form>
'''

def retocarurl(url):
    if url.startswith('http%3A%2F%2F'):
        url = "http://" + url.split('F%2F')[1]
    elif url.startswith('http%3A%2F%2F'):
        url = "http://" + url.split('F%2F')[1]
    else:
        url = "http://" + url 
    return url

def adddiccionarios(url):
    url = retocarurl(url)
    if(buscardiccionario(paginasinv,url) == None):
        paginas[str(len(paginas))] = url
        paginasinv[url] = str(len(paginasinv))
        aux_file = open("file_urls.csv","w")
        printdiccionariofile(paginas,aux_file)
        aux_file.close()
    

    

def petpagina(recurso):
    if recurso.startswith('/0') or recurso.startswith('/1') or recurso.startswith('/2') or recurso.startswith('/3') or recurso.startswith('/4') or recurso.startswith('/5') or recurso.startswith('/6') or recurso.startswith('/7') or recurso.startswith('/8') or recurso.startswith('/0'):
        return True
    else:
        return False

def buscardiccionario(diccionario,clave):
    try:
        return diccionario[clave]
    except KeyError:
        return None

def printdiccionariofile(paginas,aux_file):
    for number in paginas:
        aux_file.write(number+","+paginas[number]+"\n") 

def printdiccionariohtml(paginas):
    total_dic = "<br>"
    for number in paginas:
        total_dic = total_dic + number + " : "+"<a href ='"+paginas[number]+"'>"+paginas[number]+"</a>" + "<br>"
    total_dic = total_dic + "<br>" 
    return total_dic

def leerfichero(aux_file):
    for line in aux_file:
        n,r = line.split(',')
        r = r.split('\n')[0]
        paginas[n]= r
        

class listweb(webapp.webApp):

    def parse(self,request):
        return(request.split()[0],request.split()[1],request)

    def __init__(self, hostname, port):
        try:
            aux_file = open('file_urls.csv','r')
            leerfichero(aux_file)
            aux_file.close()
        except:
            aux_file = open('file_urls.csv','w')
            aux_file.close()
        super().__init__(hostname, port)

    def process(self, parsedRequest):
        metodo,recurso,peticion = parsedRequest
        if metodo == "POST":
            if "URL" not in peticion:
                codigo = "404 Not Found"
                respuesta = "Not Found"
            else:
                codigo = "200 ok"               
                cuerpo = peticion.split('\r\n\r\n',1)[1]
                cuerpo = cuerpo.split('=')[1]
                if cuerpo != "":
                    adddiccionarios(cuerpo)
                respuesta = "<body>"+ printdiccionariohtml(paginas) + "<h1>" + formulario + "</h1></body>"
        elif recurso == '/':
            codigo = "200 ok"
            respuesta = "<body>"+ printdiccionariohtml(paginas) + "<h1>" + formulario + "</h1></body>";
        elif petpagina(recurso):
            respuesta = buscardiccionario(paginas,recurso.split('/')[1])
            if respuesta == None:
                codigo = "404 Not found"
                respuesta = "HTTP ERROR Recurso no disponible"
            else:
                codigo = "302 Found"
                respuesta = "<head><meta http-equiv=Refresh content=0;url="+respuesta+"></head>"
        else:
            codigo = "404 Not Found"
            respuesta = "Not Found"
        return (codigo, "<html>"+respuesta+"</html>")


if __name__ == "__main__":
    miapp = listweb("localhost", 1234)
