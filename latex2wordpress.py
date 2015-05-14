import re

class Converter(object):
    """
    This is the main class that performs the conversion from native LaTeX code to
    HTML-ized code suitable for copy-pasting into Wordpress. This class has private
    methods (beginning with an underscore) for internal use and public methods for
    public consumption.

    The methods together make several passes through the LaTeX source code, each time
    modifying the self.content_modified class member. The main() function performs the
    conversion by instantiating the class with the latex source and the .aux file
    created during LaTeX source compilation. The main function then calls the
    various convert* methods of this class to process various LaTeX tags.

    There is not inherent order to calling of these convert* methods, but it is
    recommended that they be called in the order shown in main.py.

    The various private methods implement helper function needed by the convert*
    methods.
    """


    # Private methods. Not for public consumption

    def _generate_newcommand_map(self):
        """
        Creates a mapping between custom commands defined via \newcommand{} and its
        latex source

        LaTeX users tend to define custom commands for frequently-used key sequences.
        There is no way to transfer these definitions over to Wordpress. As a result,
        the definition of these custom commands needs to be extracted from the
        definition and resubstituted into the source. We need a mapping between the
        custom command name and its code in standard Latex. This method creates such a
        mapping

        @return: None
        """
        newcommand_mappings = re.findall(r'\\newcommand\{(\\\w+)\}\{(.*?)\}\n',
                                         self.content,
                                         re.DOTALL)
        return dict(newcommand_mappings)

    def _generate_label_map(self, auxfile):
        """
        Creates mapping between label string and label number.

        Equation numbering in LaTeX source happens via equation labels. During
        compilation, the LaTeX engine makes a second pass through the LaTeX source code
        and assigns numbers to the labels. Since Wordpress does not have a LaTeX
        compiler in a traditional sense, we need to assign numbers to labels manually.
        For that, we need a hashmap of label string to label number. The .aux file
        created during latex compilation needs to be parsed to create this mapping.

        @param auxfile: The .aux file generated during latex source compilation
        @return: None
        """
        labels = re.findall(r"\\newlabel\{(.*?)\}\{\{(.*?)\}",
                            auxfile.read())
        return dict(labels)

    def _process_equation(self, matchobj):
        """
        This is the function passed to re.sub() for processing the \begin{equation}
        tag. It does two things: (1) replaces the \label{string} with an equation
        number by consulting the self.labelmap and (2) places the contents of \begin{
        equation} in HTML tags. It returns the HTML-ized equation string with equation
        number.

        @param matchobj: matchobject passed to this function by re.sub()
        @return: Wordpress-compatible HTML-ized equation string
        """
        eqstring = matchobj.group(0)

        try:
            # Extract the \label{...} from the equation
            labelstring = re.findall(r"\\label\s*\{(.*?)\}",
                                     eqstring)[0]

            # Replace the label text with the equation number gotten form the aux file
            eqstring = re.sub(	r"\\label\s*\{(.*?)\}",
                                    "\ \ \ \ \ (%s)" % self.labelmap[labelstring],
                                    eqstring,
                                    re.DOTALL)
        except IndexError:
            # \label tag is not present in the equation
            pass

        eq_strip_latex_tags = re.sub(	r"\\begin\s*\{\s*equation\s*\}([\s\S]*?)\\end\s*\{\s*equation\s*\}",
                                        '<p align="center"> \\n $latex \displaystyle \\1 $</p>',
                                        eqstring,
                                        re.DOTALL)

        return eq_strip_latex_tags

    def _process_align(self, matchobj):
        """
        This is the function passed to re.sub() for processing the \begin{align}
        tag. It does two things: (1) replaces the \label{string} with an equation
        number by consulting the self.labelmap and (2) places the contents of \begin{
        align} in HTML tags. It returns the HTML-ized equation string with equation
        number.
        @param matchobj: matchobject passed to this function by re.sub()
        @return: Wordpress-compatible HTML-ized equation string
        """
        align_string = matchobj.group(0)

        try:
            # Extract the \label{...} from the equation
            labelstrings = re.findall(r"\\label\s*\{(.*?)\}",
                                      align_string)

            # Replace the label texts with the equation number gotten form the aux file
            for ls in labelstrings:
                align_string = re.sub(	r"\\label\s*\{(.*?)\}",
                                            "\ \ \ \ \ (%s)" % self.labelmap[ls],
                                            align_string,
                                            count=1)
        except IndexError:
            # \label tag is not present in the aligned environment
            pass

        al_strip_latex_tags = re.sub(	r"\\begin\s*\{\s*align\s*\}([\s\S]*?)\\end\s*\{\s*align\s*\}",
                                        '<p align = "center"> \n $latex \n \\\\begin{aligned} \n\t\\1 \n\\\\end{aligned}\n$ \n<p>',
                                        align_string,
                                        re.DOTALL)

        return al_strip_latex_tags

    def _process_reference(self, reftype="myeqno"):
        """
        Replaces \myeqno{} and \eqref{} tags in *text* (not equation/align
        environments) with numbers

        @param reftype: Type of reference.
        @return:
        @TODO: Refactor this to remove explicit hardcoding of reference types.
        """
        # if reftype == "myeqno":
        #     refpattern = r"\\myeqno\s*\{\s*([\s\S]*?)\s*\}"
        # elif reftype == "eqref":
        #     refpattern = r"\\eqref\s*\{\s*([\s\S]*?)\s*\}"
    
        refpattern = r"\\%s\s*\{\s*([\s\S]*?)\s*\}" % reftype
        
        def processref(matchobj):
            reftag = matchobj.group(0)
            labelstring = re.findall(refpattern, reftag)[0]
            prefix = "Eq. " if reftype == "myeqno" else ""
            return re.sub(refpattern, "%s(%s)" % (prefix, self.labelmap[labelstring]), reftag)
        return processref

    @staticmethod
    def _escape_special(s):
        """
        If s contains escape sequences, then properly escapes them. For
        example, "\text" is converted to "\\text"
        @return: String with properly escaped special characters
        """
        # return "%r" %s
        return s.encode("string_escape")

    def __init__(self, texfile, auxfile):
        """
        Initializes the content of the converter by invoking the read method of the
        readable object
        @param texfile: A readable object containing tex source
        @param auxfile: A readable, .aux file resulting form compilation of the .tex
        source
        @return: None
        """
        self.texfile_name = texfile.name
        self.content = texfile.read()
        self.newcommand_map = self._generate_newcommand_map()
        self.labelmap = self._generate_label_map(auxfile)


        # When starting, modified content is same as original content.
        # Later, as we call different converter methods, the content_modified will be
        # used to store results of latest changes.
        self.content_modified = self.content

    # Following methods are for public consumption
    def extract_text(self):
        """
        Extracts the  between \begin{document} and \end{document}
        @return: None
        """
        try:
            self.content_modified = re.findall(r'\\begin\s*\{\s*document\s*\}(.*)\\end\s*\{\s*document\s*\}',
                                               self.content_modified,
                                               re.DOTALL)[0]
        except:
            pass

    def strip_title_elements(self):
        """
        Strips title elements like title, author etc
        @return: None
        """
        self.content_modified = re.sub( "\\\\title\{.*\}",
                                        "",
                                        self.content_modified,
                                       re.DOTALL)

        self.content_modified = re.sub("\\\\author\{.*\}",
                                       "",
                                       self.content_modified,
                                       re.DOTALL)

    def convert_inline_math(self):
        """
        Converts inline math, i.e. math between $$ tags
        @return: None
        """
        self.content_modified = re.sub("\$(.*?)\$",
                                       '$latex \\1$',
                                       self.content_modified,
                                       count=0)

    def convert_equations(self):
        """
        Processes \begin{equation} environment
        @return: None
        """
        self.content_modified = re.sub(r'\\begin\s*\{\s*equation\s*\}[\s\S]*?\\end\s*\{\s*equation\s*\}',
                                       self._process_equation,
                                       self.content_modified,
                                       re.DOTALL)

    def convert_aligned(self):
        """
        Processes math within \begin{align} tag
        @return: None
        """
        self.content_modified = re.sub(r'\\begin\s*\{\s*align\s*\}[\s\S]*?\\end\s*\{\s*align\s*\}',
                                       self._process_align,
                                       self.content_modified,
                                       re.DOTALL)

    def convert_sections(self):
        """
        Process \section{} tags
        @return: None
        """
        self.content_modified = re.sub(r"\\section\s*\{([\s\S]*?)\}",
                                       "<h4> \\1 </h4>",
                                       self.content_modified,
                                       re.DOTALL)

    def convert_references(self):
        """
        Converts \myeqno{}, \ref{}, and \eqref{} tags
        @return: None
        """
        # Replace all \myeqno{} and \eqref{} tags
        tag_list = ["myeqno", "eqref"]

        for tag in tag_list:
            tag_instances = re.findall(r"\\%s\{.*?\}" % tag, self.content_modified)
            for itag in tag_instances:
                self.content_modified = re.sub(self._escape_special(itag),
                                               self._process_reference(reftype=tag),
                                               self.content_modified,
                                               re.DOTALL)

    def convert_formatting(self):
        """
        Converts formatting tags: {\em...}, {\bf...}, etc
        @return: None
        """

        # Process {\em ...}
        self.content_modified = re.sub(r"\{\s*\\em\s*(.*?)\s*\}",
                                       "<i>\\1</i>",
                                       self.content_modified)

        # Process {\bf ...} tag
        self.content_modified = re.sub(r"\{\s*\\bf\s*(.*?)\s*\}",
                                       "<strong>\\1</strong>",
                                       self.content_modified)

        # Process \href{url}{link text}
        self.content_modified = re.sub(r"\\href\s*\{(.*?)\}\{(.*?)\}",
                                       '<a href="\\1">\\2</a>',
                                       self.content_modified)

    def convert_newcommands(self):
        """
        Replaces custom commands defined by \newcommand{} with standard latex
        @return: None
        """
        for newcommand, std_latex in self.newcommand_map.items():
            # print Converter._escape_special(newcommand), Converter._escape_special(std_latex)
            self.content_modified = re.sub(Converter._escape_special(newcommand),
                                           Converter._escape_special(std_latex),
                                           self.content_modified,
                                           count=0)


    def write_html(self, outfile_name=None):
        """
        Write HTML output
        @return: None
        """
        if not outfile_name:
            outfile_name = re.sub("(.*?)\.tex",
                                  "\\1_wordpress.tex",
                                  self.texfile_name,
                                  re.DOTALL)

        open(outfile_name, "w").write(self.content_modified)