import os

class Sym_norm:
    SRC_DOC_PATH = os.getenv('PREFIX') + '/share/apache2/default-site/htdocs/manual'
    DEST_DOC_PATH = os.getenv('HOME') + '/.011/share/ln/docs/apache2-docs'
    SRC_SUFFIX = '.en'
    DEST_SUFFIX = ''

    def create_symlink(self):
        if not os.path.exists(self.DEST_DOC_PATH):
            os.mkdir(self.DEST_DOC_PATH)
        assert os.path.exists(self.SRC_DOC_PATH), "directory '{0}' does not exist!".format(path)
        for dirpath, dirnames, filenames in os.walk(self.SRC_DOC_PATH):
            dest_path = os.path.join(self.DEST_DOC_PATH + dirpath.removeprefix(self.SRC_DOC_PATH))
            if not os.path.exists(dest_path):
                os.mkdir(dest_path)
            for filename in filenames:
                if filename.endswith(self.SRC_SUFFIX):
                    os.symlink(dirpath + '/' + filename, dest_path + '/' + filename.removesuffix(self.SRC_SUFFIX) + self.DEST_SUFFIX)

if __name__ == '__main__':
    Sym_norm().create_symlink()
