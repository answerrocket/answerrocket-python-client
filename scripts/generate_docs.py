#!/usr/bin/env python3
"""
Generate markdown documentation from Python modules for GitHub Wiki.
"""

import ast
import inspect
import importlib
import os
import sys
from pathlib import Path
from typing import List, Tuple, get_type_hints, Any, Set
import re

# SDK types that should be linked to API-Types.md
SDK_TYPES = {
    'MaxResult', 'ExecuteSqlQueryResult', 'DomainObjectResult', 'RunMaxSqlGenResult',
    'RunSqlAiResult', 'RunSkillResult', 'AsyncSkillRunResult', 'ChatLoadingInfo',
    'ContentBlock', 'ChatReportOutput', 'LlmChatMessage', 'LlmFunctionProperty',
    'LlmFunctionParameters', 'LlmFunction', 'ClientConfig', 'FeedbackType',
    'QuestionType', 'ThreadType', 'MaxChatEntry', 'MaxChatThread', 'MaxChatUser',
    'SharedThread', 'ChatArtifact', 'PagedChatArtifacts', 'EvaluateChatQuestionResponse',
    'MaxMutationResponse'
}


def link_type_references(text: str) -> str:
    """
    Convert type names to markdown links pointing to API-Types.md.

    Examples:
    - MaxChatEntry -> [MaxChatEntry](API-Types#maxchatentry)
    - list[MaxChatEntry] -> list[[MaxChatEntry](API-Types#maxchatentry)]
    """
    for type_name in SDK_TYPES:
        # GitHub Wiki auto-generates anchors from headings (lowercase)
        # Use [Display Text](Page-Name#anchor) format for direct navigation
        anchor = type_name.lower()
        link = f"[{type_name}](API-Types#{anchor})"

        # Replace standalone type name (not part of another word)
        # Use word boundaries but also handle cases like `Type` or `Type,`
        pattern = r'\b' + re.escape(type_name) + r'\b'
        text = re.sub(pattern, link, text)

    return text


def format_numpy_params(section_text: str, is_returns: bool = False) -> str:
    """
    Convert NumPy-style parameter/returns section to clean markdown.

    For parameters (is_returns=False), converts:
        param_name : type
            Description here.
    To:
        - **param_name** (`type`): Description here.

    For returns (is_returns=True), converts:
        type
            Description here.
    To:
        `type` - Description here.
    """
    lines = section_text.split('\n')
    result = []
    current_param = None
    current_type = None
    current_desc_lines = []

    for line in lines:
        stripped = line.strip()

        # Check if this is a parameter definition line (contains " : ")
        if ' : ' in line and not line.startswith(' '):
            # Save previous parameter if any
            if current_param:
                desc = ' '.join(current_desc_lines).strip()
                optional_note = ', optional' if 'optional' in current_type.lower() else ''
                type_clean = current_type.replace(', optional', '').replace(' optional', '').strip()
                # Link type references in the type and description
                linked_type = link_type_references(type_clean)
                linked_desc = link_type_references(desc)
                result.append(f"- **{current_param}** ({linked_type}{optional_note}): {linked_desc}")

            # Parse new parameter
            param_part, type_part = stripped.split(' : ', 1)
            current_param = param_part.strip()
            current_type = type_part.strip()
            current_desc_lines = []
        elif current_param and stripped:
            # This is part of the description
            current_desc_lines.append(stripped)
        elif not stripped and current_param:
            # Blank line - might be between parameters
            pass
        elif is_returns and not current_param and stripped and not line.startswith(' '):
            # For Returns section: first non-indented line is the type
            current_param = "return_type"  # Placeholder
            current_type = stripped
            current_desc_lines = []
        elif is_returns and current_param and stripped:
            # For Returns section: indented lines are description
            current_desc_lines.append(stripped)

    # Save last parameter
    if current_param:
        desc = ' '.join(current_desc_lines).strip()
        if is_returns:
            # Format for returns: type - description (no backticks around linked types)
            # Link type references in the type and description
            linked_type = link_type_references(current_type)
            linked_desc = link_type_references(desc)
            result.append(f"{linked_type} - {linked_desc}" if linked_desc else f"{linked_type}")
        else:
            optional_note = ', optional' if 'optional' in current_type.lower() else ''
            type_clean = current_type.replace(', optional', '').replace(' optional', '').strip()
            # Link type references in the type and description
            linked_type = link_type_references(type_clean)
            linked_desc = link_type_references(desc)
            result.append(f"- **{current_param}** ({linked_type}{optional_note}): {linked_desc}")

    return '\n'.join(result) if result else section_text


def parse_sphinx_params(text: str) -> str:
    """
    Parse Sphinx-style :param lines and convert to markdown.

    Converts:
        :param name: description
        :param type name: description
    To:
        - **name**: description
    """
    lines = text.split('\n')
    result = []

    for line in lines:
        stripped = line.strip()

        # Check if this is a :param line
        if stripped.startswith(':param '):
            # Extract param name and description
            # Format: :param name: description or :param type name: description
            param_part = stripped[7:]  # Remove ':param '

            if ':' in param_part:
                name_part, desc = param_part.split(':', 1)
                name_part = name_part.strip()
                desc = desc.strip()

                # Handle ":param type name:" format - extract just the name
                name_parts = name_part.split()
                if len(name_parts) > 1:
                    param_name = name_parts[-1]  # Last word is the actual param name
                else:
                    param_name = name_part

                # Format as markdown list item
                result.append(f"- **{param_name}**: {desc}")
            else:
                # Malformed :param line, keep as-is
                result.append(line)
        elif stripped.startswith(':return:'):
            # Skip :return: lines - we handle returns separately
            continue
        else:
            result.append(line)

    return '\n'.join(result)


def parse_docstring(docstring: str) -> Tuple[str, dict]:
    """
    Parse NumPy-style docstring into description and sections.

    Returns
    -------
    tuple
        (description, sections_dict)
    """
    if not docstring:
        return "", {}

    lines = docstring.strip().split('\n')
    description_lines = []
    sections = {}
    current_section = None
    current_content = []
    prev_line = None

    for i, line in enumerate(lines):
        stripped = line.strip()

        # Check if this is a section header (all dashes under text)
        if stripped and all(c == '-' for c in stripped) and len(stripped) >= 3:
            # The previous line is the section name
            if prev_line and prev_line.strip():
                new_section_name = prev_line.strip()

                # Save previous section if any, removing the new section name from its content
                if current_section and current_content:
                    # Remove the new section name if it's the last line in current content
                    if current_content and current_content[-1].strip() == new_section_name:
                        current_content.pop()
                    sections[current_section] = '\n'.join(current_content)
                    current_content = []

                # Start new section
                current_section = new_section_name

                # Remove the section name from description if it's there
                if description_lines and description_lines[-1].strip() == current_section:
                    description_lines.pop()
                # Don't add the dashes line to anything (it's handled here)
        elif current_section:
            # We're inside a section, collect content
            current_content.append(line)
        else:
            # Part of description - but skip if this might be a section header
            # (we'll know for sure on the next iteration)
            description_lines.append(line)

        prev_line = line

    # Save last section
    if current_section and current_content:
        sections[current_section] = '\n'.join(current_content)

    # Clean up description - remove any standalone section names that snuck in
    cleaned_desc_lines = []
    skip_next_blank = False

    for i, line in enumerate(description_lines):
        stripped = line.strip()

        # Skip lines that are just section names
        if stripped in sections.keys():
            skip_next_blank = True  # Also skip blank lines after section names
            continue

        # Skip blank line immediately after a section name
        if skip_next_blank and not stripped:
            skip_next_blank = False
            continue

        skip_next_blank = False
        cleaned_desc_lines.append(line)

    description = '\n'.join(cleaned_desc_lines).strip()
    return description, sections


def format_type_annotation(annotation) -> str:
    """Format a type annotation for display."""
    if annotation is None or annotation == inspect.Parameter.empty:
        return ""

    # Convert annotation to string
    if hasattr(annotation, '__name__'):
        return annotation.__name__

    ann_str = str(annotation)

    # Clean up common type representations
    ann_str = ann_str.replace('typing.', '')
    ann_str = ann_str.replace('<class \'', '').replace('\'>', '')
    ann_str = ann_str.replace('answer_rocket.', '')
    ann_str = ann_str.replace('pandas.core.frame.', '')

    return ann_str


def ast_annotation_to_string(annotation) -> str:
    """Convert AST annotation to string."""
    if annotation is None:
        return ""

    if isinstance(annotation, ast.Name):
        return annotation.id
    elif isinstance(annotation, ast.Constant):
        # Preserve quotes for string literals
        if isinstance(annotation.value, str):
            return repr(annotation.value)
        return str(annotation.value)
    elif isinstance(annotation, ast.Attribute):
        value = ast_annotation_to_string(annotation.value)
        return f"{value}.{annotation.attr}" if value else annotation.attr
    elif isinstance(annotation, ast.Subscript):
        value = ast_annotation_to_string(annotation.value)
        slice_str = ast_annotation_to_string(annotation.slice)
        return f"{value}[{slice_str}]"
    elif isinstance(annotation, ast.Tuple):
        elements = [ast_annotation_to_string(e) for e in annotation.elts]
        return f"({', '.join(elements)})"
    elif isinstance(annotation, ast.BinOp) and isinstance(annotation.op, ast.BitOr):
        left = ast_annotation_to_string(annotation.left)
        right = ast_annotation_to_string(annotation.right)
        return f"{left} | {right}"
    else:
        try:
            return ast.unparse(annotation) if hasattr(ast, 'unparse') else ""
        except:
            return ""


def get_function_signature_with_types(func_obj: Any) -> dict:
    """Extract function signature with type annotations."""
    try:
        sig = inspect.signature(func_obj)
        params = []
        return_type = ""

        for param_name, param in sig.parameters.items():
            param_info = {'name': param_name}

            # Get type annotation
            if param.annotation != inspect.Parameter.empty:
                param_info['type'] = format_type_annotation(param.annotation)

            # Get default value
            if param.default != inspect.Parameter.empty:
                param_info['default'] = repr(param.default)

            params.append(param_info)

        # Get return type
        if sig.return_annotation != inspect.Signature.empty:
            return_type = format_type_annotation(sig.return_annotation)

        return {'params': params, 'return_type': return_type}
    except Exception:
        return {'params': [], 'return_type': ''}


def get_module_docs(module_path: Path, module_obj: Any = None) -> dict:
    """Extract documentation from a Python module file with runtime type info."""
    with open(module_path, 'r', encoding='utf-8') as f:
        source_code = f.read()
        tree = ast.parse(source_code)

    module_doc = ast.get_docstring(tree) or ""
    classes = []
    functions = []
    constants = []
    type_aliases = []

    # Extract module-level constants and type aliases
    for node in tree.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    var_name = target.id

                    # Check if it's a constant (ALL_CAPS)
                    if var_name.isupper():
                        const_value = None
                        # Try to get the value
                        if isinstance(node.value, ast.Constant):
                            const_value = node.value.value
                        elif isinstance(node.value, ast.Num):  # For older Python versions
                            const_value = node.value.n
                        elif isinstance(node.value, ast.Str):  # For older Python versions
                            const_value = node.value.s
                        constants.append({'name': var_name, 'value': const_value})

                    # Check if it's a type alias (PascalCase ending with 'Type' or has Subscript like Literal[...])
                    elif var_name[0].isupper() and (var_name.endswith('Type') or isinstance(node.value, ast.Subscript)):
                        # Extract the type definition
                        type_def = ast_annotation_to_string(node.value)
                        type_aliases.append({'name': var_name, 'definition': type_def})

    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            class_doc = ast.get_docstring(node) or ""

            # Try to get runtime class object for type hints
            class_obj = None
            if module_obj:
                try:
                    class_obj = getattr(module_obj, node.name, None)
                except Exception:
                    pass

            # Extract class attributes from AST (for dataclasses and annotated vars)
            attributes = []

            # First try runtime dataclass fields
            if class_obj and hasattr(class_obj, '__dataclass_fields__'):
                for field_name, field in class_obj.__dataclass_fields__.items():
                    attr_type = format_type_annotation(field.type)
                    attributes.append({'name': field_name, 'type': attr_type})
            else:
                # Fall back to AST parsing for annotated assignments
                for item in node.body:
                    if isinstance(item, ast.AnnAssign) and isinstance(item.target, ast.Name):
                        attr_name = item.target.id
                        attr_type = ast_annotation_to_string(item.annotation)
                        attributes.append({'name': attr_name, 'type': attr_type})

            methods = []
            for item in node.body:
                if isinstance(item, ast.FunctionDef):
                    method_doc = ast.get_docstring(item) or ""

                    # Get method object for type hints
                    method_obj = None
                    if class_obj:
                        try:
                            method_obj = getattr(class_obj, item.name, None)
                        except Exception:
                            pass

                    # Get signature with types - try runtime first, then AST
                    sig_info = {}
                    if method_obj and callable(method_obj):
                        sig_info = get_function_signature_with_types(method_obj)
                    else:
                        # Extract from AST
                        params = []
                        for arg in item.args.args:
                            param_info = {'name': arg.arg}
                            if arg.annotation:
                                param_info['type'] = ast_annotation_to_string(arg.annotation)
                            params.append(param_info)

                        return_type = ""
                        if item.returns:
                            return_type = ast_annotation_to_string(item.returns)

                        sig_info = {'params': params, 'return_type': return_type}

                    methods.append({
                        'name': item.name,
                        'doc': method_doc,
                        'signature': sig_info
                    })

            classes.append({
                'name': node.name,
                'doc': class_doc,
                'methods': methods,
                'attributes': attributes
            })
        elif isinstance(node, ast.FunctionDef) and node.col_offset == 0:
            # Top-level function
            func_doc = ast.get_docstring(node) or ""

            # Get function object for type hints
            func_obj = None
            if module_obj:
                try:
                    func_obj = getattr(module_obj, node.name, None)
                except Exception:
                    pass

            # Get signature with types - try runtime first, then AST
            sig_info = {}
            if func_obj and callable(func_obj):
                sig_info = get_function_signature_with_types(func_obj)
            else:
                # Extract from AST
                params = []
                for arg in node.args.args:
                    param_info = {'name': arg.arg}
                    if arg.annotation:
                        param_info['type'] = ast_annotation_to_string(arg.annotation)
                    params.append(param_info)

                return_type = ""
                if node.returns:
                    return_type = ast_annotation_to_string(node.returns)

                sig_info = {'params': params, 'return_type': return_type}

            functions.append({
                'name': node.name,
                'doc': func_doc,
                'signature': sig_info
            })

    return {
        'module_doc': module_doc,
        'classes': classes,
        'functions': functions,
        'constants': constants,
        'type_aliases': type_aliases
    }


def generate_markdown(module_name: str, docs: dict) -> str:
    """Generate markdown documentation from extracted docs."""
    md = []

    # Module header
    md.append(f"# {module_name}\n")

    # Module docstring
    if docs['module_doc']:
        desc, sections = parse_docstring(docs['module_doc'])
        if desc:
            md.append(f"{desc}\n")

    # Constants (if any)
    if docs.get('constants'):
        md.append("## Constants\n")
        for const in docs['constants']:
            const_value = f" = `{const['value']}`" if const.get('value') is not None else ""
            md.append(f"- **{const['name']}**{const_value}\n")
        md.append("\n")

    # Classes
    if docs['classes']:
        md.append("## Classes\n")
        for cls in docs['classes']:
            md.append(f"### `{cls['name']}`\n")
            desc = ""
            sections = {}
            if cls['doc']:
                desc, sections = parse_docstring(cls['doc'])
                if desc:
                    md.append(f"{desc}\n")

            # Show attributes for dataclasses (if any were found)
            if cls.get('attributes'):
                md.append("\n**Attributes:**\n")

                # If there's an Attributes section in the docstring, parse it for descriptions
                attr_descriptions = {}
                if 'Attributes' in sections and sections['Attributes'].strip():
                    # Parse the Attributes section to extract descriptions
                    formatted_attrs = format_numpy_params(sections['Attributes'])
                    md.append(formatted_attrs + "\n")
                else:
                    # Fall back to just listing attributes without descriptions
                    for attr in cls['attributes']:
                        attr_type = f" : `{attr['type']}`" if attr.get('type') else ""
                        md.append(f"- **{attr['name']}**{attr_type}\n")

            # Methods
            if cls['methods']:
                md.append("#### Methods\n")
                for method in cls['methods']:
                    if method['name'].startswith('_') and method['name'] != '__init__':
                        continue  # Skip private methods

                    # Skip methods with TODO in docstring (temporary/internal methods)
                    if method['doc'] and 'TODO:' in method['doc']:
                        continue

                    # Build method signature with types
                    sig_info = method.get('signature', {})
                    params = sig_info.get('params', [])

                    # Format parameters with types
                    param_strs = []
                    for param in params:
                        param_str = param['name']
                        if param.get('type'):
                            # Link type references in parameter types
                            linked_type = link_type_references(param['type'])
                            param_str += f": {linked_type}"
                        if param.get('default'):
                            param_str += f" = {param['default']}"
                        param_strs.append(param_str)

                    args_str = ', '.join(param_strs)
                    return_type = sig_info.get('return_type', '')
                    # Link type references in return type
                    return_str = f" -> {link_type_references(return_type)}" if return_type else ""

                    md.append(f"##### `{method['name']}({args_str}){return_str}`\n")

                    if method['doc']:
                        desc, sections = parse_docstring(method['doc'])
                        if desc:
                            # Parse Sphinx-style :param lines and convert to markdown
                            desc = parse_sphinx_params(desc)

                            if desc.strip():
                                md.append(f"\n{desc}\n")

                        # Parameters
                        if 'Parameters' in sections and sections['Parameters'].strip():
                            md.append("\n**Parameters:**\n")
                            formatted_params = format_numpy_params(sections['Parameters'])
                            md.append(formatted_params + "\n")

                        # Returns
                        if 'Returns' in sections and sections['Returns'].strip():
                            md.append("\n**Returns:**\n")
                            formatted_returns = format_numpy_params(sections['Returns'], is_returns=True)
                            md.append(formatted_returns + "\n")

    # Functions
    if docs['functions']:
        md.append("## Functions\n")
        for func in docs['functions']:
            if func['name'].startswith('_'):
                continue  # Skip private functions

            # Skip functions with TODO in docstring (temporary/internal functions)
            if func['doc'] and 'TODO:' in func['doc']:
                continue

            # Build function signature with types
            sig_info = func.get('signature', {})
            params = sig_info.get('params', [])

            # Format parameters with types
            param_strs = []
            for param in params:
                param_str = param['name']
                if param.get('type'):
                    # Link type references in parameter types
                    linked_type = link_type_references(param['type'])
                    param_str += f": {linked_type}"
                if param.get('default'):
                    param_str += f" = {param['default']}"
                param_strs.append(param_str)

            args_str = ', '.join(param_strs)
            return_type = sig_info.get('return_type', '')
            # Link type references in return type
            return_str = f" -> {link_type_references(return_type)}" if return_type else ""

            md.append(f"### `{func['name']}({args_str}){return_str}`\n")

            if func['doc']:
                desc, sections = parse_docstring(func['doc'])
                if desc:
                    # Parse Sphinx-style :param lines and convert to markdown
                    desc = parse_sphinx_params(desc)

                    if desc.strip():
                        md.append(f"\n{desc}\n")

                # Parameters
                if 'Parameters' in sections and sections['Parameters'].strip():
                    md.append("\n**Parameters:**\n")
                    formatted_params = format_numpy_params(sections['Parameters'])
                    md.append(formatted_params + "\n")

                # Returns
                if 'Returns' in sections and sections['Returns'].strip():
                    md.append("\n**Returns:**\n")
                    formatted_returns = format_numpy_params(sections['Returns'], is_returns=True)
                    md.append(formatted_returns + "\n")

    return '\n'.join(md)


def generate_types_documentation(base_path: Path, wiki_path: Path) -> None:
    """Generate comprehensive types documentation from all modules."""
    answer_rocket_path = base_path / 'answer_rocket'

    # Modules that contain type definitions
    modules_with_types = ['types', 'data', 'skill', 'output', 'llm', 'client_config', 'chat']

    all_constants = []
    all_type_classes = []
    all_type_aliases = []

    for module_name in modules_with_types:
        module_path = answer_rocket_path / f'{module_name}.py'
        if not module_path.exists():
            continue

        try:
            module_obj = None
            try:
                module_obj = importlib.import_module(f'answer_rocket.{module_name}')
            except Exception:
                pass

            docs = get_module_docs(module_path, module_obj)

            # Collect constants
            for const in docs.get('constants', []):
                all_constants.append({
                    'module': module_name,
                    'name': const['name'],
                    'value': const.get('value')
                })

            # Collect type aliases
            for alias in docs.get('type_aliases', []):
                all_type_aliases.append({
                    'module': module_name,
                    'name': alias['name'],
                    'definition': alias.get('definition')
                })

            # Collect type classes (dataclasses and TypedDicts)
            for cls in docs.get('classes', []):
                # Check if it's a dataclass or TypedDict
                class_doc = cls.get('doc', '')
                is_type_class = False

                # Check if it has attributes (dataclasses/TypedDicts usually do)
                if cls.get('attributes'):
                    is_type_class = True

                # Also check if it's a result class or TypedDict
                if cls['name'].endswith('Result') or 'TypedDict' in class_doc or '@dataclass' in str(module_obj):
                    is_type_class = True

                if is_type_class:
                    all_type_classes.append({
                        'module': module_name,
                        'name': cls['name'],
                        'doc': cls['doc'],
                        'attributes': cls.get('attributes', [])
                    })

        except Exception as e:
            print(f"  ⚠ Warning: Error collecting types from {module_name}: {e}")

    # Generate markdown
    md = []
    md.append("# answer_rocket.types\n")
    md.append("Type definitions, result classes, and constants used throughout the AnswerRocket SDK.\n")

    # Constants section
    if all_constants:
        md.append("## Constants\n")
        for const in all_constants:
            const_value = f" = `{const['value']}`" if const.get('value') is not None else ""
            md.append(f"- **{const['name']}**{const_value} (from `{const['module']}`)\n")
        md.append("\n")

    # Type aliases section
    if all_type_aliases:
        md.append("## Type Aliases\n")
        for alias in all_type_aliases:
            md.append(f"### `{alias['name']}`\n")
            md.append(f"*Defined in `answer_rocket.{alias['module']}`*\n\n")
            md.append(f"```python\n{alias['name']} = {alias['definition']}\n```\n\n")

    # Type classes section
    if all_type_classes:
        md.append("## Type Classes\n")
        for cls in all_type_classes:
            md.append(f"### `{cls['name']}`\n")
            md.append(f"*Defined in `answer_rocket.{cls['module']}`*\n")

            if cls['doc']:
                desc, sections = parse_docstring(cls['doc'])
                if desc:
                    md.append(f"\n{desc}\n")

                # Handle attributes from docstring
                if cls.get('attributes'):
                    md.append("\n**Attributes:**\n")
                    if 'Attributes' in sections and sections['Attributes'].strip():
                        formatted_attrs = format_numpy_params(sections['Attributes'])
                        md.append(formatted_attrs + "\n")
                    else:
                        for attr in cls['attributes']:
                            attr_type = f" : `{attr['type']}`" if attr.get('type') else ""
                            md.append(f"- **{attr['name']}**{attr_type}\n")

    # Write to wiki
    output_file = wiki_path / "API-Types.md"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(md))

    print(f"  ✓ Created {output_file.name} with {len(all_type_classes)} type classes, {len(all_type_aliases)} type aliases, and {len(all_constants)} constants")


def main():
    """Generate documentation for all answer_rocket modules."""
    base_path = Path(__file__).parent.parent
    answer_rocket_path = base_path / 'answer_rocket'
    wiki_path = base_path / 'wiki'

    # Add parent directory to path to import answer_rocket
    sys.path.insert(0, str(base_path))

    # Create wiki directory
    wiki_path.mkdir(exist_ok=True)

    # Find all Python modules (excluding internal/implementation modules)
    modules_to_document = [
        'client',
        'data',
        'chat',
        'config',
        'skill',
        'llm',
        'output',
        # 'types',  # Will be handled separately with comprehensive type collection
        # 'auth',  # Internal authentication implementation - not for external use
        # 'error',  # Simple exception class - minimal documentation value
    ]

    for module_name in modules_to_document:
        module_path = answer_rocket_path / f'{module_name}.py'
        if not module_path.exists():
            continue

        print(f"Generating documentation for {module_name}...")

        try:
            # Import the module to get runtime type information
            module_obj = None
            try:
                module_obj = importlib.import_module(f'answer_rocket.{module_name}')
            except Exception as e:
                print(f"  ⚠ Warning: Could not import module for type hints: {e}")

            docs = get_module_docs(module_path, module_obj)
            markdown = generate_markdown(f"answer_rocket.{module_name}", docs)

            # Write to wiki
            output_file = wiki_path / f"API-{module_name.title()}.md"
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(markdown)

            print(f"  ✓ Created {output_file.name}")
        except Exception as e:
            print(f"  ✗ Error processing {module_name}: {e}")
            import traceback
            traceback.print_exc()

    # Generate comprehensive types documentation
    print("\nGenerating comprehensive types documentation...")
    try:
        generate_types_documentation(base_path, wiki_path)
    except Exception as e:
        print(f"  ✗ Error generating types documentation: {e}")
        import traceback
        traceback.print_exc()

    print("\nDocumentation generation complete!")
    print(f"Files created in: {wiki_path}")


if __name__ == '__main__':
    main()
