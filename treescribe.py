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

    filtered_entries = []
    for entry in entries:
        entry_path = os.path.join(directory, entry)
        if include_patterns:
            if not matches_include_patterns(entry_path, include_patterns):
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

def write_tree_to_file(root_directory, ignore_patterns, include_patterns, output_file):
    """Generate the tree and file contents, then write to the output file."""
    tree_lines, file_paths = generate_tree_lines(root_directory, ignore_patterns, include_patterns)
    with open(output_file, 'w') as f:
        f.write('\n'.join(tree_lines))
        f.write('\n\n' + '=' * 50 + '\n\n')
        for file_path in file_paths:
            f.write(f'{file_path}\n')
            try:
                with open(file_path, 'r') as content_file:
                    content = content_file.read()
                f.write(content)
                if content and not content.endswith('\n'):
                    f.write('\n')
            except Exception as e:
                f.write(f'[Error reading file: {e}]\n')
            f.write('\n' + '-' * 50 + '\n\n')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate directory tree and file contents with include/exclude filters.')
    parser.add_argument('-i', '--include', action='append', help='Include patterns (e.g., "*.py", "src/")')
    parser.add_argument('-e', '--exclude', action='append', help='Exclude patterns (e.g., "build/", "*.tmp")')
    parser.add_argument('-o', '--output', default='treescribe.output.txt', help='Output file name')
    args = parser.parse_args()

    script_dir = os.path.dirname(os.path.abspath(__file__))
    ignore_file_path = os.path.join(script_dir, '.trscrignore')
    ignore_patterns = read_ignore_file(ignore_file_path)
    
    if args.exclude:
        ignore_patterns += args.exclude
    
    include_patterns = args.include if args.include else []
    root_directory = os.getcwd()
    output_file = args.output

    write_tree_to_file(root_directory, ignore_patterns, include_patterns, output_file)