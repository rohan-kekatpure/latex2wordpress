### latex2wordpress: Make your LaTeX docs Wordpress-ready

Posting LaTeX content to Wordpress is a hassle. Even with existing (January 2015) LaTeX support on Wordpress, 
LaTeX content needs to be hand-modified to conform to Wordpress format. Additionally
there is no support for LaTeX labels and references. They need to be inserted by hand. 
If an equation or a reference is added in the text, all the subsequent numbering changes need to performed
manually. The process is manual and unscalable for larger documents. 

```latextowordpress``` is a tool for converting LaTeX compositions to a format suitable for copy-pasting to Wordpress. 
The core logic involves extracting various LaTeX tags and replacing or wrapping them with HTML so they are acceptable to 
wordpress. The converter can be extended by adding methods for processing of additional tags. 

### Usage
The converter consists of two Python files `latex2wordpress.py` and `main.py`. 

 1. Download the two Python files and place them in any directory

 2. Go to the folder with your latex source and compile your LaTeX source twice. This should 
 generate a `.aux` file in the LaTeX source folder
 
 3. Invoke the LaTeX to Wordpress converter:

 `python l2wp.py latexfile.tex latexfile.aux`

 If `l2wp.py` is not in your path, then you have to provide complete path to it. 

The Wordpress-ready file would be available as ```latexfilename_wordpress.tex``` 


### Rules for composing LaTeX files for accurate conversion to wordpress format


<!--Custom LaTeX to Wordpress converters <a href="https://lucatrevisan.wordpress.com/latex-to-wordpress/">exist</a>. 
These are applicable to mathematical publishing and nicely deals with -->
