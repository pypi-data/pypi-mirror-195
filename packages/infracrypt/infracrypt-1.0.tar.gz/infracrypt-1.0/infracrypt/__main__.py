"""Infracrypt main module."""
import json
import os
import sys
from infracrypt import pyfile_encode, pyfile_parser

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python -m infracrypt <path to python file>")
        sys.exit(1)
    ARG = sys.argv[1]
    responses = pyfile_parser.parse_and_return_responses(os.path.abspath(ARG))
    if responses == 'No imports of flask found, file is invalid':
        sys.exit(1)
    encrypted_responses = pyfile_encode.encrypt_responses([
        response[1][7:] for response in responses
    ])
    with open("encrypted_responses.json", "w", encoding='utf-8') as jsonfile:
        jsonfile.write(json.dumps({"encryptions" : encrypted_responses}))
    # replace the return statements in the file with the encrypted responses
    lines = []
    with open(os.path.abspath(ARG), "r", encoding='utf-8') as file:
        lines = file.readlines()
    with open(os.path.abspath(ARG), "w", encoding='utf-8') as file:
        ENC_COUNTER = 0
        for i, line in enumerate(lines):
            if line.strip().startswith("return"):
                ENC_TEXT = f"'{encrypted_responses[ENC_COUNTER]['response']}'"
                file.write(
                    line.replace(
                        line.strip()[7:], ENC_TEXT
                    )
                )
                ENC_COUNTER += 1
            else:
                file.write(line)
    print("File has been rewritten with encryption!")
    print("Encryption data in encrypted_responses.json")
                           