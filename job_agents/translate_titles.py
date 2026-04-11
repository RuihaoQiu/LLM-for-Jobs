import re
from typing import List
import asyncio
from langcodes import Language
from .client import aclient, DEFAULT_MODEL, process_in_batches, load_prompt

_prompt_to_en = load_prompt("translate_titles_to_en")
_prompt_from_en_template = load_prompt("translate_titles_from_en")

numerical_regex = re.compile(r"^\d+[.]?\s*")

def rm_newlines(title: str) -> str:
    return re.sub(r"\n+", " ", title)

def make_input_content(titles: List[str]) -> str:
    return "\n".join([f"{i+1}. "+ rm_newlines(title) for i, title in enumerate(titles)])

async def fetch_response_to_en(titles: List[str]) -> str:
    content = make_input_content(titles)
    messages = [
        {"role": "system", "content": _prompt_to_en},
        {"role": "user", "content": content},
    ]

    try:
        response = await aclient.chat.completions.create(
            model=DEFAULT_MODEL,
            messages=messages
        )
        output = response.choices[0].message.content
        return output
    except Exception as e:
        print(f"Error processing input: {str(e)}")
        return ""

async def fetch_response_from_en(titles: List[str], to_lang_code: str) -> str:
    content = make_input_content(titles)
    language = Language.get(to_lang_code).display_name()
    prompt = _prompt_from_en_template.format(language=language)
    messages = [
        {"role": "system", "content": prompt},
        {"role": "user", "content": content},
    ]

    try:
        response = await aclient.chat.completions.create(
            model=DEFAULT_MODEL,
            messages=messages
        )
        output = response.choices[0].message.content
        return output
    except Exception as e:
        print(f"Error processing input: {str(e)}")
        return ""

def remove_numerical(title: str) -> str:
    return numerical_regex.sub("", title).strip()

def process_output_content(content: str) -> List[str]:
    titles = content.split("\n")
    return [remove_numerical(title) for title in titles]

def get_titles(contents: List[str]) -> List[str]:
    return [title for content in contents for title in process_output_content(content)]

async def translate_titles_to_en(titles: List[str], batch_size: int = 10) -> List[str]:
    responses = await process_in_batches(titles, fetch_response_to_en, batch_size, desc="Translating to EN")
    return get_titles(responses)

async def translate_titles_from_en(titles: List[str], to_lang_code: str, batch_size: int = 10) -> List[str]:
    async def fetch(batch: List[str]) -> str:
        return await fetch_response_from_en(batch, to_lang_code)
    responses = await process_in_batches(titles, fetch, batch_size, desc="Translating from EN")
    return get_titles(responses)

if __name__ == "__main__":
    titles_lt = [
        "Vyriausiasis (-ioji) teisininkas (-ė",
        "Vyriausiasis teisininkas (-ė) Licencijų administravimo skyriuje",
        "VYRESNIOJI (-YSIS) TEISININKĖ (-AS) (KORPORATYVINĖ IR ĮMONIŲ TEISĖ",
        "Teisininkas (-ė",
        "Inovacijų ekspertas (-ė",
        "Informacinių sistemų saugos pareigūnas (-ė) (įgaliotinis (-ė)) 0,5 et. darbo krūviu",
        "Strateginio planavimo skyriaus finansų planuotojo (-jos",
        "Komunikacijos skyriaus patarėjo(-jos",
        "Teisininkas (-ė",
        "TEISININKĖ (-AS) (GINČŲ TEISĖ"
    ]
    translated_titles = asyncio.run(translate_titles_to_en(titles_lt, batch_size=2))
    print(translated_titles)