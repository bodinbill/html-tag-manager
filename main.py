'''
    JSP script tag splitter.
'''
import os
from common.script_generator import ScriptGenerator, ImageGenerator
from common.script_replacer import ScriptReplacer

WORKSPACE = '/Users/Bodin/projectworkspace'
ROOT_PATH = WORKSPACE + '/FrontProject/webapps'

replacer = ScriptReplacer()


def action(abs_filename):
    if abs_filename.endswith('.jsp') or abs_filename.endswith('.jspf'):
        text = open(abs_filename, 'r').read()
        # generator = ScriptGenerator(
        #   r'((<!--)* *<link (.+)[^>](\/*>|>\n*<\/link>))', r'href\n*=\n*[\'"](.+\.png\S*)[\'"] *',
        #    'icon', '%s<r:icon src="%s" />')

        generator = ImageGenerator(
            r'((<!--)? *([\'"].*)?<img([\w\W]+?)\/?>)', r'(\S+\n*=\n*[\'"][\w\W]+[\'"])? *src\n*=\n*[\'"](.+\.(jpg|png|jpeg|gif|tiff|ico)\S*)[\'"] *(\S+\n*=\n*[\'"][\w\W]+[\'"])?',
            'img', '%s<r:image src="%s" attr="%s" />')

        script_texts = generator.run(text)
        replacer.replace(text, script_texts, abs_filename)


for (dirpath, dirnames, filenames) in os.walk(ROOT_PATH):
    for filename in filenames:
        abs_filename = os.sep.join([dirpath, filename])
        action(abs_filename)

print 'DONE.'
