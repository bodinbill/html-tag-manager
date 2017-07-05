'''
    Test script generator.
'''
from script_generator import ImageGenerator
import unittest


class ImageGeneratorTest(unittest.TestCase):
    def setUp(self):
        self.underTest = ImageGenerator(
            r'((<!--)? *([\'"]\s*(<.*>)?)?<img([\w\W]+?)[^%]>)',
            r'(\S+\n*=\n*[\'"][\w\W]+[\'"])? *src\n*=\n*[\'"](.+\.(jpg|png|jpeg|gif|tiff|ico)\S*)[\'"] *(\S+\n*=\n*[\'"][\w\W]+[\'"])?',
            'img', '%s<r:register-img src="%s" attr="%s" />')

    def test_basic(self):
        html = '''
<img class="logo" style="padding: 0" src="/img/test.png" alt="text message">

        <img class="logo" style="padding: 0" 
        
            src="/img/test.png" 
            alt="text message">

        <img src="/img/test.png" alt="">

        <ul>
                <li name="subtit-a"><img src="/img_glb/mini/admin/thumb/subjbar_default01.gif" alt="umum1"></li>
            </ul>
        '''

        scripts = self.underTest.run(html)

        self.assertEquals(len(scripts), 4)
        self.assertEquals(
            scripts[0][1], '<r:register-img src="/img/test.png" attr="class=\\"logo\\" style=\\"padding: 0\\" alt=\\"text message\\"" />')
        self.assertEquals(
            scripts[1][1], '<r:register-img src="/img/test.png" attr="class=\\"logo\\" style=\\"padding: 0\\" alt=\\"text message\\"" />')
        self.assertEquals(
            scripts[2][1], '<r:register-img src="/img/test.png" />')
        self.assertEquals(
            scripts[3][1], '<r:register-img src="/img_glb/mini/admin/thumb/subjbar_default01.gif" attr="alt=\\"umum1\\"" />')

    def test_script(self):
        html = '''
            <script>
                += \'<img src="/img/test.png">\'
                += \'<a href=""><img src="/img/test.png"></a>\'
                += \'   <img src="/img/test.png">\'
                += \'\t<img src="/img/test.png"> \'
                
            </script>
        '''

        scripts = self.underTest.run(html)

        self.assertEquals(len(scripts), 0)

    def test_script_attr_override(self):
        html = '''
            <img class="logo" src="/img/test.png" alt="<%=globalMessage %>">

            <img class="logo" src="/img/test.png">
            
        '''

        scripts = self.underTest.run(html)
        self.assertEquals(len(scripts), 2)
        self.assertEquals(
            scripts[0][0], '<img class="logo" src="/img/test.png" alt="<%=globalMessage %>">')
        self.assertEquals(
            scripts[0][1], '<c:set var="_imgAttrText">class=\\"logo\\" alt=\\"<%=globalMessage %>\\"</c:set>\n' +
            '<r:register-img src="/img/test.png" attr="${_imgAttrText}" />')
        self.assertEquals(
            scripts[1][0], '<img class="logo" src="/img/test.png">')
        self.assertEquals(
            scripts[1][1], '<r:register-img src="/img/test.png" attr="class=\\"logo\\"" />')

    def test_script_advance(self):
        html = '''
            <div><img class="logo" src="<%=baseUrl %>/img/test.png" alt="<%=globalMessage %>">
            </div>
        '''
        scripts = self.underTest.run(html)
        self.assertEquals(len(scripts), 1)
        self.assertEquals(
            scripts[0][0], '<img class="logo" src="<%=baseUrl %>/img/test.png" alt="<%=globalMessage %>">')
        self.assertEquals(scripts[0][1], '<c:set var="_imgSrcText"><%=baseUrl %>/img/test.png</c:set>\n' +
                          '<c:set var="_imgAttrText">class=\\"logo\\" alt=\\"<%=globalMessage %>\\"</c:set>\n' +
                          '<r:register-img src="${_imgSrcText}" attr="${_imgAttrText}" />')


if __name__ == "__main__":
    unittest.main()
