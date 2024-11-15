import openai
from openai import OpenAI
import os


def send_prompt(client,article_text):
    prompt = """
    Będziesz miał podany artykuł. Przekształć go w kod HTML. Użyj odpowiednich tagów HTML, 
    aby zorganizować treść artykułu. Zaznacz miejsca na grafiki przy użyciu tagu 
    <img> z atrybutem src='image_placeholder.jpg'. Dodaj do każdej grafiki atrybut alt 
    z opisem grafiki, który może zostać użyty do wygenerowania jej i podpis pod grafiką w odpowiednim tagu HTML. Kod HTML powinien 
    obejmować wyłącznie zawartość między tagami <body> i </body>.
    """
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

def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()
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
    if not os.path.exists(input_file):
        print(f"Plik {input_file} nie istnieje!")
        return
    article_text = read_file(input_file)
    print(article_text)
    response = send_prompt(client,article_text)
    print(response)

if __name__ == "__main__":
    main()