import sys
import logging
import argparse

from vibora.pdf2png import pdf_to_png
from vibora.pdf2txt import pdf_to_text
from vibora.txt2pdf import txt_to_pdf
from vibora.extract_img_from_pdf import extract_img_from_pdf
from vibora.compress import compress_pdf
from vibora.merge import merge_pdf, merge_pdf_directory
from vibora.rename import rename_file
from vibora.rotate import rotate_pdf
from vibora.img2pdf import image_to_pdf
from vibora.split import split_pdf
from vibora.watermark import watermark_pdf
from vibora.encrypt import encrypt_pdf
from vibora.decrypt import decrypt_pdf
from vibora.pdf2audio import audio
from vibora.redact import Redactor
from vibora.compare import compare_file
from vibora.extra_compression.rwcompression import rwcomp
from vibora.extra_compression.fitzcompression import fitzcomp
from vibora.pdf_search import pdf_search


COMMAND_MESSAGES = {
    "pdf2png": "Converting file: {pdf_path}",
    "pdf2txt": "Converting file: {pdf_path}",
    "extractimg": "Extracting images from file: {pdf_path}",
    "compress": "Compressing file: {pdf_path}",
    "txt2pdf": "Converting file: {txt_path}",
    "merge": "Merging files: {pdf_files}",
    "mergeall": "Merging files in directory: {dir_path}",
    "rename": "Renaming file {file_path} to {new_name}",
    "rotate": "Rotating file: {pdf_path}",
    "img2pdf": "Converting file: {img_path}",
    "split": "Splitting file: {pdf_path}",
    "watermark": "Adding watermark to file: {pdf_path}",
    "encrypt": "Encrypting file: {pdf_path}",
    "decrypt": "Decrypting file: {pdf_path}",
    "pdf2audio": "Reading file: {pdf_path}",
    "redact": "Redacting file: {pdf_path}",
    "compare": "Comparing files {file1} and {file2}",
}


def setup_debug(args):
    if getattr(args, "debug", False):
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.WARNING)


def print_status(command, args):
    msg = COMMAND_MESSAGES.get(command)
    if msg:
        print(f"{msg.format(**vars(args))}\n. . .")


def custom_error(msg):
    print("Command not recognized. Use 'help' to see the available commands.")
    sys.exit(1)


def build_parser():
    parser = argparse.ArgumentParser(description="vibora")
    parser.error = custom_error
    subparser = parser.add_subparsers(title='subparser', dest='subcommand')

    def add_debug(p):
        p.add_argument('-d', '--debug', action='store_true', help='enable debug mode')

    # pdf2png
    p = subparser.add_parser('pdf2png', description='Convert a .PDF file into a .PNG file.')
    p.add_argument('pdf_path', type=str, help='Path to the PDF file to convert.')
    add_debug(p)

    # pdf2txt
    p = subparser.add_parser('pdf2txt', description='Convert a .PDF file into a .TXT file.')
    p.add_argument('pdf_path', type=str, help='Path to the PDF file.')
    add_debug(p)

    # extractimg
    p = subparser.add_parser('extractimg', description='Extract all images from a .PDF file.')
    p.add_argument('pdf_path', type=str, help='Path to the .PDF file.')
    add_debug(p)

    # compress
    p = subparser.add_parser('compress', description='Compress a PDF file without losing quality.')
    p.add_argument('pdf_path', type=str, help='Path to the PDF file to compress.')
    p.add_argument('output', type=str, nargs='?', help='Name of the output file.')
    add_debug(p)

    # txt2pdf
    p = subparser.add_parser('txt2pdf', description='Convert a .TXT file into a .PDF file.')
    p.add_argument('txt_path', type=str, help='Path to the .TXT file.')
    add_debug(p)

    # merge
    p = subparser.add_parser('merge', description='Merge .PDF files into a single one.')
    p.add_argument('pdf_files', type=str, nargs='+', help='Path to .PDF files.')
    add_debug(p)

    # mergeall
    p = subparser.add_parser('mergeall', description='Merge all .PDF files inside a directory.')
    p.add_argument('dir_path', type=str, help='Path to directory.')
    add_debug(p)

    # rename
    p = subparser.add_parser('rename', description='Rename a file.')
    p.add_argument('file_path', type=str, help='Path to the file to rename.')
    p.add_argument('new_name', type=str, help='New file name.')
    add_debug(p)

    # rotate
    p = subparser.add_parser('rotate', description='Rotate a .PDF file by 90 degrees.')
    p.add_argument('pdf_path', type=str, help='Path to the .PDF file.')
    add_debug(p)

    # img2pdf
    p = subparser.add_parser('img2pdf', description='Convert an image into a .PDF file.')
    p.add_argument('img_path', type=str, help='Path to the image file.')
    add_debug(p)

    # split
    p = subparser.add_parser('split', description='Split a .PDF file into separated page files.')
    p.add_argument('pdf_path', type=str, help='Path to the .PDF file.')
    add_debug(p)

    # watermark
    p = subparser.add_parser('watermark', description='Add a watermark to a .PDF file.')
    p.add_argument('pdf_path', type=str, help='Path to the .PDF file.')
    p.add_argument('watermark_path', type=str, help='Path to the watermark file.')
    add_debug(p)

    # encrypt
    p = subparser.add_parser('encrypt', description='Encrypt a .PDF file.')
    p.add_argument('pdf_path', type=str, help='Path to the .PDF file.')
    p.add_argument('password', type=str, help='Password to encrypt the file with.')
    add_debug(p)

    # decrypt
    p = subparser.add_parser('decrypt', description='Decrypt a .PDF file.')
    p.add_argument('pdf_path', type=str, help='Path to the .PDF file.')
    p.add_argument('password', type=str, help='Password to decrypt the file.')
    add_debug(p)

    # pdf2audio
    p = subparser.add_parser('pdf2audio', description='Read a .PDF file aloud.')
    p.add_argument('pdf_path', type=str, help='Path to the .PDF file.')
    add_debug(p)

    # redact
    p = subparser.add_parser('redact', description='Redact sensitive information from a .PDF file.')
    p.add_argument('pdf_path', type=str, help='Path to the .PDF file.')
    add_debug(p)

    # compare
    p = subparser.add_parser('compare', description='Compare files at a low level.')
    p.add_argument('file1', type=str, help='Path to file one.')
    p.add_argument('file2', type=str, help='Path to file two.')
    add_debug(p)

    # rwcompress
    p = subparser.add_parser('rwcompress', description='Compress files using pdfrw compression algorithm.')
    p.add_argument('pdf_path', type=str, help='Path to the .PDF file.')

    # fitzcompress
    p = subparser.add_parser('fitzcompress', description='Compress files using pymupdf.')
    p.add_argument('pdf_path', type=str, help='Path to the .PDF file.')

    # pdfsearch
    p = subparser.add_parser('pdfsearch', description='Search for .PDF files on the web.')
    p.add_argument('theme', type=str, nargs='+', help='What kind of .PDF files you want to find?')

    return parser


def run_command(args):
    cmd = args.subcommand
    setup_debug(args)

    if cmd in COMMAND_MESSAGES:
        print_status(cmd, args)

    match cmd:
        case 'pdf2png':
            pdf_to_png(args.pdf_path)
        case 'pdf2txt':
            pdf_to_text(args.pdf_path)
        case 'extractimg':
            extract_img_from_pdf(args.pdf_path)
        case 'compress':
            compress_pdf(args.pdf_path, args.output)
        case 'txt2pdf':
            txt_to_pdf(args.txt_path)
        case 'merge':
            merge_pdf(*args.pdf_files)
        case 'mergeall':
            merge_pdf_directory(args.dir_path)
        case 'rename':
            rename_file(args.file_path, args.new_name)
        case 'rotate':
            rotate_pdf(args.pdf_path)
        case 'img2pdf':
            image_to_pdf(args.img_path)
        case 'split':
            split_pdf(args.pdf_path)
        case 'watermark':
            watermark_pdf(args.pdf_path, args.watermark_path)
        case 'encrypt':
            encrypt_pdf(args.pdf_path, args.password)
        case 'decrypt':
            decrypt_pdf(args.pdf_path, args.password)
        case 'pdf2audio':
            audio(args.pdf_path)
        case 'redact':
            Redactor(args.pdf_path).redaction()
        case 'compare':
            compare_file(args.file1, args.file2)
        case 'rwcompress':
            rwcomp(args.pdf_path)
        case 'fitzcompress':
            fitzcomp(args.pdf_path)
        case 'pdfsearch':
            theme = ' '.join(args.theme)
            pdf_search(theme)


if __name__ == '__main__':
    if len(sys.argv) == 1:
        print("Missing arguments, see 'help' for reference on how to use it!")
    elif sys.argv[1].lower() == 'help':
        import os
        help_path = os.path.join(os.path.dirname(__file__), 'vibora', 'help')
        with open(help_path, 'r') as f:
            print(f.read())
    else:
        parser = build_parser()
        args = parser.parse_args()
        run_command(args)
