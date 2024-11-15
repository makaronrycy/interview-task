import openai
from openai import OpenAI
import os


def send_prompt(client,article_text):
    prompt = """
    Będziesz miał podany artykuł. Przekształć go w kod HTML. 
    Użyj odpowiednich tagów HTML, aby zorganizować treść artykułu. Nie zmieniaj i nie dodawaj nic do treści artykułu, ani nie zmieniaj kolejności. 
    Podziel artykuł na używając semantycznych elementów HTML5 takich jak header, section, article,footer. 
    Zaznacz miejsca na grafiki przy użyciu tagu <img> z atrybutem src='image_placeholder.jpg', będące w środku <figure>. Do każdej grafiki atrybut alt 
    z dokładnym opisem grafiki, który zostanie użyty jako zapytanie do wygenerowania odpowiedniej grafiki i podpis pod grafiką po polsku w tagu figcaption.
    Użyj <strong> lub <em> do podkreślenia wyrazów. 
    Kod HTML powinien obejmować wyłącznie zawartość między tagami <body> i </body>, czyli nie generować tych znaczników. 
    Zwróć sam tekst bez twojego formatowania kodu html(```html i ```)
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
def write_to_preview(template_path,html_path,preview_path):
    template = read_file(template_path)
    html = read_file(html_path)
    body_location = template.find("<body>") +len("<body>")
    preview_content = template[:body_location]+html+template[body_location:]
    write_to_file(preview_path,preview_content)
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

    #czytanie artykułu
    article_text = read_file(input_file)
    #wysłanie zapytania
    response = send_prompt(client,article_text)
    #zapisanie HTML odpowiedzi
    write_to_file(output_file,response)
    #generowanie podglądu
    write_to_preview(template_file,output_file,preview_file)
if __name__ == "__main__":
    main()