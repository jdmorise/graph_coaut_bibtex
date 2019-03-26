
# Version 0.25 of bibtex graph visualizer

# Contact: jdmorise a t yahoo.com

# Copyright (c) 2015-2016, Benjamin Laemmle
# 

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

#------------------------------------------------------------------------------------------------------------------------------
# Changelog: 
# v0.25: 
#        Bug Fix of graph generation
#        
# 
#------------------------------------------------------------------------------------------------------------------------------
# v0.24: 
#        Added level and years (before and after) for reduction of the graph. 
#        Fixed Bug for Calculation of number o publications with timed filters
# 

import argparse
import sys
import bibtexparser
from bibtexparser.bparser import BibTexParser
from bibtexparser.customization import convert_to_unicode

import pygraphviz as pgv




#  Authors class
class Authors (object): 
    
    def __init__ (self,main_author_first,main_author_sur):
        # The list of authors
        self.list_of_authors = [{'surname':main_author_sur,'firstname':main_author_first,'hfactor':0,'noPub':0,'relations': 0,'level':0}]
        # The list of relations
        self.list_of_relations = []
        self.rel_max = 0
        self.before = 3000
        self.after = 1900
        self.article_fact = 1
        self.proc_fact = 1
        self.book_fact = 1

        
    def author_append (self, this_surname, this_firstname ): 
        append_bool = 1
        for idx in range (0,len(self.list_of_authors)) :
            idx_surname = self.list_of_authors[idx]['surname']
            idx_firstname = self.list_of_authors[idx]['firstname']
            # if Name already exists in database, do not add it
            if this_surname in idx_surname and this_firstname[0] in idx_firstname : 
                append_bool = 0
                # if firstname in database is shorter than this_firstname, replace it
                if len(this_firstname) > len(idx_firstname):
                    self.list_of_authors[idx]['firstname'] = this_firstname
        if append_bool > 0 :
            self.list_of_authors.append({'surname':this_surname,'firstname':this_firstname,'hfactor':0,'noPub':0, 'relations': 0, 'level': 256})

        
#------------------------------------------------------------------------------------------------
    def create_author_list (self,bib_database): 
        for articles in bib_database.entries:

            authors_of_article = articles['author']
            # If Authors are delimited by ' and '
            if ' and ' in authors_of_article: 
                full_names = authors_of_article.split(' and ')

                for s_aut in full_names:
                    # Format Nikneijad, Ali M.
                    if ', ' in s_aut : 
                        names = s_aut.split(', ')
                        this_surname = names[0]
                        this_firstname = names[1]
                    # Format Ali M. Nikneijad 
                    else :
                        names = s_aut.split(' ') 
                        this_firstname = names[0]
                        this_surname = names[-1] # last element
                        if len(names)>2 :
                            for x in range (1,len(names)-1):
                                this_firstname = this_firstname + ' ' + names[x]  
                    # Check if author is already in list, otherwise append 
                    self.author_append( this_surname, this_firstname ) 

            elif '.,' in authors_of_article:

                full_names = authors_of_article.split('.,')
                for s_aut in full_names:
                    names = s_aut.split(', ')

                    if len(names) > 1 : # Check if names is empty
                        this_surname = names[0]
                        this_firstname = names[1]
                        if this_firstname[-1] is not '.' : 
                            this_firstname = this_firstname + '.'


                    self.author_append( this_surname, this_firstname ) 

            elif ',' in authors_of_article: 
                full_names = authors_of_article.split(',')
                for i in range(0,len(full_names)/2) :
                    this_surname = full_names[2*i].strip()
                    this_firstname = full_names[2*i+1].strip()

                    self.author_append( this_surname, this_firstname ) 

        print('No of Authors: ' + str(len(self.list_of_authors)))

        
    # -----------------------------------------------------------------------------
    def create_relations ( self, bib_database ) : 
        
        length = len(self.list_of_authors)    
        
        for i in range (0,length):
            aut_name_i = self.list_of_authors[i]['surname'] + ', ' + self.list_of_authors[i]['firstname'][0]
            lvl_i = self.list_of_authors[i]['level']
                        
            # increase number of publications for author
            for articles in bib_database.entries:
                if aut_name_i in articles['author'] and self.before > int(articles['year']) > self.after:
                    self.list_of_authors[i]['noPub'] += 1
                    
            # In my old script version, J was iterated from i (instead i+1).
            # This was not a problem with the old script, as the self- nodes were removed (or not drawn). 
            
            for j in range(i+1,length):
                this_firstname = self.list_of_authors[j]['firstname']
                this_surname = self.list_of_authors[j]['surname']
                aut_name_j = this_surname + ', ' + this_firstname[0]
                rel = 0
                
                lvl_j = self.list_of_authors[j]['level']
                
                for articles in bib_database.entries:
                    if aut_name_i in articles['author'] and aut_name_j in articles['author'] and self.before > int(articles['year']) > self.after:
                       
                        rel = rel + 1
                        
                        if lvl_i < lvl_j:
                            lvl_j = lvl_i + 1
                        elif  lvl_i > lvl_j :
                            lvl_i = lvl_j + 1
                            
                self.list_of_authors[i]['level'] = lvl_i
                self.list_of_authors[j]['level'] = lvl_j
              

                if rel > 0:
                    self.list_of_relations.append([i,j,rel])
                    self.list_of_authors[i]['relations'] += rel
                    self.list_of_authors[j]['relations'] += rel
                    
                    # increase counter for maximum relationshsip number
                    if rel > self.rel_max: 
                        self.rel_max = rel


        print('No of relations: ' + str(len(self.list_of_relations)))  

        
#------------------------------------------------------------------------------------------------

class AuthorsGraph(pgv.AGraph):
    def __init__(self):
        # colors
        self.my_colorscheme = 'X11'
        self.node_fill_color = 'deepskyblue2'
        self.node_outline_color = 'navy'
        self.edge_color = 'firebrick'
        self.node_font_color = 'navy'
        self.aut_pub_thr = 1
        self.aut_edge_thr = 1
        self.edge_rel_thr = 1
        self.level = 1
        self.before = 0
        self.after = 0
        super(AuthorsGraph,self).__init__(strict=False, directed=False, splines=True, style='filled', colorscheme=self.my_colorscheme)
        
        

    def add_author_nodes(self,This_Authors):
        print('Add Nodes to Graph')
        for idx in range(0,len(This_Authors.list_of_authors)):
            if This_Authors.list_of_authors[idx]['noPub'] >= self.aut_pub_thr and This_Authors.list_of_authors[idx]['level'] <= self.level:
                graph_label = This_Authors.list_of_authors[idx]['surname'] + '&#92;n' + This_Authors.list_of_authors[idx]['firstname'] + '&#92;n' + str(This_Authors.list_of_authors[idx]['noPub'])

                self.add_node(idx, label=graph_label)
                self.node_attr.update(style='filled', color=self.node_outline_color, penwidth=3, fillcolor=self.node_fill_color, fontcolor=self.node_font_color)
                # print This_Authors.list_of_authors[idx]['surname'] + ' ' + This_Authors.list_of_authors[idx]['firstname'] + ' ' + str(This_Authors.list_of_authors[idx]['level'])
            
    #------------------------------------------------------------------------------------------------
    def add_author_edges(self,This_Authors): 
        print('Add Edges to Graph')
        print('Add Edges to Graph')
        for rel in This_Authors.list_of_relations:
            if rel[2] >= self.edge_rel_thr and self.has_node(rel[0]) and self.has_node(rel[1]):
                rel_width = float(rel[2]) / This_Authors.rel_max*4 + 1
                self.add_edge(rel[0],rel[1],label=rel[2],weigth = rel[2], dir='none', penwidth=rel_width, color=self.edge_color )

    #------------------------------------------------------------------------------------------------
    def remove_author_nodes(self): 

        print('Compact Graph')
        remove = [node for node in self.nodes() if self.degree(node) < self.aut_rel_thr]
        self.remove_nodes_from(remove)    
        print('Remaining Nodes: ' + str(self.number_of_nodes()))
        print('Remaining Edges: ' + str(self.number_of_edges()))

#------------------------------------------------------------------------------------------------

def main():
    
    
    G = AuthorsGraph()

    usage = """"Examples: """

    parser = argparse.ArgumentParser(usage=usage)
    parser.add_argument('-if','--input_filename', help='Filename of publication database in bibtex format')
    parser.add_argument('-gf','--graph_filename', default = 'graph.png', help='Filename of graph output stored as png')
    parser.add_argument('-ma','--main_author_name', default='Max Mustermann')
    parser.add_argument('-ert','--edge_relation_thres', type=int, default=1, help='Only add edges with ERT or more number of relations')
    parser.add_argument('-art','--author_relation_thres', type=int, default=1, help='Only add authors with ART or more number of relations')
    parser.add_argument('-apt','--author_publication_thres', type=int, default=1, help='Only add authors with APT number of publications')
    parser.add_argument('-lvl','--level', type=int, default=256)
    parser.add_argument('-b', '--before', type=int, default = 2050,help='Only use Publications before YEAR for the graph')
    parser.add_argument('-a', '--after', type=int, default = 1900,help='Only use Publications after YEAR for the graph')
    

    parser.add_argument('-gp','--graph_programm', default = 'fdp', help="""Graph Programm for rendering the graph. one of the following: fdp,dot,sfdp,circo,twopi.""")  

    print("""A Graph Display Software for bibtex databases
    Copyright (C) 2015 Benjamin Laemmle, jdmorise a t yahoo.com
    
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
    
    """)

    if len(sys.argv) == 1:
        parser.print_help()
        return 1
    else : 

        args = parser.parse_args()


        # thresholds
        G.edge_rel_thr = args.edge_relation_thres
        G.aut_rel_thr = args.author_relation_thres
        G.aut_pub_thr = args.author_publication_thres
        G.level = args.level

        MyParser = BibTexParser()
        MyParser.customization = convert_to_unicode
        
        print('Inputfile: ' + args.input_filename)

        with open(args.input_filename) as bibtex_file:
            bib_database = bibtexparser.load(bibtex_file,parser=MyParser)

        # construct array of authors
        # 
        
        main_author_name = args.main_author_name.split(' ')
        
        MyAuthors = Authors(main_author_name[0],main_author_name[-1])
        
        MyAuthors.after = args.after
        MyAuthors.before = args.before

        MyAuthors.create_author_list (bib_database)

        # construct array of relationsships
        MyAuthors.create_relations (bib_database)

        # Add Nodes to Graph
        G.add_author_nodes(MyAuthors)

        # Add Edges to Graph
        G.add_author_edges(MyAuthors)

        # remove nodes with no connection
        G.remove_author_nodes()

        print('Render Graph')
        G.write('debug.dot')

        G.layout(prog=args.graph_programm)
        G.draw(args.graph_filename)
        print('Graph file written to: ' + args.graph_filename)
        return 0

if __name__ == "__main__":
    sys.exit(main())
