def getStringIndex(htmlString, stringToSearch):
    bodyStartIndex = -1
    try:
        bodyStartIndex = htmlString.index(stringToSearch)
    except ValueError:
        return bodyStartIndex
    return bodyStartIndex

class html_parcer:
    def __init__(self, string = '', func_head = (lambda x: x), func_body = (lambda x: x)):
        self._func_head = func_head
        self._func_body = func_body
        head_start = getStringIndex(string, '<head')
        body_start = getStringIndex(string, '<body')
        body_end = getStringIndex(string, '</body>') + 7
        if head_start >= 0 and body_start >= 0 and body_end >= 6:
            self._prefix = string[:head_start]
            self._head = str(string[head_start:body_start])
            self._body = str(string[body_start:])
            self._postfix = str(string[body_end:])#'</html>'

            body_end = getStringIndex(self._body, '</body>')
            self._body = self._body[:(body_end + 7)]
        else:
            self._prefix = ''
            self._head = ''
            self._body = ''
            self._postfix = ''

    def getHTMLString(self):
        return (self._prefix +
                self._func_head(self._head) +
                self._func_body(self._body) +
                self._postfix)