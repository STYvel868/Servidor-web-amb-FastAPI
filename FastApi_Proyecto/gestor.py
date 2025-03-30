import os
import json
from typing import List, Dict, Any

# Nom del arxiu JSON
nom_fitxer = "alumnes.json"

# Carrega dades inicials
def carregar_dades() -> List[Dict[str, Any]]:
    # Utilitzem try except per si no existeix l'arxiu
    try:
        # Declarem un arxiu f i l'obrim passant-li com argument nom_fixter
        # Li passem 'r' com argument per llegir-ho i encoding en 'utf-8'
        with open(nom_fitxer, 'r', encoding='utf-8') as f:
            # Importem el módul de json i cridem a la funció load per carregar-ho
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        # Si apareix una excepció retornem una llista buida
        return []

# Guardar dades, en aquesta funció indiquem que no ha de retornar res amb el 'None'
def desar_dades(alumnes: List[Dict[str, Any]]) -> None:
    # Declarem un arxiu f i l'obrim per escriure noves dades
    # Li passem com a argument w per poder escriure i encoding 'utf-8'
    with open(nom_fitxer, 'w', encoding='utf-8') as f:
        # Importem el módul de json i fem un dump amb les dades sobre l'arxiu f
        # Amb indent especifiquem la quantitat de espais d'un tabulador 
        # Amb ensure_ascii evitem caràcters invàlids per a que s'escriguin malament
        json.dump(alumnes, f, indent=4, ensure_ascii=False)

# Genera un nou ID
def nou_id(alumnes: List[Dict[str, Any]]) -> int:
    # Declarem maxId com None
    maxId = None
    # Iterem sobre la llista d'alumnes
    for alumne in alumnes :
        # Si es el primer alumne igualemn maxId a aquesta id    
        if maxId == None:
            maxId = alumne["id"]
        # Si l'id del alumne es major actualitzem
        elif alumne["id"] > maxId :
            maxId = alumne["id"] 
    # Si la llista es buida retornem 1
    if maxId == None :
        return 1
    # Retornem la nova id
    else :
        return maxId
    
# Menú principal
def menu() -> str:
    # Si estem a windows ('nt') natejem pantalla amb la comanda 'cls'
    if os.name == 'nt' :
        os.system('cls')
    # Si estem a linux natejem pantalla amb la comanda 'clear'
    else :
        os.system('clear')
    # Mostrem el menú
    print("Gestió alumnes")
    print("-------------------------------")
    print("1. Mostrar alumnes")
    print("2. Afegir alumne")
    print("3. Veure alumne")
    print("4. Esborrar alumne")
    print("5. Desar a fitxer")
    print("6. Llegir fitxer")
    print("0. Sortir")
    # Amb la funcio input llegim el que escribim a la consola hi ho guardem a la variable
    inputConsola = input("> ")
    return inputConsola

# Funcionalitats
# Funció per mostrar alumnes
def mostrar_alumnes(alumnes: List[Dict[str, Any]]) -> None:
    # Si estem a windows ('nt') natejem pantalla amb la comanda 'cls'
    if os.name == 'nt' :
        os.system('cls')
    # Si estem a linux natejem pantalla amb la comanda 'clear'
    else :
        os.system('clear')
    print("Llistat d'alumnes")
    print("-------------------------------")
    for alumne in alumnes:
        # Imprimim en format f la id del alumne, el nom i el seu cognom
        # Exemple de format f:
        # nom = "Alicia"
        # edad = 35
        # print(f"Em dic {nom} y tinc {edat} anys.")
        print(f"ID: {alumne['id']} | Nom: {alumne['nom']} {alumne['cognom']}")

# Funcio per afegir alumnes
def afegir_alumne(alumnes: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    # Si estem a windows ('nt') natejem pantalla amb la comanda 'cls'
    if os.name == 'nt' :
        os.system('cls')
    # Si estem a linux natejem pantalla amb la comanda 'clear'
    else :
        os.system('clear')
    print("Afegir nou alumne")
    print("-------------------------------")
    # Generem un nou ID
    nouId = nou_id(alumnes)
    # Creem els nous alumnes usant inputs
    nou_alumne = {
        'id': nouId,
        'nom': input("Nom: "),
        'cognom': input("Cognom: "),
        'data': {
            'dia': int(input("Dia de naixement: ")),
            'mes': int(input("Mes de naixement: ")),
            'any': int(input("Any de naixement: "))
        },
        'email': input("Email: "),
        # Com feina es un s/n usem la funció lower per si ho fiquem en mayus i evaluem si es True o False
        'feina': input("Treballa? (s/n): ").lower() == 's',
        'curs': input("Curs: ")
    }
    # Afegim el nou alumne amb la funció appenda a la llista d'alumnes
    alumnes.append(nou_alumne)
    print("\nAlumne afegit correctament!")
    # Retornem els alumnes
    return alumnes

# Funció per veure alumnes
def veure_alumne(alumnes: List[Dict[str, Any]]) -> None:
    # Si estem a windows ('nt') natejem pantalla amb la comanda 'cls'
    if os.name == 'nt' :
        os.system('cls')
    # Si estem a linux natejem pantalla amb la comanda 'clear'
    else :
        os.system('clear')
    print("Veure alumne")
    print("-------------------------------")
    try:
        alumneId = int(input("ID de l'alumne: "))
        alumneTrobat = None
        for alumne in alumnes :
            if alumneId == alumne["id"] :
                alumneTrobat = alumne

        if alumne != None:
            print(f"ID: {alumne['id']}")
            print(f"Nom: {alumne['nom']} {alumne['cognom']}")
            print(f"Data de naixement: {alumne['data']['dia']}/{alumne['data']['mes']}/{alumne['data']['any']}")
            print(f"Email: {alumne['email']}")
            print(f"Treballa: {'Sí' if alumne['feina'] else 'No'}")
            print(f"Curs: {alumne['curs']}")
        else:
            print("Alumne no trobat!")
    except ValueError:
        print("ID ha de ser un número!")

def esborrar_alumne(alumnes: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    # Si estem a windows ('nt') natejem pantalla amb la comanda 'cls'
    if os.name == 'nt' :
        os.system('cls')
    # Si estem a linux natejem pantalla amb la comanda 'clear'
    else :
        os.system('clear')
    print("Esborrar alumne")
    print("-------------------------------")
    try:
        alumneId = int(input("ID de l'alumne: "))
        alumnesLlista = []
        for alumne in alumnes :
            if alumneId != alumne["id"] :
                alumnesLlista.append(alumne)            
        print("Alumne esborrat correctament!")
        return alumnesLlista
    except ValueError:
        print("ID ha de ser un número!")
        return alumnes

# Programa principal
def main():
    alumnes = carregar_dades()
    
    while True:
        match menu():
            case "1":
                mostrar_alumnes(alumnes)
                input("\nPrem Enter per continuar...")
            
            case "2":
                alumnes = afegir_alumne(alumnes)
                input("\nPrem Enter per continuar...")
            
            case "3":
                veure_alumne(alumnes)
                input("\nPrem Enter per continuar...")
            
            case "4":
                alumnes = esborrar_alumne(alumnes)
                input("\nPrem Enter per continuar...")
            
            case "5":
                desar_dades(alumnes)
                print("Dades desades correctament!")
                input("\nPrem Enter per continuar...")
            
            case "6":
                alumnes = carregar_dades()
                print("Dades carregades correctament!")
                input("\nPrem Enter per continuar...")
            
            case "0":
                print("Adeu!")
                break
            
            case _:
                print("\nOpció incorrecta!")
                input()

if __name__ == "__main__":
    main()