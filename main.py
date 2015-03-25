import sys
from latex2wordpress import Converter

def main():
    """
    Driver function for LaTeX to Wordpress converter.
    @return: None
    """

    inputfile = open(sys.argv[1])
    auxfile = open(sys.argv[2])
    converter = Converter(inputfile, auxfile)


    print "Extracting text...",
    converter.extract_text()
    print "done"

    print "Substituting custom commands defined via \\newcommand{}..."
    converter.convert_newcommands()

    print "Stripping title elements...",
    converter.strip_title_elements()
    print "done"

    print "Processing inline math...",
    converter.convert_inline_math()
    print "done"

    print "Processing \\equation{} environment...",
    converter.convert_equations()
    print "done"

    print "Processing \\align{} environment...",
    converter.convert_aligned()
    print "done"

    print "Processing \\section{} environment...",
    converter.convert_sections()
    print "done"

    print "Processing cross references...",
    converter.convert_references()
    print "done"

    print "Processing formatting...",
    converter.convert_formatting()
    print "done"

    print "Writing HTML output...",
    converter.write_html()
    print "done"

if __name__ == "__main__":
    main()