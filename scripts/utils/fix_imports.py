#!/usr/bin/env python3
"""
Fix all import paths in the project systematically
"""

import os
import re

def fix_imports_in_file(file_path):
    """Fix import statements in a single file"""
    print(f"🔧 Fixing imports in: {file_path}")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Fix common import patterns
        fixes = [
            # query_agent imports
            (r'from src.core.query_agent import', 'from src.core.query_agent import'),
            (r'from src.core.query_agent_enhanced import', 'from src.core.query_agent_enhanced import'),
            
            # sql imports
            (r'from src.core.sql import', 'from src.core.sql import'),
            
            # table mapper imports
            (r'from src.nlp.enhanced_table_mapper import', 'from src.nlp.enhanced_table_mapper import'),
            
            # embeddings imports
            (r'from src.nlp.create_lightweight_embeddings import', 'from src.nlp.create_lightweight_embeddings import'),
            (r'from src.nlp.sentence_embeddings import', 'from src.nlp.sentence_embeddings import'),
            
            # pronoun resolver imports
            (r'from src.nlp.enhanced_pronoun_resolver import', 'from src.nlp.enhanced_pronoun_resolver import'),
            
            # distance units imports
            (r'from src.database.distance_units import', 'from src.database.distance_units import'),
            
            # database reference parser imports
            (r'from src.database.database_reference_parser import', 'from src.database.database_reference_parser import'),
            
            # masker imports
            (r'from src.database.eoninfotech_masker import', 'from src.database.eoninfotech_masker import'),
            
            # intelligent reasoning imports
            (r'from src.core.intelligent_reasoning import', 'from src.core.intelligent_reasoning import'),
            
            # config imports
            (r'from src.core.config import', 'from src.core.config import'),
            
            # user manager imports
            (r'from src.core.user_manager import', 'from src.core.user_manager import'),
            
            # performance monitor imports
            (r'from src.core.performance_monitor import', 'from src.core.performance_monitor import'),
            
            # flask app imports
            (r'from src.api.flask_app import', 'from src.api.flask_app import'),
            (r'from src.api.app import', 'from src.api.app import'),
            (r'from src.api.llm_service import', 'from src.api.llm_service import'),
        ]
        
        # Apply fixes
        for pattern, replacement in fixes:
            content = re.sub(pattern, replacement, content)
        
        # Add sys.path.append if needed and not already present
        if ('from src.' in content or 'import src.') and 'sys.path.append' not in content:
            # Find where to insert the path
            lines = content.split('\n')
            insert_pos = 0
            
            # Find the position after initial comments and imports
            for i, line in enumerate(lines):
                if line.strip().startswith('#') or line.strip() == '' or line.strip().startswith('"""') or line.strip().startswith("'''"):
                    continue
                elif line.strip().startswith('import ') and not line.strip().startswith('import src'):
                    continue
                else:
                    insert_pos = i
                    break
            
            # Insert the path setup
            path_setup = [
                'import sys',
                "sys.path.append('/home/linux/Documents/chatbot-diya')",
                ''
            ]
            
            # Check if sys import already exists
            has_sys_import = any('import sys' in line for line in lines[:insert_pos + 5])
            if has_sys_import:
                path_setup = path_setup[1:]  # Skip the import sys line
            
            lines[insert_pos:insert_pos] = path_setup
            content = '\n'.join(lines)
        
        # Write back if changed
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"  ✅ Fixed imports in {file_path}")
            return True
        else:
            print(f"  ℹ️ No changes needed in {file_path}")
            return False
            
    except Exception as e:
        print(f"  ❌ Error fixing {file_path}: {e}")
        return False

def find_python_files():
    """Find all Python files in the project"""
    python_files = []
    
    for root, dirs, files in os.walk('/home/linux/Documents/chatbot-diya'):
        # Skip certain directories
        skip_dirs = {'.git', '__pycache__', '.pytest_cache', 'node_modules', '.venv', 'chatbot_env'}
        dirs[:] = [d for d in dirs if d not in skip_dirs]
        
        for file in files:
            if file.endswith('.py'):
                python_files.append(os.path.join(root, file))
    
    return python_files

def main():
    print("🔄 Fixing Import Paths Across Project")
    print("=" * 50)
    
    python_files = find_python_files()
    print(f"Found {len(python_files)} Python files")
    
    fixed_count = 0
    
    for file_path in python_files:
        if fix_imports_in_file(file_path):
            fixed_count += 1
    
    print(f"\n✅ Fixed imports in {fixed_count} files")
    print("🎉 Import path correction complete!")

if __name__ == "__main__":
    main()
