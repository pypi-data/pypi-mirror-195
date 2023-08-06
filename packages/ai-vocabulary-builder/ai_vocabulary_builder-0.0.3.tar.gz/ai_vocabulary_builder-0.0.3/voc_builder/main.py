"""Main entrance of AI Vocabulary Builder"""
import csv
import datetime
import logging
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from textwrap import dedent
from typing import List, TextIO

import click
import openai
from rich.panel import Panel
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.prompt import Prompt
from rich.table import Table

# Set logging to stdout by default
log_format = "%(asctime)s - %(name)s - [%(levelname)s]:  %(message)s"
logging.basicConfig(format=log_format, level=logging.DEBUG)

logger = logging.getLogger()

# The default path for storing the vocabulary book
DEFAULT_CSV_FILE_PATH = Path('~/aivoc_builder.csv').expanduser()

console = Console()


class VocBuilderError(Exception):
    """Base exception type for aivoc."""


@dataclass
class WordSample:
    """A word sample which is ready to be added into a vocabulary book

    :param word: The word itself, for example: "world"
    :param word_meaning: The Chinese meaning of the word
    :param pronunciation: The pronunciation of the word, "/wɔrld/"
    :param orig_text: The original text
    :param translated_text: The translated text
    """

    word: str
    word_meaning: str
    pronunciation: str
    orig_text: str
    translated_text: str


def write_new_one(text: str):
    """Write a new word to the vocabulary book"""
    builder = VocBuilderCSVFile(DEFAULT_CSV_FILE_PATH)
    progress = Progress(SpinnerColumn(), TextColumn("[bold blue] Querying OpenAI API"))
    known_words = builder.find_known_words(text)
    with progress:
        task_id = progress.add_task("get", start=False)
        try:
            word = get_word_and_translation(text, known_words)
            progress.update(task_id, total=1, advance=1)
        except VocBuilderError as e:
            console.print(f'[red] Error processing text, detail: {e}[red]')
            progress.update(task_id, total=1, advance=1)
            return

    table = Table(title="翻译结果", show_header=False)
    table.add_column("title")
    table.add_column("detail", overflow='fold')
    table.add_row("[bold]原文[/bold]", f'[grey42]{word.orig_text}[grey42]')
    table.add_row("[bold]中文翻译[/bold]", word.translated_text)
    table.add_row("[bold]生词（自动提取）[/bold]", word.word)
    table.add_row("[bold]释义[/bold]", word.word_meaning)
    table.add_row("[bold]发音[/bold]", word.pronunciation)

    console.print(table)

    if builder.is_duplicated(word):
        console.print(f'Word "{word.word}" is already in your vocabulary book, skip.', style='grey42')
        return

    builder.append_word(word)
    console.print(
        f'Word [bold]"{word.word}"[/bold] has been added to your vocabulary book, well done!', style='grey42'
    )
    console.print(f'Your vocabulary book now contains [bold]{builder.words_count()}[/bold] words.', style='grey42')
    console.print(f'Open file {builder.file_path} to review.', style='grey42')


class VocBuilderCSVFile:
    """A CSV file which stores the words

    :param file_path: The path of the .csv file
    """

    header_row = ('添加时间', '单词', '读音', '释义', '例句/翻译')

    def __init__(self, file_path: Path):
        # Initialize the file if not exists
        if not file_path.exists():
            with open(file_path, 'w') as fp:
                self._get_writer(fp).writerow(self.header_row)

        self.file_path = file_path

    def append_word(self, w: WordSample):
        """Append a word to the current file

        :param w: WordSample object
        """
        with open(self.file_path, 'a') as fp:
            self._get_writer(fp).writerow(
                (
                    datetime.datetime.now().strftime('%Y-%m-%d %H:%M'),
                    w.word,
                    w.pronunciation,
                    w.word_meaning,
                    '{} / {}'.format(w.orig_text, w.translated_text),
                )
            )

    def words_count(self) -> int:
        """Get the count of all words"""
        return len(self.read_all())

    def is_duplicated(self, word: WordSample) -> bool:
        """Check if a world is already presented in current file"""
        for w in self.read_all():
            if w.word == word.word:
                return True
        return False

    def read_all(self) -> List[WordSample]:
        """Read all words from file

        :return: List of WordSample objects
        """
        words = []
        with open(self.file_path, 'r') as fp:
            for row in self._get_reader(fp):
                t, tran_t = row['例句/翻译'].split(' / ', 1)
                w = WordSample(
                    word=row['单词'],
                    word_meaning=row['释义'],
                    pronunciation=row['读音'],
                    orig_text=t,
                    translated_text=tran_t,
                )
                words.append(w)
        return words

    def find_known_words(self, text: str) -> List[str]:
        """Find out words already in record"""
        words = {s.group().lower() for s in re.finditer(r'[a-zA-Z]+', text)}
        all_words = {w.word for w in self.read_all()}
        return list(words & all_words)

    def _get_reader(self, fp: TextIO):
        """Get the CSV reader obj"""
        return csv.DictReader(fp, delimiter=",", quoting=csv.QUOTE_MINIMAL)

    def _get_writer(self, fp: TextIO):
        """Get the CSV writer obj"""
        return csv.writer(fp, delimiter=",", quoting=csv.QUOTE_MINIMAL)


def get_word_and_translation(text: str, known_words: List[str]) -> WordSample:
    """Get the most uncommon word in the given text, the result also include other
    information such as meaning of the word and etc.

    :param text: The text which needs to be translated
    :param known_words: Words already known
    :return: a `WordSample` object
    :raise VocBuilderError: when unable to finish the API call or reply is malformed
    """
    try:
        reply = query_openai(text, known_words)
    except Exception as e:
        raise VocBuilderError('Error querying OpenAI API: %s' % e)
    try:
        return parse_openai_reply(reply, text)
    except ValueError as e:
        raise VocBuilderError(e)


def parse_openai_reply(reply_text: str, orig_text: str) -> WordSample:
    """Parse the OpenAI reply into WorkSample

    :param reply_text: Formatted text
    :param orig_text: The original text which needs translation
    :return: WordSample object
    :raise: ValueError when the given reply text can not be parsed
    """
    d = {'word': None, 'meaning': None, 'pronunciation': None, 'translated': None}
    for line in reply_text.split('\n'):
        if ':' in line:
            key, value = line.split(':', 1)
            d[key.strip(' -')] = value.strip()

    if not all(d.values()):
        raise ValueError('Reply text "%s" is invalid' % reply_text)

    return WordSample(
        # The word was surrounded by {} sometimes
        word=d['word'].strip('{}').lower(),
        word_meaning=d['meaning'],
        pronunciation=d['pronunciation'],
        orig_text=orig_text,
        translated_text=d['translated'],
    )


# The prompt being used to make word
prompt_tmpl = dedent(
    '''
I will give you a sentence and a list of words called "known-words" which is divided
by ",", please find out the most uncommon word in the sentence(the word must not in "known-words"),
get the simplified Chinese meaning of that word, the pronunciation of that word
and translate the whole sentence into simplified Chinese.

Your answer should be separated into 4 different lines, each line's content is as below:

- word: {{word}}
- pronunciation: {{pronunciation}}
- meaning: {{chinese_meaning_of_word}}
- translated: {{translated_sentence}}

The answer should have no extra content.

known-words: {known_words}

The sentence is:

{text}
'''
)


def query_openai(text: str, known_words: List[str]) -> str:
    """Query OpenAI to get the translation results.

    :return: Well formatted string contains word and meaning
    """
    content = prompt_tmpl.format(text=text, known_words=','.join(known_words))
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": content},
        ],
    )
    logger.debug('Completion API returns: %s', completion)
    return completion.choices[0].message.content.strip()


@click.command()
@click.option('--api-key', envvar='OPENAI_API_KEY', required=True, help='Your OpenAI API key')
@click.option('--text', type=str, help='Text to be translated, interactive mode also supported')
@click.option('--log-level', type=str, default='INFO', help='Log level, change it to DEBUG to see more logs')
def main(api_key: str, text: str, log_level: str):
    # Set logging level
    logger.setLevel(getattr(logging, log_level.upper()))

    openai.api_key = api_key

    # Read text either from command line or stdin
    if text:
        write_new_one(text.strip())
        return
    elif not sys.stdin.isatty():
        text = sys.stdin.read().strip()
        write_new_one(text.strip())
        return

    # No text found, enter interactive mode
    console.print(
        Panel(
            dedent(
                f'''
    [bold]Guides[/bold]:
    - Input one sentence at a time, don't paste huge amounts of text
    - The vocabulary book can be found in [bold]{DEFAULT_CSV_FILE_PATH}[/bold]
    - Press Ctrl+c to quit'''
            ).strip(),
            title='Welcome to AI Vocabulary Builder!',
        )
    )

    while True:
        text = Prompt.ask('[blue]>[/blue] Enter text').strip()
        if not text.strip():

            continue
        write_new_one(text.strip())


if __name__ == '__main__':
    main()
