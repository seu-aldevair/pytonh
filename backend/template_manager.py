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
        # Initialize if it doesn't exist, though it should have been used first
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
    if report:
        report['filename'] = filename
    return report

def _get_templates_from_dir(directory):
    """Loads all templates from a specified directory."""
    templates = []
    if not os.path.exists(directory):
        return templates
    
    # Sort files to ensure consistent ordering for ADM templates
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
    
    human_adm_templates = all_human_templates[:NUM_ADM_TEMPLATES]
    human_templates = all_human_templates[NUM_ADM_TEMPLATES:]
    ai_templates = _get_templates_from_dir(AI_TEMPLATES_DIR)

    return {
        'human_adm': human_adm_templates,
        'human': human_templates,
        'ai': ai_templates
    }

def sanitize_filename(name):
    """Sanitizes a string to be used as a valid filename."""
    name = re.sub(r'[<>:"/\\|?*]', '', name)
    name = name.replace(' ', '_')
    # Basic accent removal
    name = re.sub(r'[áàâãä]', 'a', name, flags=re.IGNORECASE)
    name = re.sub(r'[éèêë]', 'e', name, flags=re.IGNORECASE)
    name = re.sub(r'[íìîï]', 'i', name, flags=re.IGNORECASE)
    name = re.sub(r'[óòôõö]', 'o', name, flags=re.IGNORECASE)
    name = re.sub(r'[úùûü]', 'u', name, flags=re.IGNORECASE)
    name = re.sub(r'ç', 'c', name, flags=re.IGNORECASE)
    return f"{name[:50]}.json" # Truncate for safety

def _save_template(directory, template_data, is_ai=False):
    """Saves a single template to the specified directory."""
    os.makedirs(directory, exist_ok=True)
    
    title = template_data.get('titulo', 'sem_titulo')
    base_filename = sanitize_filename(title)
    filename = base_filename
    filepath = os.path.join(directory, filename)
    
    # Handle potential filename conflicts
    counter = 1
    while os.path.exists(filepath):
        name, ext = os.path.splitext(base_filename)
        filename = f"{name}_{counter}{ext}"
        filepath = os.path.join(directory, filename)
        counter += 1

    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(template_data, f, ensure_ascii=False, indent=4)
        
    return filename # Return the actual saved filename

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
        raise PermissionError("Human ADM templates cannot be deleted.")

    if template_type == 'human':
        directory = HUMAN_TEMPLATES_DIR
    elif template_type == 'ai':
        directory = AI_TEMPLATES_DIR
    else:
        raise ValueError("Invalid template type specified.")

    filepath = os.path.join(directory, template_name)

    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Template '{template_name}' not found.")

    # Delete the file
    os.remove(filepath)

    # Remove from usage data
    data = _load_usage_data()
    if template_name in data:
        del data[template_name]
        _save_usage_data(data)

    return True