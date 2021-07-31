import os
import MeCab
import mojimoji
import unicodedata
from typing import Optional

class JumanTokenizer:
    """almost copy-and-paste from MecabTokenizer in 
    https://huggingface.co/transformers/_modules/transformers/models/bert_japanese/tokenization_bert_japanese.html

    insted of using fugashi, JumanTokenzier use MeCab.
    """

    def __init__(
        self,
        do_lower_case=False,
        never_split=None,
        normalize_text=False,
        dic_dir: Optional[str] = None,
        mecabrc: Optional[str] = "/etc/mecabrc"
    ):
        self.do_lower_case = do_lower_case
        self.never_split = never_split if never_split is not None else []
        self.normalize_text = normalize_text
        
        if dic_dir is None:
            dic_dir = subprocess.run(
                ["mecab-config", "--dicdir"], check=True, stdout=subprocess.PIPE, text=True
            ).stdout.rstrip() + "/jumandic/"
        
        if not os.path.isdir(dic_dir):
            raise RuntimeError(
                "The jumandic dictionary itself is not found."
            )

        mecab_option = f'-d "{dic_dir}" -r "{mecabrc}" ' + "-Owakati"

        self.mecab = MeCab.Tagger(mecab_option)

    def tokenize(self, text, never_split=None, **kwargs):
        if self.normalize_text:
            text = unicodedata.normalize("NFKC", text)

        never_split = self.never_split + (never_split if never_split is not None else [])
        tokens = []
        
        text = mojimoji.han_to_zen(text).replace("\u3000", " ")
        for token in self.mecab.parse(text).rstrip("\n").split(" ")[:-1]:

            if self.do_lower_case and token not in never_split:
                token = token.lower()

            tokens.append(token)

        return tokens
    