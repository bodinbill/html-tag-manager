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
                script = self.gen_tag(m).replace('\r\n', '').replace('\n', '').replace('\t', '').strip()
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
                    
                    self.append(script_texts, script, self.gen_text(attrs, varText, srcText))

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
            self, tag_pattern, src_pattern, attr_name, output_template)

    def gen_src(self, attrs):
        return attrs[0][1]

    def append(self, script_texts, script, script_text):
        if script_text.count('%'):
            print '%%%%', script_text
        else:
            script_texts.append((script, script_text))

    def gen_text(self, attrs, varText, srcText):
        altText = ' '.join([attrs[0][0].strip(), attrs[0][3].strip()])
        altText = altText.replace(' alt=""', "").replace('"', '\\"').strip()
        
        output = self.output_template % (varText, srcText, altText)
        
        return output.replace(' attr=""', "")


if __name__ == "__main__":
    generator = ImageGenerator(
        r'((<!--)? *([\'"].*)?<img([\w\W]+?)\/?>)', r'(\S+\n*=\n*[\'"][\w\W]+[\'"])? *src\n*=\n*[\'"](.+\.(png)\S*)[\'"] *(\S+\n*=\n*[\'"][\w\W]+[\'"])?',
        'img', '%s<r:register-img src="%s" attr="%s" />')

    html = '''

    <img class="logo" style="padding: 0" src="/img/test.png" alt="text message">

    <img class="logo" style="padding: 0" 
    
        src="/img/test.png" 
        alt="text message">

    <img src="/img/test.png" alt="">

    <script>
        += \'<img src="/img/test.png">\'
        += \'<a href=""><img src="/img/test.png"></a>\'
    </script>
                <div class="mycell5">
					<img alt="Step 2" src="/img_glb/promotion/global11/img_step2.png" />
					<div class="step_title">STEP 2</div>
					<div class="step_des">Shop at 11street</div>
				</div>
    '''

    scripts = generator.run(html)

    for data in scripts:
        print '------'
        print data[0]
        print data[1]
