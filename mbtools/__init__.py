import re
from decimal import Decimal
import subprocess, os, platform
from glob import glob

# ------------------------
# System Operational Utils
# ------------------------

def open_file(file):
    # Ref: https://stackoverflow.com/questions/434597/open-document-with-default-application-in-python
    if platform.system() == 'Darwin':  # macOS
        subprocess.call(('open', file))
    elif platform.system() == 'Windows':  # Windows
        os.startfile(file)
    else:  # linux variants
        subprocess.call(('xdg-open', file))

def get_files(start_dir, pattern):
    files = []
    # start_dir = os.getcwd()
    # pattern   = "*.log"

    for dir,_,_ in os.walk(start_dir):
        files.extend(glob(os.path.join(dir,pattern)))

    return files



# ------------
# String Utils
# ------------
def describe_obj(obj, attributes_to_not_describe=[]) -> str:
    if obj.__dict__:
        atts = ", \n".join([u" = ".join(['\t{} ({})'.format(key, type(val)), '{}'.format(str(val))]) for key, val in
                            obj.__dict__.items() if key not in attributes_to_not_describe])
        return '{} (\n{}\n)'.format(obj.__class__.__name__, atts)
    return ''

def convert_text_to_decimal(text):
    text_number = text.replace('.', '').replace(',', '.')
    return Decimal(text_number)

def extract_text_numbers_from_text(text):
    return re.findall("\d+\d*[.,]?\d+", text)

def extract_decimal_or_int_from_text(text):
    text_numbers = re.findall("-?\d+\d*[.,]-?\d+", text)
    decimals_or_ints = []
    for tn in text_numbers:
        tn = tn.replace('.', '').replace(',', '.')
        if '.' in tn:
            decimals_or_ints.append(Decimal(tn))
        else:
            decimals_or_ints.append(int(tn))

    if decimals_or_ints and len(decimals_or_ints)==1:
        return decimals_or_ints[0]
    else:
        return decimals_or_ints

def remove_all_occurrences(text, *args):
    for arg in args:
        text = re.sub('{}+'.format(arg), '', text)
    return text

def remove_multiple_spaces(text):
    return re.sub(' +', ' ', text).strip()

def remove_multiple_spaces_and_line_breaks(text):
    # Other option: ' '.join(text.split())
    return re.sub(r'\s+', ' ', text).strip()

def remove_all_spaces_and_line_breaks(text):
    # Ref: https://stackoverflow.com/questions/8270092/remove-all-whitespace-in-a-string-in-python
    return re.sub(r'\s+', '', text)

def extract_variables(text_with_variables, text_with_values):
    '''
    Extract variables and your values from two strings:

    extrair_variaveis(text_with_variables='Fone: {{ unidade_telefone }}, Setor {{ setor_nome }}',
                      text_with_values='Fone: (84) 4006-9500, Setor TI')

    O resultado será o seguinte: {'unidade_telefone': '(84) 4006-9500', 'setor_nome': 'TI'}

    :param text_with_variables:
    :param text_with_values:
    :return: a dictionary
    '''
    p = re.compile('{{ (.*?) }}')
    variables = p.findall(text_with_variables)

    text_with_variables_to_match = text_with_variables
    for v in variables:
        text_with_variables_to_match = text_with_variables_to_match.replace('{{ '+v+' }}', '(.*)')

    try:
        m = re.match(text_with_variables_to_match, text_with_values)
        valores = m.groups()
    except Exception as e:
        print(text_with_variables)
        print(text_with_values)
        raise e

    result = dict()
    if len(variables) == len(valores):
        for i in range(len(variables)):
            result[variables[i]] = valores[i]

    return result