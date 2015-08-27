#!/usr/bin/env python2

from BeautifulSoup import BeautifulSoup
from BeautifulSoup import Tag
import argparse
from xml.dom import minidom

def converter( hhcf ):
    n_slc = (lambda x: x.get(u'name') == u'Name' and not x.findChildren())
    v_slc = (lambda x: x.get(u'name') == u'Local' and not x.findChildren())

    hhcf_dom = BeautifulSoup( hhcf, selfClosingTags=['li'] )

    hhcf_dom.body.name = 'book'

    top_ul = hhcf_dom.ul
    top_ul.name =  "chapters"

    for x in top_ul('ul'):
        obj = x.fetchPreviousSiblings()[0]
        x.fetchPreviousSiblings()[0].fetchPreviousSiblings()[0].extract()
        obj.extract()
        obj = obj.extract()
        
        x.name='sub'
        x['name'] = obj.find( n_slc )['value'].replace("\"",'\\"')
        x['link'] = obj.find( v_slc )['value'].replace("\"",'\\"')

    for x in top_ul('li'):
        obj = x.fetchNextSiblings()[0];
        obj.extract()

        x.name='sub'
        x['name'] = obj.find( n_slc )['value'].replace("\"",'\\"')
        x['link'] = obj.find( v_slc )['value'].replace("\"",'\\"')
    
    return hhcf_dom
    

if __name__ == "__main__":

    parser = argparse.ArgumentParser( description="Parse  .hhc file to .devhelp2 file." )
    parser.add_argument('file1', help='.hcc file')
    parser.add_argument('-o', '--output' , metavar="file2", help='name the output file')
    parser.add_argument('-t', '--title' , default='duck', help='.devhelp2 file\'s title')
    parser.add_argument('-n', '--name' , default='duck', help='.devhelp2 file\'s name?')

    args = parser.parse_args()

    with open( args.file1, 'r' ) as f:
        if args.output :
            filename = args.output
        else:
            filename = 'output.devhelp2'

        with open( filename, 'w+' ) as ff:
            dom = converter( f.read() )
            book = dom.book.extract()
            book.object.extract()

            book['xmlns']=r'http://www.devhelp.net/book'
            book['title']=args.title
            book['name']=args.name
            book['link']='index.html'
            book['author']=""

            dom = '<?xml version="1.0" encoding="utf-8" standalone="no"?>\n'+\
            '<!DOCTYPE book PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "">\n' + book.prettify()

            ff.write( dom )
