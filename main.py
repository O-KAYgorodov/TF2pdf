#!/usr/bin/python3

import sys, getopt, pdfkit, time
from urllib.request import urlopen
from urllib.error import HTTPError
from html_parcer import html_parcer, getStringIndex

def gethtmltextfromlink(link):
    print('Downloading from source ' + link)
    return ((urlopen(link)).read()).decode("utf-8")#ret_val

def startTFRecurcive(htmlbodystring):
    return '<body>' + recurciveTFContentExtractor(htmlbodystring, 'main')[0] + '</body>' #add info from end of page to the end

def recurciveTFContentExtractor(htmlbodystring, div_name ='', link_dict = {}):
    #extracts content

    # head_string - head section of html. Writes ones
    # page_header - h1 tag of section (current web page)
    # page_content - content of current page
    # link_name - name for internal linking

    # finds <h1 itemprop="name" class="devsite-page-title">
    page_header = str(htmlbodystring[getStringIndex(htmlbodystring, '<h1 itemprop="name" class="devsite-page-title">'):
                             (getStringIndex(htmlbodystring, '</h1>') + 5)])
    # finds <div class="devsite-article-body clearfix
    page_content = str(htmlbodystring[getStringIndex(htmlbodystring, '<div class="devsite-article-body clearfix'):
                              getStringIndex(htmlbodystring, '<div class="devsite-content-footer nocontent">')])

    # get name from h1 without spaces
    link_name = div_name
    to_top = ''
    page_header_list = page_header.split('\n')
    if link_name == '':
        link_name = page_header_list[1]
        while link_name.startswith(' '):
            link_name = link_name[1:]
        a = getStringIndex(link_name, ' ')
        while a >= 0:
            b = list(link_name)
            b[a] = '_'
            link_name = "".join(b)
            a = getStringIndex(link_name, ' ')
        to_top = '<a href="#main" class="pb_after">To top</a>'

    page_header_list[0] = page_header_list[0][:-1] + ' id="' + link_name + '">'

    page_header = ''
    for i in range(len(page_header_list)):
        page_header += (page_header_list[i] + '\n')

    page_content = (page_header + page_content)#.lower()

    #working with links
    add_after = ''
    start_link_tag = 0
    try:
        while 1:
            #search for <a> tag
            start_link_tag = page_content.index('<a ', (start_link_tag + 1))
            end_link_tag = page_content.index('>', start_link_tag)
            #get link from tag
            start_link = page_content.index('href="', start_link_tag, end_link_tag) + 6
            end_link = page_content.index('"', start_link, end_link_tag)
            link = page_content[start_link:end_link]
            # exclude internal links with #
            try:
                link = link[:(link.index('#'))]
            except ValueError:
                link = link
            # replace outer link to internal
            # conditition -> curr_link[:(len(preffered_link))] == preffered_link
            # check for the case when preffered_link == ''
            if (link[:36] == 'https://www.tensorflow.org/api_docs/'):
                new_link = link_dict.get(link)
                if new_link == None:
                    link_dict[link] = link
                    tries = 10
                    sleep = 0.01
                    while tries > 0:
                        try:
                            ret_val = recurciveTFContentExtractor(gethtmltextfromlink(link),
                                                                  link_dict=link_dict)
                            #print('Success!')
                        except HTTPError:
                            tries -= 1
                            if tries == 0:
                                new_link = link
                            else:
                                time.sleep(sleep)
                                sleep *= 2
                            #print('Error downloading. Try again. Last ' + str(tries) + ' tries')
                            continue
                        else:
                            add_after += ret_val[0]
                            new_link = '#' + ret_val[1]
                            link_dict = ret_val[2]
                            link_dict[link] = new_link
                            page_content = page_content[:start_link] + new_link + page_content[end_link:]
                            break
    except ValueError:
        # if .index doesn't find <a> tag anymore
        page_content += (to_top + add_after)

    return (page_content, link_name, link_dict)

def main(argv):
    name = argv[0]
    argv = argv[1:]
    if argv == []:
        print(name +
              ' --url <link to page> -o <outputfile>\n' +
              '[--css <css file>]\n' +
              '[--page-size <page size to print (A4 for default)>]')
        sys.exit(2)
    outputfile = ''
    page_size = 'A4'
    url = ''
    css = ''

    try:
        opts, args = getopt.getopt(argv, "ho:p:", ["of=", "ofile=", "url=", "css=", "page-size="])
    except getopt.GetoptError:
        print(name +
              ' --url <link to page> -o <outputfile>\n' +
              '[--css <css file>]\n' +
              '[--page-size <page size to print (A4 for default)>]')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h' or opt == '--help':
            print(name +
                  ' --url <link to page> -o <outputfile>\n' +
                  '[--css <css file>]\n' +
                  '[--page-size <page size to print (A4 for default)>]')
            sys.exit()
        elif opt in ("-o", "--ofile"):
            outputfile = arg
        elif opt in ('--url'):
            url = arg
        elif opt in ('--css'):
            css = arg
        elif opt in ('--page-size'):
            page_size = arg

    try:
        string = gethtmltextfromlink(url)
    except HTTPError and ValueError:
        string = ''

    if string != '':
        main_page = html_parcer(string, func_body=startTFRecurcive)
        htmlStr = main_page.getHTMLString()

        options = {
            'page-size': page_size,
            'margin-top': '0.75in',
            'margin-right': '0.75in',
            'margin-bottom': '0.75in',
            'margin-left': '1.0in',
        }
        pdfkit.from_string(htmlStr, outputfile, options=options, css=css)

if __name__ == "__main__":
    main(sys.argv)
