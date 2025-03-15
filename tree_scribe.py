import os

def get_directory_structure(root_dir):
    structure = []
    for root, files in os.walk(root_dir):
        level = root.replace(root_dir, '').count(os.sep)
        indent = ' ' * 4 * level
        structure.append(f"{indent}[{os.path.basename(root)}]")
        sub_indent = ' ' * 4 * (level + 1)
        for file in files:
            structure.append(f"{sub_indent}{file}")
    return '\n'.join(structure)

def get_files_content(root_dir):
    file_contents = []
    for root, _, files in os.walk(root_dir):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                file_contents.append(f"---\n{file_path}\n---\n{content}")
            except Exception as e:
                file_contents.append(f"---\n{file_path}\n---\n[Reading error: {e}]")
    return '\n'.join(file_contents)

def main():
    root_dir = os.getcwd()
    output_file = os.path.join(root_dir, "ts_output.txt")
    
    structure = get_directory_structure(root_dir)
    file_contents = get_files_content(root_dir)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(structure)
        f.write('\n' + '=' * 50 + '\n')
        f.write(file_contents)
    
    print(f"Done. See '{output_file}'")

if __name__ == "__main__":
    main()