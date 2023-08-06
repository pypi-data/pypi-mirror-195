# tokenish

![Code Coverage](https://img.shields.io/badge/Coverage-96%25-brightgreen.svg)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A simple tool to fill pattern with tokens from file or directory.

- [Installation](#installation)
- [How to use](#how-to-use)
- [Example](#example)
- [Commands](#commands)
- [License](#license)
- [Tests](#tests)

## Installation

```sh
pip install tokenish
```

## How to use

```txt
usage: tokenish [-h] [-t TOKENS [TOKENS ...]] [-e ENCODING] [-o OUTPUT_DIRECTORY] [-om MAX_FILE_ROWS] pattern

Generate rows from pattern for each token combinations

positional arguments:
  pattern               text to fill with links or usernames/passwords

optional arguments:
  -h, --help            show this help message and exit
  -t TOKENS [TOKENS ...], --tokens TOKENS [TOKENS ...]
                        list of tokens file or directory path
  -e ENCODING, --encoding ENCODING
                        type of encoding to apply
  -o OUTPUT_DIRECTORY, --output-directory OUTPUT_DIRECTORY
                        directory where results will write, print is None
  -om MAX_FILE_ROWS, --max-file-rows MAX_FILE_ROWS
                        maximum number of rows per file, default 10 000
```

Available token paths:

- file: all lines in file are consider like tokens.
- directory: all lines of all files in directory are consider like tokens.

Each token paths should have an associated token in pattern.
For example, if two token paths are defined, pattern should contain &TOKEN_0& and &TOKEN_1&.

Available encodings:

- base64

The pattern part to encode must be in the following tag:

```txt
&ENC[to encode]ODE&
```

## Example

Let's consider the /tokens directory with the following tree structure:

```txt
.
├── passwords
│   └── passwords_1.txt
└── usernames
    ├── usernames_1.txt
    └── usernames_2.txt
```

Content of usernames_1.txt:

```txt
admin
root
user
```

Content of usernames_2.txt:

```txt
user1
user2
```

Content of passwords_1.txt:

```txt
1234
6712
```

The command:

```sh
tokenish "Authorization: Basic &TOKEN_0&:&TOKEN_1&" -t usernames/ passwords/passwords_1.txt
```

Print:

```txt
Authorization: Basic admin:1234
Authorization: Basic admin:6712
Authorization: Basic root:1234
Authorization: Basic root:6712
Authorization: Basic user:1234
Authorization: Basic user:6712
Authorization: Basic user1:1234
Authorization: Basic user1:6712
Authorization: Basic user2:1234
Authorization: Basic user2:6712
```

You can add an encoding like:

```sh
tokenish "Authorization: Basic &ENC[&TOKEN_0&:&TOKEN_1&]ODE&" -t usernames/ passwords/passwords_1.txt -e base64
```
Print:

```txt
Authorization: Basic YWRtaW46MTIzNA==
Authorization: Basic YWRtaW46NjcxMg==
Authorization: Basic cm9vdDoxMjM0
Authorization: Basic cm9vdDo2NzEy
Authorization: Basic dXNlcjoxMjM0
Authorization: Basic dXNlcjo2NzEy
Authorization: Basic dXNlcjE6MTIzNA==
Authorization: Basic dXNlcjE6NjcxMg==
Authorization: Basic dXNlcjI6MTIzNA==
Authorization: Basic dXNlcjI6NjcxMg==
```

## Commands

Print all combination of username/password, where usernames replace &TOKEN_0& and passwords replace &TOKEN_1&.

```sh
tokenish "Authorization: Basic &TOKEN_0&:&TOKEN_1&" -t /path/to/usernames/dir/ /path/to/passwords.txt
```

Save all combination of username/password in directory /path/output/ composed by files of 10 000 lines.

```sh
tokenish "Authorization: Basic &TOKEN_0&:&TOKEN_1&" -t /path/to/usernames/dir/ /path/to/passwords.txt -o /path/output/
```

Save all combination of username/password in directory /path/output/ composed by files of 500 lines.

```sh
tokenish "Authorization: Basic &TOKEN_0&:&TOKEN_1&" -t /path/to/usernames/dir/ /path/to/passwords.txt -o /path/output/ -om 500
```

Print all combination of username/password, where usernames replace &TOKEN_0& and passwords replace &TOKEN_1&.
Expression in tag &ENC[...]ODE& will encode in base64.

```sh
tokenish "Authorization: Basic &ENC[&TOKEN_0&:&TOKEN_1&]ODE&" -t /path/to/usernames/dir/ /path/to/passwords.txt -e base64
```

## License

tokenish is released under MIT license. See [LICENSE](https://github.com/VictorMeyer77/tokenish/blob/main/LICENSE).

## Tests

Run these commands to run tests and update coverage badge:

```sh
pip install readme-coverage-badger
coverage run -m --omit "/usr/local/*,/usr/lib/*,tests/*,venv/*" unittest discover tests/tokenish
readme-cov
```