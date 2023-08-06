from sphinx.application import Sphinx
import os


def generate_pdf(doc_path, doc_index):
    """
    Generate a PDF file from a Sphinx documentation project.

    Args:
        doc_path (str): The path to the root directory of the Sphinx documentation project.
        doc_index (str): The filename of the RST index file (without the extension).
    """
    # Change to the documentation directory
    os.chdir(doc_path)

    # Build the documentation
    app = Sphinx(doc_path, doc_path, doc_path, doc_path, doc_index, buildername='latex')
    app.build()

    # Convert the LaTeX file to PDF
    os.chdir(os.path.join(doc_path, '_build', 'latex'))
    os.system('make')

    # Move the PDF file to the documentation directory
    os.rename(os.path.join(doc_path, '_build', 'latex', f'{doc_index}.pdf'), os.path.join(doc_path, f'{doc_index}.pdf'))

if __name__ == '__main__':
    generate_pdf("docs/source", 'index')