# DATALUTA
Este é um projeto do PetComputação da UFMS juntamente com a UNB (Universidade de Brasilia) de fazer extração de dados dos portais de noticias relacionados aos movimentos indigenas 

# Campos Filtrados
- Titulo da noticia
- Fonte
- Data
- Local

# Estratégias 
1° é feito um filtro nas URLS do titulo, com 3 funções 
| Função | Filtro |
| ------ | ------ |
| Ocorrencia1 | Extraindo informação do através do \|  |
| Ocorrencia2 | Extraindo informação do através do - |
| Ocorrencia3 | Sem filtro |

Para isso dividi os links das matérias em 3 arquivos que correspondem esses contextos

2° Usando a função netloc do python onde ele separa uma url em partes, 
Por exemplo, em um URL como https://www.example.com:8080/path/to/resource, o componente netloc seria www.example.com:8080. Aqui, www.example.com é o domínio, e 8080 é a porta.

```
    url = "https://www.example.com/path/to/resource"
    parsed_url = urlparse(url)
    parsed_url.netloc

```

# Tecnologias
- Python 3.11.6
- Requests
- BeautifulSoup
- pandas

