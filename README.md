# graph_coaut_bibtex
Graph Display Software for Author Relationships with Bibtex Files   
(c) 2015-2019 JD Morise   
jdmorise a t yahoo dot com   

### Introduction to funtionality on my blog: 
https://onmenwhostareongraphs.wordpress.com/2015/06/09/graph-display-software-for-author-relationships-with-bibtex-files/   
https://onmenwhostareongraphs.wordpress.com/category/visualization-of-author-relationships/   

### Installation Requirements:    
Python    
Graphviz - https://www.graphviz.org/   
Pygraphviz - http://pygraphviz.github.io/documentation/pygraphviz-1.5/download.html#documentation   
bibtexparser - https://bibtexparser.readthedocs.io/en/master/index.html   



### Examples (with provided example.bib) 
python graph_coaut_bibtex.py -if example.bib -gf graph_red.png -ma "A. Mirzaei" -lvl 1  -apt 3 -ert 3   
python graph_coaut_bibtex.py -if example.bib -gf graph_plain.png    


### Commandline Arguments: 
python graph_coaut_bibtex.py --help   

    A Graph Display Software for bibtex databases
    Copyright (C) 2015-2019 JD Morise, jdmorise a t yahoo.com
    
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>. 
    
    
usage: "Examples:    

optional arguments:   
  -h, --help            show this help message and exit   
  -if INPUT_FILENAME, --input_filename INPUT_FILENAME   
                        Filename of publication database in bibtex format   
  -gf GRAPH_FILENAME, --graph_filename GRAPH_FILENAME   
                        Filename of graph output stored as png   
  -ma MAIN_AUTHOR_NAME, --main_author_name MAIN_AUTHOR_NAME   
  -ert EDGE_RELATION_THRES, --edge_relation_thres EDGE_RELATION_THRES   
                        Only add edges with ERT or more number of relations   
  -art AUTHOR_RELATION_THRES, --author_relation_thres AUTHOR_RELATION_THRES   
                        Only add authors with ART or more number of relations   
  -apt AUTHOR_PUBLICATION_THRES, --author_publication_thres AUTHOR_PUBLICATION_THRES   
                        Only add authors with APT number of publications   
  -lvl LEVEL, --level LEVEL   
  -b BEFORE, --before BEFORE   
                        Only use Publications before YEAR for the graph   
  -a AFTER, --after AFTER   
                        Only use Publications after YEAR for the graph   
  -gp GRAPH_PROGRAMM, --graph_programm GRAPH_PROGRAMM   
                        Graph Programm for rendering the graph. one of the following: fdp,dot,sfdp,circo,twopi.   
