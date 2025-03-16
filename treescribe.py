#!/usr/bin/env python3

import os
import fnmatch
import argparse

def read_ignore_file(ignore_file_path):
    """Read and parse the .ignore file to collect ignore patterns, ignoring comments."""
    ignore_patterns = []
    if not os.path.exists(ignore_file_path):
        return ignore_patterns
    with open(ignore_file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            pattern = line.split('#', 1)[0].strip()
            if pattern:
                ignore_patterns.append(pattern)
    return ignore_patterns

def match_ignore_patterns(path, ignore_patterns):
    """Check if the given path matches any ignore patterns."""
    for pattern in ignore_patterns:
        if pattern.endswith('/'):
            if os.path.isdir(path) and fnmatch.fnmatch(os.path.basename(path), pattern[:-1]):
                return True
        else:
            if fnmatch.fnmatch(path, pattern) or fnmatch.fnmatch(os.path.basename(path), pattern):
                return True
    return False

def matches_include_patterns(path, include_patterns):
    """Check if the given path matches any include patterns."""
    for pattern in include_patterns:
        if pattern.endswith('/'):
            if os.path.isdir(path) and fnmatch.fnmatch(os.path.basename(path), pattern[:-1]):
                return True
        else:
            if fnmatch.fnmatch(path, pattern) or fnmatch.fnmatch(os.path.basename(path), pattern):
                return True
    return False

def generate_tree_lines(directory, ignore_patterns, include_patterns, parent_prefix='', is_last=False, is_root=True):
    """Generate the tree structure lines and collect non-ignored file paths."""
    lines = []
    files = []
    if is_root:
        dir_name = os.path.basename(os.path.normpath(directory))
        lines.append(f"{dir_name}/")
        is_root = False

    try:
        entries = os.listdir(directory)
    except PermissionError:
        return lines, files

    file_include_patterns = []
    dir_include_patterns = []
    if include_patterns:
        for pattern in include_patterns:
            if pattern.endswith('/'):
                dir_include_patterns.append(pattern)
            else:
                file_include_patterns.append(pattern)
    has_file_includes = len(file_include_patterns) > 0

    filtered_entries = []
    for entry in entries:
        entry_path = os.path.join(directory, entry)
        is_dir = os.path.isdir(entry_path)

        if include_patterns:
            if is_dir:
                include_dir = False
                if has_file_includes:
                    include_dir = True
                else:
                    include_dir = matches_include_patterns(entry_path, dir_include_patterns)
                if not include_dir:
                    continue
            else:
                if not matches_include_patterns(entry_path, file_include_patterns):
                    continue

        if match_ignore_patterns(entry_path, ignore_patterns):
            continue

        filtered_entries.append(entry)

    filtered_entries.sort()

    for i, entry in enumerate(filtered_entries):
        entry_path = os.path.join(directory, entry)
        is_last_entry = i == len(filtered_entries) - 1

        connector = '└── ' if is_last_entry else '├── '
        next_connector = '    ' if is_last_entry else '│   '

        current_line = f"{parent_prefix}{connector}{entry}"
        if os.path.isdir(entry_path):
            current_line += '/'
        lines.append(current_line)

        if os.path.isdir(entry_path):
            subdir_prefix = parent_prefix + next_connector
            sub_lines, sub_files = generate_tree_lines(
                entry_path, ignore_patterns, include_patterns, subdir_prefix, is_last_entry, is_root=False
            )
            lines.extend(sub_lines)
            files.extend(sub_files)
        else:
            files.append(entry_path)

    return lines, files

def generate_output(root_directory, ignore_patterns, include_patterns):
    """Generate the tree structure and file content strings."""
    tree_lines, file_paths = generate_tree_lines(root_directory, ignore_patterns, include_patterns)
    tree_str = '\n'.join(tree_lines)
    
    content_str = '\n\n' + '=' * 50 + '\n\n'
    for file_path in file_paths:
        content_str += f'{file_path}\n'
        try:
            with open(file_path, 'r') as content_file:
                content = content_file.read()
            content_str += content
            if content and not content.endswith('\n'):
                content_str += '\n'
        except Exception as e:
            content_str += f'[Error reading file: {e}]\n'
        content_str += '\n' + '-' * 50 + '\n\n'
    return tree_str, content_str

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Generate directory tree and file contents with include/exclude filters.',
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        '-r', '--root',
        default=os.getcwd(),
        help='Root directory to scan (default: current working directory)'
    )
    parser.add_argument(
        '-o', '--output',
        default='treescribe.output.txt',
        help='Output file name (default: treescribe.output.txt)'
    )
    parser.add_argument('-i', '--include', action='append', help='Include patterns (e.g., "*.py", "src/")')
    parser.add_argument('-e', '--exclude', action='append', help='Exclude patterns (e.g., "build/", "*.tmp")')
    parser.add_argument('-n', '--no-file', action='store_true', help='Do not write to a file')
    parser.add_argument('-t', '--print-tree', action='store_true', help='Print directory structure to terminal')
    parser.add_argument('-c', '--print-content', action='store_true', help='Print file contents to terminal')
    
    args = parser.parse_args()

    args.root = os.path.abspath(args.root)
    if not os.path.exists(args.root):
        raise FileNotFoundError(f"Root directory not found: {args.root}")
    if not os.path.isdir(args.root):
        raise NotADirectoryError(f"Path is not a directory: {args.root}")

    ignore_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.trscrignore')
    ignore_patterns = read_ignore_file(ignore_file_path)
    
    if args.exclude:
        ignore_patterns += args.exclude
    
    include_patterns = args.include if args.include else []

    tree_str, content_str = generate_output(args.root, ignore_patterns, include_patterns)
    full_output = tree_str + content_str

    if not args.no_file:
        with open(args.output, 'w') as f:
            f.write(full_output)
        print(f"Done. See {args.output}")

    if args.print_tree:
        print(tree_str)
    
    if args.print_content:
        print(content_str)