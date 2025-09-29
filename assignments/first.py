from collections import Counter
from pathlib import Path
from typing import Dict
import argparse
import string
from time import time

from loguru import logger
import matplotlib.pyplot as plt

# Funzione che permette di estrarre dal file il 
# solo testo del libro (esclude preambolo, licenza, ecc)
def extract_main_text(text:str, skip_extra: bool = False) -> str:
    # Restituisce il testo completo se skip_extra 
    # è falso (== se non richiedo di estrarre il main text)
    if not skip_extra:
        return text
    
    if skip_extra:
        # Cerca i delimitatori tipici dei libri Project Gutenberg
        # (in lower case perché viene sempre chiamata su testi in lower case)
        start_marker = "*** start of the project gutenberg ebook"
        end_marker   = "*** end of the project gutenberg ebook"

        start_idx = text.find(start_marker)
        end_idx = text.find(end_marker)

        # Controllo se ho trovato i marker (in caso contrario, 
        # gli idx vengono inizializzati automaticamente a -1)
        if start_idx != -1 and end_idx != -1:
            # Prendi solo il testo tra start e end
            return text[start_idx + len(start_marker): end_idx]
        else:
            return text


def frequency_counter(file_path: Path, skip_extra: bool = False) -> Dict[str, float]:
    # Leggo il file e metto tutto in minuscolo
    text = file_path.read_text(encoding="utf-8", errors="ignore").lower()
    # Chiamo extract_main_text nel caso lo decida da linea di comando
    text = extract_main_text(text, skip_extra=skip_extra)
    
    # Tengo solo le lettere, togliendo caratteri speciali o non ascii
    letters = [c for c in text.lower() if c in string.ascii_lowercase]

    total = len(letters)

    # Messaggio nel caso non si trovino lettere nel testo
    if total == 0:
        logger.info("No letter found.") 

    
    logger.debug(f"Total number of letters: {total}")

    conteggio = Counter(letters)

    # Costruisci il dizionario: {lettera: frequenza_relativa}
    frequencies = {lettera: freq / total for lettera, freq in conteggio.items()}
    frequencies = dict(sorted(frequencies.items()))

    logger.info(f"Relative frequencies: {frequencies}")
    
    return frequencies  

# Funzione che mostra un'istogramma delle frequenze
def show_histogram(frequencies: dict):
    letters = list(frequencies.keys())
    values = list(frequencies.values())

    plt.figure(figsize=(12, 6))
    plt.bar(letters, values, color='green')
    plt.xlabel('Letters')
    plt.ylabel('Relative frequency')
    plt.title('Letters frequency histogram')
    plt.ylim(0, max(values)*1.1)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.show()

# Funzione che restituisce le statistiche di base del file di testo
def book_stats(file_path: Path, skip_extra: bool = False) -> Dict:
    text = file_path.read_text(encoding="utf-8", errors="ignore").lower()
    # Chiamo extract_main_text nel caso lo decida da linea di comando
    text = extract_main_text(text, skip_extra=skip_extra)

    num_chars = len(text)
    num_letters = sum(1 for c in text.lower() if c in string.ascii_lowercase)
    num_words = len(text.split())
    num_lines = len(text.splitlines())

    stats = {
        "Number of characters": num_chars,
        "Number of letters": num_letters,
        "Number of words": num_words,
        "Number of lines": num_lines
    }
    return stats

parser = argparse.ArgumentParser(
        description="Evaluates the relative frequency of letters in a text."
    )
parser.add_argument(
        "file",
        type=Path,
        help="File path."
    )
parser.add_argument(
        "--histogram", "-g",
        action="store_true",
        help="Displays the frequency histogram."
    )
parser.add_argument(
    "--skip-extra", "-s",
    action="store_true",
    help="Skips the text sections that don't belong to the book (preamble, license, etc.)"
)
parser.add_argument(
    "--stats", "-t",
    action="store_true",
    help="Displays the book statistics (characters, letters, words, lines)"
)
args = parser.parse_args()

    # Calcolo del tempo di esecuzione
start_time = time()

frequencies = frequency_counter(args.file, skip_extra=args.skip_extra)


if args.histogram and frequencies:
        show_histogram(frequencies)

if args.stats:
        stats = book_stats(args.file, skip_extra=args.skip_extra)
        logger.info("Book statistics:")
        for k, v in stats.items():
            logger.info(f"{k}: {v}")

elapsed = time() - start_time  
logger.info(f"Total running time: {elapsed:.5f} seconds.")


