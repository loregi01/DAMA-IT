import requests

def invia_richiesta_al_server():
    url = 'http://127.0.0.1:5000/api'
    dati = {'key': 'value'}  # Dati da inviare al server Flask
    response = requests.post(url, json=dati)
    if response.status_code == 200:
        print("Richiesta inviata con successo!")
        print("Risposta dal server:", response.text)
    else:
        print("Errore durante l'invio della richiesta:", response.status_code)

if __name__ == "__main__":
    invia_richiesta_al_server()
