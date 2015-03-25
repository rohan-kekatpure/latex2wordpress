<h3>latex2wordpress</h3>

Posting LaTeX content to Wordpress is a hassle. Even with existing (January 2015) LaTeX support on Wordpress, 
LaTeX content needs to be hand-modified to conform to Wordpress format. Additionally
there is no support for LaTeX labels and references. They need to be inserted by hand. 
If an equation or a reference is added in the text, all the subsequent numbering changes need to performed
manually. The process is manual and unscalable. 

This small project is a tool in converting my LaTeX compositions to a format suitable for copy-pasting to Wordpress. 
The core logic involves extracting various LaTeX tags and replacing or wrapping them with HTML so they are acceptable to 
wordpress. The converter can be extended by adding methods for processing of additional tags. 

<h4>How to use</h4>
The converter consists of two Python files ```latex2wordpress.py``` and ```main.py```. 


<ul>
<li>Go to the folder with your latex source and compile your LaTeX source twice. Theere should be a .aux 
file in the LaTeX source folder </li>
<li>Download the two Python files and place them in any directory</li>
<li>Invoke the LaTeX to Wordpress converter as follows: </li>
</ul>
```python main.py path/to/latexfile.tex path/to/auxfile.aux```
<ul>
<li> The Wordpress-ready file would be available as latexfilename_wordpress.tex </li>
</ul>



<!--Custom LaTeX to Wordpress converters <a href="https://lucatrevisan.wordpress.com/latex-to-wordpress/">exist</a>. 
These are applicable to mathematical publishing and nicely deals with -->
