import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import pandas as pd

#---------------------------------------------------------------------------Funções----------------------------------------------------------------------------------#

def extrair_dominio(url):
    parsed_url = urlparse(url)
    # Pega o domínio (sem www, por exemplo)
    dominio = parsed_url.netloc
    return dominio

def IsWordpress(Formatacao):           
    
    data = Formatacao.find("meta", {'property': ['article:published_time','og:updated_time' ]})
    
    # Se a tag for encontrada, imprime o valor do atributo content
    if data and 'content' in data.attrs:
        data_publicacao = data.attrs['content']
        data_sem_hora = data_publicacao.split('T')[0]
        ano, mes, dia = data_sem_hora.split('-')
            
        #Inverte para o formato DD-MM-YYYY
        data_invertida = f"{dia}-{mes}-{ano}"
        return data_invertida
                  
    return "nao entrado Wordpress"

def DataTime(Formatacao):
    # Encontra a tag <time>
    time = Formatacao.find("time")
    datetime_value = time.get("datetime")  # Pega o valor do atributo datetime
    if datetime_value and datetime_value != "#":
        data = datetime_value  # Se o datetime for válido, usa ele
    else:
        data = time.text.strip()  # Pega o texto dentro da tag <time>
    
    return data


def Meta(Formatacao):
    
    meta_tag = Formatacao.find("meta", {'property': ['og:article:published_time', 'article:published_time']})

    if meta_tag and 'content' in meta_tag.attrs:
        # Extrai a data do atributo 'content' e formata
        data_publicacao = meta_tag['content']
        data_sem_hora = data_publicacao.split('T')[0]
        data_sem_espaço = data_sem_hora.split(' ')[0]
        ano, mes, dia = data_sem_espaço.split('-')
        
        # Formata para o formato DD-MM-YYYY
        data_invertida = f"{dia}-{mes}-{ano}"
        return data_invertida
    
    return "Não encontrado meta"

def Divms(Formatacao):
    data_divs = Formatacao.find_all("div", class_="ms-1")  # pega todas as divs com a classe "ms-1", no caso da agencia Para, duas.

    # a função next procura todos os elementos da nossa lista, neste caso ela percorre todas as divs com class="ms-1" 
    # contém uma data (procurando a barra '/' ou '-')
    data_div = next((div for div in data_divs if div.text and ("/" in div.text or "-" in div.text)), None)

    # Se encontrou, extrai o texto e remove espaços extras
    data = data_div.text.strip() if data_div else None
    return data

def DivAutor(Formatacao):
    data_texto = Formatacao.find("div", class_="AutorDataPublicacao")
    data_texto = data_texto.text.strip()
    data = data_texto.split(" | ")[1]
    return data

def DivNews(Formatacao):
    data_texto = Formatacao.find("div", class_="news-publishinfo")
    data = data_texto.find("p").text.strip()
    return data

def DataSpan(Formatacao):
    data_texto =  Formatacao.find("span")
    data = data_texto.text.strip()
    return data


def Ocorrencia1(site, linha):

    Formatacao = BeautifulSoup (site.text, 'html.parser')
    titulo = Formatacao.title.string
    titulof = titulo.split("|")[0]
    local = None
    parsed_url = urlparse(linha)  
    dominio = parsed_url.netloc

    if 'wp-content' in Formatacao.prettify() or 'wp-admin' in Formatacao.prettify():        
        data = IsWordpress(Formatacao)   

    elif Formatacao.find("meta", {'property': ['og:article:published_time', 'article:published_time','article:modified_time']}):
        data = Meta(Formatacao)

    elif Formatacao.find("time"):
        data = DataTime(Formatacao)
    
    elif Formatacao.find("div", class_="ms-1"):
        data = Divms(Formatacao)

    else:
        data = None  

    return  [titulof, dominio, local, data]



def Ocorrencia2(site, linha):
    Formatacao = BeautifulSoup (site.text, 'html.parser')
    titulo = Formatacao.title.string
    titulof = titulo.split('–')[0] 
    parsed_url = urlparse(linha)  
    dominio = parsed_url.netloc
    
    if 'wp-content' in Formatacao.prettify() or 'wp-admin' in Formatacao.prettify():        
        data = IsWordpress(Formatacao)   

    elif Formatacao.find("meta", {'property': ['og:article:published_time', 'article:published_time']}):
        data = Meta(Formatacao)

    elif Formatacao.find("time"):
        data = DataTime(Formatacao)

    elif Formatacao.find("div", class_="AutorDataPublicacao"):
        data = DivAutor(Formatacao)
    
    elif Formatacao.find("div", class_="news-publishinfo"):
        data = DivNews(Formatacao)
       
    else:
        data = None   

    local = None
    return [titulof, dominio, local , data]



def Ocorrencia3(site, linha):
    Formatacao = BeautifulSoup (site.text, 'html.parser')
    titulo = Formatacao.title.string
    titulof = titulo.split("|")[0]
    parsed_url = urlparse(linha)  
    dominio = parsed_url.netloc
    if 'wp-content' in Formatacao.prettify() or 'wp-admin' in Formatacao.prettify():        
        data = IsWordpress(Formatacao)
        
    elif Formatacao.find("time"):
        data = DataTime(Formatacao)
    
    elif Formatacao.find("span"):
        data = DataSpan(Formatacao)

    else:
        data = None    
    local = None


    return [titulof, dominio, local,data ]





#---------------------------------------------------------------------------MAIN----------------------------------------------------------------------------------#


Lista1=["cimi.org.br","g1.globo.com","brasildefato.com.br","agenciabrasil.ebc.com.br", "metropoles.com",
        "midiamax.uol.com.br", "tvt.org.br", "socioambiental.org", "jornalistaslivres.org", "agenciapara.com.br", "gazetadocerrado.com.br",
        "revistaforum.com.br"]

Lista2=["seculodiario.com.br", "amazoniareal.com.br", "campograndenews.com.br", "folha.uol.com.br", "anovademocracia.com.br",
        "ihu.unisinos.br", "conexaoto.com.br", "combateracismoambiental.net.br", "folhabv.com.br", "sul21.com.br", 
        "cartacapital.com.br", "oeco.org.br", "folhabv.com.br", "racismoambiental.net.br", "em.com.br"]

Lista3=["uol.com.br", "oglobo.globo.com", "gov.br", "terra.com.br", "tapajósdefato.com.br", "correiobraziliense.com.br",
        "opovo.com.br", "agenciacenarium.com.br", "noticias.uol.com.br", "gov.br/pt-br", "correiodopovo.com.br",
        "funai.gov.br", "acritica.uol.com.br", "ndmais.com.br", "revistacenarium.com.br", "f5.folha.uol.com.br", "acritica.net"]

resultados=[]

with open ("links3.txt", 'r') as file:
    for linha in file:        
        linha = linha.strip()        
        response = requests.get(linha, 
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36' }, timeout=105) 
        # url, paprams, headers, cookies, auth, timeout, allow_redirects
        
        # Extrai o domínio da URL
        dominio_extraido = extrair_dominio(linha).replace("www.","").replace("www1.", "")
         


        if response.status_code == 200:
            response.encoding = 'utf-8'

            if dominio_extraido in Lista1:
                resultado = Ocorrencia1(response, linha)
                print(resultado)
                resultados.append(resultado)

            elif dominio_extraido in Lista2:
                resultado = Ocorrencia2(response, linha)
                print(resultado)
                resultados.append(resultado) 

            elif dominio_extraido in Lista3:
                resultado = Ocorrencia3(response, linha)
                print(resultado)
                resultados.append(resultado)

            else:
                print("")
                print("------")
                print("nao encontrado na base de dados")
                print(linha)
                print(dominio_extraido)
                print("------")

df = pd.DataFrame(resultados, columns=["Título", "Mídia", "Local", "Data"])

# Exportando para um arquivo Excel
df.to_excel("resultados.xlsx", index=False)

print("Resultados exportados para resultados.xlsx")