import requests
from bs4 import BeautifulSoup


class Translator:

    def start(self):
        self.accept()
        req_obj_list = self.connect()
        for req_obj in req_obj_list:
            self.formatting(req_obj=req_obj)

    def __init__(self, src_lang=None, trans_lang=None, word=''):
        self.src_lang = src_lang
        self.trans_lang = trans_lang
        self.word = word
        self.lang_list = [
            'Arabic', 'German', 'English', 'Spanish',
            'French', 'Hebrew', 'Japanese', 'Dutch',
            'Polish', 'Portuguese', 'Romanian', 'Russian', 'Turkish'
        ]
        self.lang_ind = 0

    def accept(self):
        print("Hello, welcome to the translator. Translator supports: ")

        for no, lang in enumerate(self.lang_list):
            print(no+1, '. ', lang, sep='')
        src_lang = int(input('Type the number of your language: '))  # to be translated
        trans_lang = int(input('Type the number of language you want to translate to or "0" to translate to all languages:'))
        word = input('Type the word you want to translate:')
        if trans_lang != 0:
            self.__init__(src_lang=self.lang_list[src_lang-1], trans_lang=self.lang_list[trans_lang-1], word=word)
        else:
            self.__init__(src_lang=self.lang_list[src_lang-1], word=word)

    def url_gen(self):
        src_low = self.src_lang.lower()

        if self.trans_lang is not None:
            trans_lower = self.trans_lang.lower()
            return [f'https://context.reverso.net/translation/{src_low}-{trans_lower}/{self.word}', ]

        if self.trans_lang is None:
            url_list = []
            for trans_l in self.lang_list:
                if self.src_lang == trans_l:
                    continue
                else:
                    url = f'https://context.reverso.net/translation/{src_low}-{trans_l.lower()}/{self.word}'
                    url_list.append(url)
            return url_list

    def connect(self):
        user_agent = 'Mozilla/5.0'
        url_list = self.url_gen()
        req_obj_list = []
        for url in url_list:
            req_obj = requests.get(url, headers={'User-Agent': user_agent})
            req_obj_list.append(req_obj)

        return req_obj_list

    def parse(self, req_obj):
        parser = 'html.parser'
        data = req_obj.content
        soup = BeautifulSoup(data, parser)
        words = soup.find(id='translations-content').text.split()
        class_mod = 'trg rtl arabic' if self.lang_ind == 0 else 'trg ltr'
        examples = [x.text.strip() for x in soup.find_all(class_=['src ltr', class_mod])]
        return words, examples

    def formatting(self, req_obj):
        words, examples = self.parse(req_obj=req_obj)
        no_word = no_examples = 5
        final_lang = self.trans_lang

        if self.trans_lang is None:
            no_examples = no_word = 1
            final_lang = self.lang_list[self.lang_ind]

        if self.src_lang == self.lang_list[self.lang_ind - 1]:
            self.lang_ind += 1

        print(f'{final_lang} Translations:')
        print(*words[:no_word], sep='\n', end='\n\n')

        print(f'{final_lang} Examples:')
        i = 0
        for _ in range(no_examples):
            print(examples[i])
            print(examples[i+1], '\n')
            i += 2

        self.save_2_file(final_lang=final_lang, words=words, examples=examples, no_word=no_word)
        self.lang_ind += 1

    # under construction
    def save_2_file(self, final_lang, words, examples, no_word):
        file_name = self.word+'.txt'
        with open(file_name, 'a', encoding='utf-8') as file_out:
            file_out.write(f'{final_lang} Translations:\n')
            print(*words[:no_word], file=file_out, sep='\n', end='\n\n')

            file_out.write(f'{final_lang} Examples:\n')
            i = 0
            for _ in range(no_word):
                file_out.write(examples[i])
                file_out.write('\n')
                file_out.write(examples[i + 1])
                file_out.write('\n\n')
                i += 2
                file_out.write('\n')


if __name__ == '__main__':
    obj = Translator()
    obj.start()
