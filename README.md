# 🌳 TreeScribe

> CLI tool that generates a tree-structured overview project directory, including the contents of its files.

## ⚙️ Installation

```bash
brew tap mdmatvey/treescribe https://github.com/mdmatvey/TreeScribe.git
brew install treescribe
```

## 🏃‍➡️ Usage

```bash
treescribe [OPTIONS]
```

## 🛠️ Options

| Flag                     | Description                 | Example                   |
|--------------------------|-----------------------------|---------------------------|
| `-h ,   --help`          | Show help message           | `-h`                      |
| `-r ,   --root`          | Root directory to scan      | `-r example_project`      |
| `-o ,   --output`        | Output file name            | `-o project_snapshot.txt` |
| `-i ,   --include`       | Include specific patterns   | `-i "*.py" -i "*.md"`     |
| `-e ,   --exclude`       | Exclude additional patterns | `-e "temp/" -e "*.log"`   |
| `-n ,   --no-file`       | Disable file output         | `-n`                      |
| `-t ,   --print-tree`    | Print structure to terminal | `-t`                      |
| `-c ,   --print-content` | Print contents to terminal  | `-c`                      |

## 📚 Examples

> Feel free to try how the utility works on the attached example_project repository

### 1. Full snapshot

```bash
treescribe -r example_project
```

**Output:**

```

example_project/
├── dir1/
│   ├── file1.txt
│   ├── file2.py
│   └── subdir1/
│       └── subfile1.txt
├── dir2/
│   └── file3.md
├── dir3/
│   ├── file4.py
│   ├── subdir2/
│   │   └── subfile2.py
│   └── subfile2.py
└── file5.txt

==================================================

/Users/mdmatvey/Work/Scripts/TreeScribe/example_project/dir1/file1.txt
This is file1

--------------------------------------------------

/Users/mdmatvey/Work/Scripts/TreeScribe/example_project/dir1/file2.py
This is file2
Dummy row

--------------------------------------------------

/Users/mdmatvey/Work/Scripts/TreeScribe/example_project/dir1/subdir1/subfile1.txt
This is subfile1
Dummy row

--------------------------------------------------

/Users/mdmatvey/Work/Scripts/TreeScribe/example_project/dir2/file3.md
This is file3

--------------------------------------------------

/Users/mdmatvey/Work/Scripts/TreeScribe/example_project/dir3/file4.py
This is file4
Dummy row
Dummy row
Dummy row

--------------------------------------------------

/Users/mdmatvey/Work/Scripts/TreeScribe/example_project/dir3/subdir2/subfile2.py
This is subfile2

--------------------------------------------------

/Users/mdmatvey/Work/Scripts/TreeScribe/example_project/dir3/subfile2.py
This is subfilefile2

--------------------------------------------------

/Users/mdmatvey/Work/Scripts/TreeScribe/example_project/file5.txt
This is file5

--------------------------------------------------
```

### 2. Include Python Files (only)

```bash
treescribe -r example_project -i "*.py"
```

**Output:**

```
example_project/
├── dir1/
│   ├── file2.py
│   └── subdir1/
├── dir2/
└── dir3/
    ├── file4.py
    ├── subdir2/
    │   └── subfile2.py
    └── subfile2.py

==================================================

/Users/mdmatvey/Work/Scripts/TreeScribe/example_project/dir1/file2.py
This is file2
Dummy row

--------------------------------------------------

/Users/mdmatvey/Work/Scripts/TreeScribe/example_project/dir3/file4.py
This is file4
Dummy row
Dummy row
Dummy row

--------------------------------------------------

/Users/mdmatvey/Work/Scripts/TreeScribe/example_project/dir3/subdir2/subfile2.py
This is subfile2

--------------------------------------------------

/Users/mdmatvey/Work/Scripts/TreeScribe/example_project/dir3/subfile2.py
This is subfilefile2

--------------------------------------------------
```

### 3. Exclude Text and Markdown Files

```bash
treescribe -r example_project -e "*.txt" -e "*.md"
```

**Output:**

```
example_project/
├── dir1/
│   ├── file2.py
│   └── subdir1/
├── dir2/
└── dir3/
    ├── file4.py
    ├── subdir2/
    │   └── subfile2.py
    └── subfile2.py

==================================================

/Users/mdmatvey/Work/Scripts/TreeScribe/example_project/dir1/file2.py
This is file2
Dummy row

--------------------------------------------------

/Users/mdmatvey/Work/Scripts/TreeScribe/example_project/dir3/file4.py
This is file4
Dummy row
Dummy row
Dummy row

--------------------------------------------------

/Users/mdmatvey/Work/Scripts/TreeScribe/example_project/dir3/subdir2/subfile2.py
This is subfile2

--------------------------------------------------

/Users/mdmatvey/Work/Scripts/TreeScribe/example_project/dir3/subfile2.py
This is subfilefile2

--------------------------------------------------
```

### 4. Terminal only

```bash
python3 treescribe.py -r example_project -n -t -c
```

**Output:** _the same as in the first point but in the terminal, not in the file_