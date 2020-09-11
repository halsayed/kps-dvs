import base64
import zipfile
import os
from os import path
from config import Config


def allowed_file(filename, extensions):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in extensions


def encode_certificate_bundle(certificate_bundle):
    with open(certificate_bundle, 'rb') as file:
        encoded_certificate = base64.b64encode(file.read())
    return encoded_certificate


def unpack_certificate_bundle(filename, upload_dir):

    with zipfile.ZipFile(filename) as archive:
        contents = []
        for entry in archive.filelist:
            suffix = entry.filename.split('_', 1)[1]
            contents.append(suffix)
            archive.extract(entry.filename, upload_dir)
            os.rename(os.path.join(upload_dir, entry.filename),
                      os.path.join(upload_dir, suffix))

        expected = ['CACertificate.crt', 'certificate.crt', 'privateKey.key']
        contents.sort()
        if contents != expected:
            raise Exception("unexpected archive contents: {} != {}".format(contents, expected))

        ca_certificate, client_certificate, client_key = [os.path.join(upload_dir, fn) for fn in expected]
        return ca_certificate, client_certificate, client_key


def certificate_bundle_loaded():
    return path.isfile(Config.CA_CERT) and path.isfile(Config.CLIENT_CERT) and path.isfile(Config.CLIENT_KEY)

