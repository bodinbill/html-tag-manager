'''
    JSP script tag splitter.
'''
import re


class ScriptGenerator:
    def __init__(self, tag_pattern, src_pattern, attr_name, output_template):
        self.tag_pattern = tag_pattern
        self.src_pattern = src_pattern
        self.attr_name = attr_name
        self.output_template = output_template

    def run(self, text):
        script_texts = []
        matches = re.findall(self.tag_pattern, text)

        def validate(script):
            for i in ['"', "'"]:
                if script.startswith(i) or script.endswith(i):
                    return False
            return True

        if len(matches):
            for m in matches:
                originScript = self.gen_tag(m)
                script = originScript.replace('\r\n', '').replace(
                    '\n', '').replace('\t', '').strip()
                script = ' '.join(script.split())

                if not validate(script):
                    continue

                attrs = re.findall(self.src_pattern, script)

                if len(attrs):
                    src = self.gen_src(attrs)

                    varText = ''
                    srcText = src

                    if src.count('%'):
                        varText = '%s\n' % self.set_var(
                            '_%sSrcText' % self.attr_name, src)
                        srcText = '${_%sSrcText}' % self.attr_name

                    self.append(script_texts, originScript,
                                self.gen_text(attrs, varText, srcText))

        return script_texts

    def append(self, script_texts, script, script_text):
        script_texts.append((script, script_text))

    def set_var(self, varName, value):
        return '<c:set var="%s">%s</c:set>' % (varName, value)

    def gen_tag(self, m):
        return m[0]

    def gen_src(self, attrs):
        return attrs[0]

    def gen_text(self, attrs, varText, srcText):
        return self.output_template % (varText, srcText)


class ImageGenerator(ScriptGenerator):
    def __init__(self, tag_pattern, src_pattern, attr_name, output_template):
        ScriptGenerator.__init__(
            self, r'((<!--)? *([\'"]\s*(<.*>)?)?<img([\w\W]+?)[^%]>)',
            r'(\S+\n*=\n*[\'"][\w\W]+[\'"])? *src\n*=\n*[\'"](.+\.(jpg|png|jpeg|gif|tiff|ico)\S*)[\'"] *(\S+\n*=\n*[\'"][\w\W]+[\'"])?',
            'img', '%s<r:image src="%s" attr="%s" />')

    def gen_src(self, attrs):
        return attrs[0][1]

    def gen_tag(self, m):
        return m[0]

    def gen_text(self, attrs, varText, srcText):
        altText = ' '.join([attrs[0][0].strip(), attrs[0][3].strip()])
        altText = altText.replace(' alt=""', "").strip()

        if altText.count('%'):
            varText += '%s\n' % self.set_var(
                '_%sAttrText' % self.attr_name, altText)
            altText = '${_%sAttrText}' % self.attr_name
        else:
            altText = altText.replace('"', '\\"')

        output = self.output_template % (varText, srcText, altText)

        return output.replace(' attr=""', "")


class HtmlImageGenerator(ScriptGenerator):
    def __init__(self):
        ScriptGenerator.__init__(
            self, r'((<!--)? *([\'"]\s*(<.*>)?)?<img([\w\W]+?)[^%]>)',
            r'(\S+\n*=\n*[\'"][\w\W]+[\'"])? *src\n*=\n*[\'"](.+\.(jpg|png|jpeg|gif|tiff|ico)\S*)[\'"] *(\S+\n*=\n*[\'"][\w\W]+[\'"])?',
            'html', '<img src="//promo.11thcdn.com%s" %s/>')

    def gen_src(self, attrs):
        return attrs[0][1]

    def gen_tag(self, m):
        return m[0]

    def gen_text(self, attrs, varText, srcText):
        altText = ' '.join([attrs[0][0].strip(), attrs[0][3].strip()])
        altText = altText.replace(' alt=""', "").strip()

        if len(altText) > 0:
            altText += ' '
        return self.output_template % (srcText, altText)


class JavascriptGenerator(ScriptGenerator):
    def __init__(self):
        ScriptGenerator.__init__(
            self, r'((<!--)* *<script ([^ ]+)(\/>|>.*<\/script>))',
            r'src\n*=\n*[\'"](.+\.js\S*)[\'"] *(charset=[\'"]\S+[\'"])* *(async)* *(defer)*',
            'script', '%s<r:register-js src="%s" alt="%s"/>')

    def gen_src(self, attrs):
        return attrs[0][0]

    def gen_text(self, attrs, varText, srcText):
        altText = ' '.join(attrs[0][1:]).strip()

        output = self.output_template % (varText, srcText, altText)

        return output.replace(' alt=""', "")
