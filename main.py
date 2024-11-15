import openai
from openai import OpenAI
import os


def send_prompt(client,article_text):
    prompt = """
    Będziesz miał podany artykuł. Przekształć go w kod HTML. 
    Użyj odpowiednich tagów HTML, aby zorganizować treść artykułu. Podziel artykuł na używając semantycznych elementów HTML5 takich jak header, section, article. Zaznacz miejsca na grafiki przy użyciu tagu 
    <img> z atrybutem src='image_placeholder.jpg'. Do każdej grafiki atrybut alt 
    z opisem grafiki, który zostanie użyty jako zapytanie do wygenerowania odpowiedniej grafiki i podpis pod grafiką po polsku w odpowiednim tagu HTML5. Kod HTML powinien 
    obejmować wyłącznie zawartość między tagami <body> i </body>. 
    Nie używaj swojego formatu kodowego html. 
    """
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role":"system",
                    "content": prompt
                },
                {
                    "role":"user",
                    "content": article_text
                }
            ]
        )
        return response.choices[0].message.content
    except openai.OpenAIError as e:
        print(f"Błąd z łączeniem z API: {e}")
        exit(1)

def read_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        print(f"Plik {input_file} nie istnieje!")
        exit(1)

def write_to_file(file_path,content):
    try:
        with open(file_path,'w',encoding='utf-8') as file:
            file.write(content)
            print(f"Plik {file_path} wygenerowany.")
    except IOError as e:
        print(f"Błąd podczas zapisywania {file_path}: {e}")
        exit(1)
def write_to_preview(template_path,article_path,preview_path):
    return
def main():
    #Pobierz klucz z zmiennych środowiskowych
    #Na windows otwieram konsole i wpisujemy setx OXIDO_OPEN_AI_KEY "klucz do openai"
    openai_key = os.getenv("OXIDO_OPEN_AI_KEY")
    if openai_key == None:
        print("Brak klucza API, ustaw klucz OXIDO_OPEN_AI_KEY w zmiennych środowiskowych")
        return
    client = OpenAI(api_key=openai_key)
    input_file = "artykul.txt"
    output_file = "artykul.html"
    template_file = "szablon.html"
    preview_file = "podglad.html"
    article_text = read_file(input_file)
    response = send_prompt(client,article_text)
    write_to_file(output_file,response)

if __name__ == "__main__":
    main()