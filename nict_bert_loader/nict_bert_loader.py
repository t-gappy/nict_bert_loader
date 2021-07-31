import os
import subprocess
from .preprocess import download_nict_bert
from .juman_tokenizer import JumanTokenizer
from transformers import AutoConfig, AutoModel, BertJapaneseTokenizer

MODEL_TYPES = [
    "100K", 
    "32K_BPE"
]
CACHE_DIR = os.path.join(os.environ.get("HOME", "./"), ".cache", "nict_bert_loader")
MODEL_NAME_FORMAT = "NICT_BERT-base_JapaneseWikipedia_{}"


def load_nict_bert(model_type,
                   task=AutoModel,
                   config_file="config.json", 
                   weight_file="pytorch_model.bin", 
                   jumandic_path=None, 
                   mecabrc_path="/etc/mecabrc"):
    
    if model_type in MODEL_TYPES:
        model_name = MODEL_NAME_FORMAT.format(model_type)
        model_cache_dir = os.path.join(CACHE_DIR, model_name)
        
        if "BPE" in model_type:
            do_subword_tokenize = True
        else:
            do_subword_tokenize = False
        tokenizer_args = {
            "vocab_file": os.path.join(CACHE_DIR, model_name, "vocab.txt"),
            "word_tokenizer_type": "mecab",
            "do_subword_tokenize": do_subword_tokenize,
            "do_lower_case": False,
            "tokenize_chinese_chars": False,
        }        
        
        # initialize mecab with jumandic
        if jumandic_path is None:
            jumandic_path = subprocess.run(
                ["mecab-config", "--dicdir"], check=True, stdout=subprocess.PIPE, text=True
            ).stdout.rstrip() + "/jumandic/"
        if not os.path.exists(jumandic_path):
            msg = "jumandic is not installed in specified path: {}".format(jumandic_path)
            raise ValueError(msg)
        
        juman_tokenizer = JumanTokenizer(
            do_lower_case=tokenizer_args["do_lower_case"],
            dic_dir=jumandic_path, mecabrc=mecabrc_path
        )
        
        # download nict bert if not exists in local
        if not os.path.exists(model_cache_dir):
            download_nict_bert(CACHE_DIR, model_name)
        
        # make jumandic BertTokenizer by overwrite `wordtokenizer.mecab`
        tokenizer = BertJapaneseTokenizer(**tokenizer_args)
        tokenizer.word_tokenizer = juman_tokenizer
        
        config = AutoConfig.from_pretrained(os.path.join(model_cache_dir, config_file))
        model = task.from_pretrained(os.path.join(model_cache_dir, weight_file), config=config)
        return tokenizer, model
        
    else:
        msg = "model_type must be `100K` or `32K_BPE`."
        raise ValueError(msg)