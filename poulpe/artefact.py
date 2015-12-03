'''Helpful functions when writing artefacts'''
import logging
import os
from .util import cmd, lines
import magic
import re
import shlex


def validate(index, artefact_type):
    '''If necessary, create the appropriate directory in the index'''
    if not os.path.isdir(index+'/'+artefact_type):
        logging.warn('Creating '+artefact_type+' index at ' +
                     index+'/'+artefact_type)
        cmd('mkdir -p '+index+'/'+artefact_type)


def text_data(fname):
    '''Return the text in fname, with best effort conversion'''
    mime = str(magic.Magic(mime=True).from_file(fname))
    logging.info('MIME Type : '+mime)
    if 'text' not in mime:
        return ''
    return open(fname, 'r', encoding='utf8').read()


def artefact_fname(index, artefact_type, artefact):
    '''Return the filename in which to record the blobs artefact is in'''
    return '/'.join([index, artefact_type, artefact])


def art_in_blob(index, artefact_type, artefact, blob):
    '''Return True iff we already know that artefact is in blob'''
    try:
        return blob in lines(artefact_fname(index, artefact_type, artefact))
    except FileNotFoundError:
        return False


def blob2file_fname(index, blob):
    '''Return the filename in which to record what files hash to a blob'''
    return '/'.join([index, 'objects', blob, 'files'])


def filehash_is_blob(index, blob, fname):
    '''Return True iff we already know that fname's hash is blob'''
    try:
        return fname in lines(blob2file_fname(index, blob))
    except FileNotFoundError:
        return False


def blob2artefact_fname(index, blob, artefact_type):
    '''Return the filename in which to records the artefact of this type that
    blob contains'''
    return '/'.join([index, 'objects', blob, artefact_type])


def blob_contains_art(index, blob, artefact_type, artefact):
    '''Return True iff we already know that blob contains this artefact'''
    try:
        return artefact in blob2artefact_fname(index, blob, artefact_type)
    except FileNotFoundError:
        return False


def add_record(index, artefact_type, artefact, fname):
    '''Inform the index that artefact was seen in file

    The index is a directory whose structure is :

    - objects/

      - <blob>/

        - files <- list of filenames whose hash equals <blob>
        - <artefact_type1> <- list of artefact of this type contained in blob
        - <artefact_type2>
        - ...
      - ...
    - <artefact_type1>

      - <artefact11> <- list of blobs that contain <artefact11>
      - <artefact12>
      -...
    - ...


    Therefore this functions writes in three files, if necessary :

    - in objects/<blob>/files to add the filename for <blob>
    - in objects/<blob>/<artefact_type> to add the artefact
    - in <artefact_type>/<artefact> to add the blob

'''
    logging.info('Creating record for '+artefact+' in '+fname)
    blob = cmd("git hash-object "+shlex.quote(fname)).strip()
    if not art_in_blob(index, artefact_type, artefact, blob):
        logging.debug('Writing that '+artefact+' is in '+blob)
        with open(artefact_fname(index, artefact_type, artefact), 'a') as f:
            f.write(blob+'\n')
    if not filehash_is_blob(index, blob, fname):
        logging.debug('Writing that '+fname+' hashes to '+blob)
        os.makedirs(os.path.dirname(blob2file_fname(index, blob)),
                    exist_ok=True)
        with open(blob2file_fname(index, blob), 'a') as f:
            f.write(fname+'\n')
    if not blob_contains_art(index, blob, artefact_type, artefact):
        logging.debug('Writing that '+blob+' contains '+artefact)
        with open(blob2artefact_fname(index, blob, artefact_type), 'a') as f:
            f.write(artefact+'\n')


def index_regex(index, fname, artefact_type, regex):
    '''Populate the index with all instances of regex found in fname'''
    text = text_data(fname)
    for art in set(map(lambda x: x.group(0),
                       re.finditer(regex, text))):
        add_record(index, artefact_type, art, fname)
