import os
from tempfile import NamedTemporaryFile

from PIL import Image
from PyPDF2 import PdfFileReader
from wand.image import Image as WandImage
from tesserwrap import Tesseract


class DocumentExtractor(object):
    def __init__(self, filename, config=None):
        filename = os.path.abspath(filename)
        fileobj = open(filename, 'r+b')

        self.path = filename
        self.file = PdfFileReader(fileobj)
        self.config = {
            'wand_resolution': 200,
            'wand_compression_quality': 70
        }

        if config:
            self.config.update(config)

        self._result_cache = None

    def __len__(self):
        return self.file.numPages

    def __getitem__(self, k):
        if not isinstance(k, (slice,) + (int, long)):
            raise TypeError
        assert ((not isinstance(k, slice) and (k >= 0))
                or (isinstance(k, slice) and (k.start is None or k.start >= 0)
                    and (k.stop is None or k.stop >= 0))), \
                "Negative indexing is not supported."

        if isinstance(k, slice):
            return list(self.iterator(k.start, k.stop))

        return list(self.iterator(k, k + 1))[0]

    def __iter__(self):
        return self.iterator()

    def iterator(self, start=0, stop=0):
        if not stop or stop > self.file.numPages:
            stop = self.file.numPages

        for page in range(start, stop):
            img = WandImage(filename=self.path + ('[%s]' % page),
                resolution=self.config['wand_resolution'])
            img.compression_quality = self.config['wand_compression_quality']
            temp = NamedTemporaryFile(suffix='.jpg')
            # Passing temp as file kwargs does not work for some reason.
            # So we just pass the filename.
            img.save(filename=temp.name)

            # Reopen the image file as PIL object
            img = Image.open(temp.name)

            # Run tesseract
            tr = Tesseract()
            result = tr.ocr_image(img)

            temp.close()

            yield {
                'text': result,
                'page': page + 1
            }
