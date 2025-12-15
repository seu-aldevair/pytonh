import json
import os
import re
from datetime import datetime

DATA_FILE = 'template_usage.json'
HUMAN_TEMPLATES_DIR = 'backend/human_templates'
AI_TEMPLATES_DIR = 'backend/ai_templates'
NUM_ADM_TEMPLATES = 10

def _load_usage_data():
    """Loads template usage data from the JSON file."""
    if not os.path.exists(DATA_FILE):
        return {}
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return {}

def _save_usage_data(data):
    """Saves template usage data to the JSON file."""
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)

def increment_template_usage(filename):
    """Increments the usage count for a given template."""
    data = _load_usage_data()
    template_info = data.get(filename, {
        'usage_count': 0,
        'last_used': None,
        'ai_analysis': []
    })
    template_info['usage_count'] += 1
    template_info['last_used'] = datetime.now().isoformat()
    data[filename] = template_info
    _save_usage_data(data)

def save_ai_analysis(filename, analysis_text):
    """Saves AI analysis text for a given template."""
    data = _load_usage_data()
    if filename not in data:
        data[filename] = {
            'usage_count': 0,
            'last_used': None,
            'ai_analysis': []
        }
    if 'ai_analysis' not in data[filename]:
        data[filename]['ai_analysis'] = []

    data[filename]['ai_analysis'].append(analysis_text)
    _save_usage_data(data)

def get_template_report(filename):
    """Retrieves usage report for a specific template."""
    data = _load_usage_data()
    report = data.get(filename)
    
    found_path = None
    for directory in [HUMAN_TEMPLATES_DIR, AI_TEMPLATES_DIR]:
        path = os.path.join(directory, filename)
        if os.path.exists(path):
            found_path = path
            break
            
    if found_path:
        try:
            with open(found_path, 'r', encoding='utf-8') as f:
                template_content = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            template_content = 'Erro ao ler o arquivo do template.'
    else:
        template_content = 'Arquivo do template não encontrado.'

    if report:
        report['filename'] = filename
        report['content'] = template_content.get('body', 'Conteúdo não disponível.')
    else:
        report = {
            'filename': filename,
            'usage_count': 0,
            'last_used': 'Nunca',
            'ai_analysis': [],
            'content': template_content.get('body', 'Conteúdo não disponível.') if isinstance(template_content, dict) else template_content
        }
        
    return report

def _get_templates_from_dir(directory):
    """Loads all templates from a specified directory."""
    templates = []
    if not os.path.exists(directory):
        return templates
    
    try:
        filenames = sorted(os.listdir(directory))
    except FileNotFoundError:
        return []

    for filename in filenames:
        if filename.endswith('.json'):
            filepath = os.path.join(directory, filename)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    template_data = json.load(f)
                    template_data['filename'] = filename
                    template_data['name'] = os.path.basename(filename)
                    templates.append(template_data)
            except (json.JSONDecodeError, UnicodeDecodeError):
                print(f"Warning: Could not decode or parse {filepath}. Skipping.")
                continue
    return templates

def get_all_templates():
    """
    Retrieves all templates, categorized into 'human_adm', 'human', and 'ai'.
    The first 10 templates from the human directory are considered 'human_adm'.
    """
    all_human_templates = _get_templates_from_dir(HUMAN_TEMPLATES_DIR)
    ai_templates = _get_templates_from_dir(AI_TEMPLATES_DIR)

    human_adm_templates = all_human_templates[:NUM_ADM_TEMPLATES]
    human_templates = all_human_templates[NUM_ADM_TEMPLATES:]

    return {
        'human_adm': human_adm_templates,
        'human': human_templates,
        'ai': ai_templates
    }

def sanitize_filename(name):
    """Sanitizes a string to be used as a valid filename."""
    name = re.sub(r'[<>:\"/\\|?*]', '', name)
    name = name.replace(' ', '_')
    name = re.sub(r'[áàâãä]', 'a', name, flags=re.IGNORECASE)
    name = re.sub(r'[éèêë]', 'e', name, flags=re.IGNORECASE)
    name = re.sub(r'[íìîï]', 'i', name, flags=re.IGNORECASE)
    name = re.sub(r'[óòôõö]', 'o', name, flags=re.IGNORECASE)
    name = re.sub(r'[úùûü]', 'u', name, flags=re.IGNORECASE)
    name = re.sub(r'ç', 'c', name, flags=re.IGNORECASE)
    return f"{name[:50]}.json"

def _save_template(directory, template_data, is_ai=False):
    """Saves a single template to the specified directory."""
    os.makedirs(directory, exist_ok=True)
    
    title = template_data.get('title') or template_data.get('name', 'sem_titulo')
    base_filename = sanitize_filename(title)
    filename = base_filename
    filepath = os.path.join(directory, filename)
    
    counter = 1
    while os.path.exists(filepath):
        name, ext = os.path.splitext(base_filename)
        filename = f"{name}_{counter}{ext}"
        filepath = os.path.join(directory, filename)
        counter += 1

    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(template_data, f, ensure_ascii=False, indent=4)
        
    return filename

def save_human_template(template_data):
    """Saves a human-created template."""
    return _save_template(HUMAN_TEMPLATES_DIR, template_data)

def save_ai_template(template_data):
    """Saves an AI-generated template."""
    return _save_template(AI_TEMPLATES_DIR, template_data, is_ai=True)

def delete_template(template_type, template_name):
    """
    Deletes a template file and its associated usage data.
    Prevents deletion of 'human_adm' templates.
    """
    if template_type == 'human_adm':
        # Allow deletion for simplicity now, can be changed back
        directory = HUMAN_TEMPLATES_DIR
    elif template_type == 'human':
        directory = HUMAN_TEMPLATES_DIR
    elif template_type == 'ai':
        directory = AI_TEMPLATES_DIR
    else:
        raise ValueError("Invalid template type specified.")

    filepath = os.path.join(directory, template_name)

    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Template '{template_name}' not found.")

    os.remove(filepath)

    data = _load_usage_data()
    if template_name in data:
        del data[template_name]
        _save_usage_data(data)

    return True