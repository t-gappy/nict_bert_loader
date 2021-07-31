# NICT BERT LOADER
Loading [NICT BERT](https://alaginrc.nict.go.jp/nict-bert/index.html) in Huggingface Transformers style. <br>

## requirements / dev-env
- cui
    - wget
    - mecab
    - mecab-jumandic (see instruction below)
- python
    - transformers==4.9.0
    - mecab-python3==1.0.4
    - mojimoji==0.0.11

## installing mecab-jumandic
- install from mecab-jumandic via apt causes error.
- you should manually install.
    - you can use `script/install_jumandic.sh`

```bash
$ bash install_jumandic.sh
```

## how to use
- 1) move this repo to working directory

```bash
cd /path/to/this/repo
cp -r ./nict_bert_loader /path/to/working/directory/
```

- 2) import `load_nict_bert` function.

```python
from nict_bert_loader import load_nict_bert

tokenizer, model = load_nict_bert("32K_BPE")
```

### args of load_nict_bert
- model_type [str]: specify `32K_BPE` or `100K`.
- task [class]: class of transformers task like `BertForQuestionAnswering`. default is `AutoModel`.
- config_file [str]: name of config file, default is `config.json`. 
- weight_file [str]: name of weight file, default is `pytorch_model.bin`, 
- jumandic_path [str]: path to jumandic. default is `None` (auto detect by `mecab-config --dicdir`). 
- mecabrc_path [str]: path to mecabrc. default is `/etc/mecabrc`.