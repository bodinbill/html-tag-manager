'''
    JSP script tag splitter.
'''
import os
from common.script_generator import JavascriptGenerator, ScriptGenerator, ImageGenerator, HtmlImageGenerator
from common.script_replacer import ScriptReplacer

WORKSPACE = '/Users/Bodin/projectworkspace'
ROOT_PATH = WORKSPACE + '/FrontProject/webapps'

replacer = ScriptReplacer(True)


def action(abs_filename):
    if abs_filename.endswith('.jsp') or abs_filename.endswith('.jspf'):
        text = open(abs_filename, 'r').read()
        # generator = ScriptGenerator(
        #    r'((<!--)* *<link (.+)[^>](\/*>|>\n*<\/link>))', r'href\n*=\n*[\'"](.+\.png\S*)[\'"] *',
        #    'icon', '%s<r:icon src="%s" />')
        # generator = ImageGenerator()
        # generator = HtmlImageGenerator()

        generator = JavascriptGenerator()

        script_texts = generator.run(text)
        replacer.replace(text, script_texts, abs_filename)


for (dirpath, dirnames, filenames) in os.walk(ROOT_PATH):
    for filename in filenames:
        abs_filename = os.sep.join([dirpath, filename])
        action(abs_filename)

print 'DONE.'
