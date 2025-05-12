import re
import yaml

def load_config(config_file='config.yaml'):
    with open(config_file, 'r', encoding='utf-8') as file:
        config = yaml.safe_load(file)
    return config

def clean_blank(text):
    cleaned_text = re.sub(r'\s+', ' ', text.strip())
    return cleaned_text