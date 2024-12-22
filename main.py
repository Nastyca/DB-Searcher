import os
import re
import json
import subprocess

from colorama import Fore

os.system("cls")

dossiers = ['Le chemin jusquà votre dossier ICI / HERE']

recherche_database = input(f"{Fore.LIGHTMAGENTA_EX}Entrez votre recherche -->{Fore.RESET} ")
print(f"")

def search(term: str, path: str):
    try:
        escaped_term = re.escape(term)
        command = ['rg', '-i', escaped_term, path, '--json']
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding='utf-8', errors='ignore')

        base_path = os.path.abspath(dossier)

        if process.stdout:
            for line in process.stdout:
                try:
                    json_data = json.loads(line)
                    if json_data['type'] == 'match':
                        file_path = json_data['data']['path']['text']
                        relative_path = os.path.relpath(file_path, base_path)

                        if 'text' in json_data['data']['lines']:
                            line_text = json_data['data']['lines']['text'].strip().replace('\n', '')
                            highlighted_text = re.sub(
                                f"({escaped_term})",
                                f"{Fore.GREEN}\\1{Fore.RESET}",
                                line_text,
                                flags=re.IGNORECASE
                            )
                        else:
                            highlighted_text = ""

                        line_number = json_data['data']['line_number']

                        print(
                            f"{Fore.BLUE}[{Fore.WHITE}Fichier : {relative_path}{Fore.BLUE}] "
                            f"{Fore.WHITE}> {Fore.BLUE}[{Fore.WHITE}Ligne : {line_number}{Fore.BLUE}] "
                            f"{Fore.WHITE}> {Fore.BLUE}[{Fore.WHITE}Texte : {highlighted_text}{Fore.BLUE}]"
                        )

                except json.JSONDecodeError:
                    continue

        _, stderr = process.communicate()
        if stderr:
            print(f"{Fore.RED}[-] Erreur lors de l'exécution de la commande ripgrep{Fore.RESET}")
            print(stderr)

    except FileNotFoundError:
        print(f"{Fore.RED}[-] Ripgrep n'est pas installé...{Fore.RESET}")
        input(f"\n{Fore.RESET}Appuyez sur ENTRÉE pour continuer --> ")

for dossier in dossiers:
    search(recherche_database, dossier)
