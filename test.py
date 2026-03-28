import os
import sys
import unittest
import glob
import shutil
import warnings
from io import StringIO
from unittest.mock import patch

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

warnings.filterwarnings("ignore", message=".*._SixMetaPathImporter.*")


class ViboraTesting(unittest.TestCase):

    def test_pdf_to_png(self):
        try:
            pdf_to_png('testfiles/testpaper1.pdf')
        except Exception as e:
            self.fail(f"pdf_to_png raised an unexpected exception: {e}")
        self.assertTrue(os.path.exists('page0.png'))
        for file in glob.glob('page*.png'):
            os.remove(file)
        print("pdf_to_png OK")

    def test_pdf_to_text(self):
        try:
            pdf_to_text('testfiles/testpaper1.pdf')
        except Exception as e:
            self.fail(f"pdf_to_text raised an unexpected exception: {e}")
        self.assertTrue(os.path.exists('file.txt'))
        with open('file.txt', 'r', encoding='utf-8') as f:
            content = f.read()
            self.assertGreater(len(content), 0)
        os.remove('file.txt')
        print("pdf_to_text OK")

    def test_txt_to_pdf(self):
        try:
            txt_to_pdf('testfiles/testpaper3.txt')
        except Exception as e:
            self.fail(f"txt_to_pdf raised an unexpected exception: {e}")
        self.assertTrue(os.path.exists('myfile.pdf'))
        os.remove('myfile.pdf')
        print("txt_to_pdf OK")

    def test_img_from_pdf(self):
        try:
            extract_img_from_pdf('testfiles/testpaper2.pdf')
        except Exception as e:
            self.fail(f"extract_img_from_pdf raised an unexpected exception: {e}")
        self.assertTrue(os.path.exists('Image1_1.jpeg'))
        for file in glob.glob('Image*.jpeg'):
            os.remove(file)
        print("img_from_pdf OK")

    def test_compress_pdf(self):
        try:
            compress_pdf('testfiles/testpaper1.pdf')
        except Exception as e:
            self.fail(f"compress_pdf raised an unexpected exception: {e}")
        self.assertTrue(os.path.exists('file.pdf'))
        os.remove('file.pdf')
        print("compress_pdf OK")

    def test_merge_pdf(self):
        try:
            merge_pdf('testfiles/testpaper1.pdf', 'testfiles/testpaper2.pdf')
        except Exception as e:
            self.fail(f"merge_pdf raised an unexpected exception: {e}")
        self.assertTrue(os.path.exists('merged_file.pdf'))
        os.remove('merged_file.pdf')
        print("merge_pdf OK")

    def test_merge_pdf_directory(self):
        try:
            merge_pdf_directory('testfiles/')
        except Exception as e:
            self.fail(f"merge_pdf_directory raised an unexpected exception: {e}")
        self.assertTrue(os.path.exists('mergedall_file.pdf'))
        os.remove('mergedall_file.pdf')
        print("merge_pdf_directory OK")

    def test_rename_file(self):
        try:
            rename_file('testfiles/testpaper4.txt', 'new.txt')
        except Exception as e:
            self.fail(f"rename_file raised an unexpected exception: {e}")
        self.assertTrue(os.path.exists('new.txt'))
        rename_file('new.txt', 'testpaper4.txt')
        shutil.move('testpaper4.txt', 'testfiles/testpaper4.txt')
        print("rename_file OK")

    def test_rotate_pdf(self):
        try:
            rotate_pdf('testfiles/rotate.pdf')
        except Exception as e:
            self.fail(f"rotate_pdf raised an unexpected exception: {e}")
        self.assertTrue(os.path.exists('file.pdf'))
        os.remove('file.pdf')
        print("rotate_pdf OK")

    def test_image_to_pdf(self):
        try:
            image_to_pdf('testfiles/testfile.png')
        except Exception as e:
            self.fail(f"image_to_pdf raised an unexpected exception: {e}")
        self.assertTrue(os.path.exists('file.pdf'))
        os.remove('file.pdf')
        print("image_to_pdf OK")

    def test_split_pdf(self):
        try:
            split_pdf('testfiles/testpaper1.pdf')
        except Exception as e:
            self.fail(f"split_pdf raised an unexpected exception: {e}")
        self.assertTrue(os.path.exists('testpaper1_page_1.pdf'))
        for file in glob.glob('testpaper1_page_*.pdf'):
            os.remove(file)
        print("split_pdf OK")

    def test_watermark_pdf(self):
        try:
            watermark_pdf('testfiles/testpaper1.pdf', 'testfiles/file.pdf')
        except Exception as e:
            self.fail(f"watermark_pdf raised an unexpected exception: {e}")
        self.assertTrue(os.path.exists('watermarked.pdf'))
        os.remove('watermarked.pdf')
        print("watermark_pdf OK")

    def test_encrypt_pdf(self):
        try:
            encrypt_pdf("testfiles/testpaper1.pdf", 'passman')
        except Exception as e:
            self.fail(f"encrypt_pdf raised an unexpected exception: {e}")
        self.assertTrue(os.path.exists('file.pdf'))
        os.remove('file.pdf')
        print("encrypt_pdf OK")

    def test_decrypt_pdf(self):
        try:
            encrypt_pdf("testfiles/testpaper1.pdf", 'passman')
            decrypt_pdf("file.pdf", 'passman')
        except Exception as e:
            self.fail(f"decrypt_pdf raised an unexpected exception: {e}")
        self.assertTrue(os.path.exists('file_decrypted.pdf'))
        for file in glob.glob('file*.pdf'):
            os.remove(file)
        print("decrypt_pdf OK")

    def test_redaction(self):
        try:
            redactor = Redactor('testfiles/sampleredaction.pdf')
            redactor.redaction()
        except Exception as e:
            self.fail(f"redaction raised an unexpected exception: {e}")
        self.assertTrue(os.path.exists('redacted.pdf'))
        os.remove('redacted.pdf')
        print("redaction OK")

    def test_compare_file(self):
        try:
            result = compare_file("testfiles/testmatch1.pdf", "testfiles/testmatch2.pdf")
        except Exception as e:
            self.fail(f"compare_file raised an unexpected exception: {e}")
        self.assertTrue(result)
        print("compare_file OK")

    # skipping audio test due to six error
    def ztest_audio(self):
        with patch('sys.stdout', new=StringIO()) as fake_stdout:
            audio('testfiles/testpapervoice.pdf')
            output = fake_stdout.getvalue().strip()
        self.assertTrue(output != '')


if __name__ == '__main__':
    unittest.main()
