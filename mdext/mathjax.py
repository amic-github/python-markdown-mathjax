

import markdown

class MathJaxPattern(markdown.inlinepatterns.Pattern):

    def __init__(self):
        markdown.inlinepatterns.Pattern.__init__(self,r'(?<!\\)'
                                                      r'(\$\$|\$|\\\[|\\\(|\\begin\{(.+?)\})'
                                                      r'(.*?)(?<!\\)'
                                                      r'(\2|\\\]|\\\)|\\end\{\3\})')
        # Cannot manage to match \\$a$ correctly with a simple regexp.

    def handleMatch(self, m):
        node = markdown.util.etree.Element('mathjax')
        node.text = markdown.util.AtomicString(m.group(2) + m.group(4) + m.group(5))
        return node

class MathJaxPostprocessor(markdown.postprocessors.Postprocessor):
    def run(self, text):
        text = text.replace('<mathjax>', '')
        text = text.replace('</mathjax>', '')
        return text
        

class MathJaxExtension(markdown.Extension):
    def extendMarkdown(self, md, md_globals):
        # Needs to come before escape matching because \ is pretty important in LaTeX
        md.inlinePatterns.add('mathjax', MathJaxPattern(), '<escape')
        md.postprocessors['mathjax'] = MathJaxPostprocessor(md)

        

def makeExtension(configs=None):
    return MathJaxExtension(configs)


