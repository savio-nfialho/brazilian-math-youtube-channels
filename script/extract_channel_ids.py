"""# Parte 0: Extração de IDS dos canais """

import requests
from bs4 import BeautifulSoup

def extrair_id_canal(urls):
    """
    Recebe uma lista de URLs de canais do YouTube (handles ou custom)
    e retorna o ID real (UC...).
    """
    ids_canais = {}
    for url in urls:
        try:
            response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
            response.raise_for_status()

            soup = BeautifulSoup(response.text, "html.parser")
            link_canonica = soup.find("link", {"rel": "canonical"})

            if link_canonica and "href" in link_canonica.attrs:
                canonica = link_canonica["href"]
                if "/channel/" in canonica:
                    canal_id = canonica.split("/channel/")[-1]
                    ids_canais[url] = canal_id
                else:
                    ids_canais[url] = "Não foi possível extrair o ID."
            else:
                ids_canais[url] = "Tag canônica não encontrada."
        except Exception as e:
            ids_canais[url] = f"Erro: {e}"

    return ids_canais

if __name__ == "__main__":
    lista_de_urls = [
    "https://www.youtube.com/@Giscomgiz",
    "https://www.youtube.com/@MarcosAba",
    "https://www.youtube.com/@sandrocuriodicasdemat",
    "https://www.youtube.com/@MatematicaRio",
    "https://www.youtube.com/@professoraangelamatematica",
    "https://www.youtube.com/@equacionamatematica",
    "https://www.youtube.com/@Matem%C3%A1ticanoPapel",
    "https://www.youtube.com/@mrbeandamatematica",
    "https://www.youtube.com/channel/UCoB7wLA9hJ8-H4ss1KlR_JQ",
    "https://www.youtube.com/@profdombrauskas",
    "https://www.youtube.com/@estudematematica",
    "https://www.youtube.com/c/Matem%C3%A1ticaemEvid%C3%AAncia",
    "https://www.youtube.com/c/Matem%C3%A1ticacomAMORim",
    "https://www.youtube.com/c/Matem%C3%A1ticaemExerc%C3%ADcios",
    "https://www.youtube.com/@matematicadatamires",
    "https://www.youtube.com/c/Matem%C3%A1ticaBoa",
    "https://www.youtube.com/@matematicadoaluno",
    "https://www.youtube.com/@Murakami.",
    "https://www.youtube.com/@praticandomatematica",
    "https://www.youtube.com/@todaamatematica",
    "https://www.youtube.com/c/Matem%C3%A1ticacomAl%C3%AA",
    "https://www.youtube.com/@portalmatematicaobmep",
    "https://www.youtube.com/@ProfHeraldo",
    "https://www.youtube.com/@MatematicaGenial",
    "https://www.youtube.com/@SomatizeEdnaMendes",
    "https://www.youtube.com/@profreginaldomoraes",
    "https://www.youtube.com/@planetamatematica",
    "https://www.youtube.com/@ProfessorVandeir",
    "https://www.youtube.com/@EurekaMatematica",
    "https://www.youtube.com/@apol",
    "https://www.youtube.com/@matematicamastigada",
    "https://www.youtube.com/@principia_matematica",
    "https://www.youtube.com/@matematicajovem",
    "https://www.youtube.com/@matematicauniversitariaRenan",
    "https://www.youtube.com/c/ProfessoraNoemiMatem%C3%A1tica",
    "https://www.youtube.com/@ameninadamatematica",
    "https://www.youtube.com/c/FiqueTranquiloMatem%C3%A1tica",
    "https://www.youtube.com/c/RenatodaMatem%C3%A1tica",
    "https://www.youtube.com/@300segundosdematematica",
    "https://www.youtube.com/@rataodamatematica",
    "https://www.youtube.com/c/RAMatem%C3%A1tica",
    "https://www.youtube.com/@aprendermatematicaa",
    "https://www.youtube.com/c/Matem%C3%A1ticaBemF%C3%A1cilOficial",
    "https://www.youtube.com/@curso.matematica.online",
    "https://www.youtube.com/@matematicaComoHobby",
    "https://www.youtube.com/@matematicaparaleigos",
    "https://www.youtube.com/@monstrodamatematica/",
    "https://www.youtube.com/@OmatematicoGrings/",
    "https://www.youtube.com/@HelpEngenharia",
    "https://www.youtube.com/@professorferretto/",
    "https://www.youtube.com/@nerckie/"
    ]

    resultados = extrair_id_canal(lista_de_urls)

    for original, canal_id in resultados.items():
        print(f"{canal_id}\n")
