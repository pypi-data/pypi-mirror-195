import argparse
import sys
from tokenish.lib.result_writer import ResultWriter
from tokenish.lib.tokenizer import *
from tokenish.lib.encoder import encode_expressions


def main(pattern, token_paths, encoding, writer):
    token_list = gather_tokens(token_paths)
    filled_expressions = fill_tokens(token_list, pattern) if len(token_paths) > 0 else []
    encoded_expressions = encode_expressions(filled_expressions, encoding) if encoding is not None \
        else filled_expressions
    if writer is not None:
        [writer.write_row(expression) for expression in encoded_expressions]
    else:
        [print(expression) for expression in encoded_expressions]
    if writer is not None:
        writer.close_file()


def parse_args(args):
    parser = argparse.ArgumentParser(prog="tokenish",
                                     description="Generate rows from pattern for each token combinations",
                                     epilog="More information on GitHub")
    parser.add_argument("pattern", help="text to fill with links or usernames/passwords")
    parser.add_argument("-t", "--tokens", nargs="+", help="list of tokens file or directory path")
    parser.add_argument("-e", "--encoding", help="type of encoding to apply")
    parser.add_argument("-o", "--output-directory", help="directory where results will write, print is None")
    parser.add_argument("-om", "--max-file-rows", type=int, help="maximum number of rows per file, default 10 000")

    args = parser.parse_args(args)

    tokens = [] if args.tokens is None else args.tokens

    if args.output_directory is not None:
        max_row_per_file = 10000 if args.max_file_rows is None else args.max_file_rows
        result_writer = ResultWriter(args.output_directory, max_row_per_file)
    else:
        result_writer = None

    return args.pattern, tokens, args.encoding, result_writer


if __name__ == '__main__':
    parameters = parse_args(sys.argv[1:])
    main(pattern=parameters[0], token_paths=parameters[1], encoding=parameters[2], writer=parameters[3])
    sys.exit(0)
