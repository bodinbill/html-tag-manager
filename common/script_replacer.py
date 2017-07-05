'''
    Script replacer.
'''
import re

class ScriptReplacer:
    def __init__(self):
        pass

    def replace(self, text, script_texts, abs_filename):
        replace = False
        for script_text in script_texts:
            if not script_text[0].count('--'):
                text = text.replace(script_text[0], script_text[1])
                replace = True
            else:
                print script_text[0]

        f = open(abs_filename, 'w')
        f.write(text)
        f.close()

        if replace:
            lines = open(abs_filename, "r").readlines()

            new_lines = []
            allow = False
            wait = False
            wrote = False
            for line in lines:
                if line.count('<r:register') and not wrote:
                    if text.count('/WEB-INF/tld/resource.tld') == 0:
                        new_lines.append(
                            '<%@ taglib prefix="r" uri="/WEB-INF/tld/resource.tld" %>\n')
                    if text.count('http://java.sun.com/jsp/jstl/core') == 0:
                        new_lines.append(
                            '<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>\n')
                    allow = True
                    wrote = True
                if not allow and re.match(r'.+contentType.+UTF-8.+', line):
                    if not line.count('%>'):
                        wait = True
                    allow = True
                elif allow and wait:
                    wait = line.count('%>') == 0
                elif allow and not wrote:
                    if text.count('/WEB-INF/tld/resource.tld') == 0:
                        new_lines.append(
                            '<%@ taglib prefix="r" uri="/WEB-INF/tld/resource.tld" %>\n')
                    if text.count('http://java.sun.com/jsp/jstl/core') == 0:
                        new_lines.append(
                            '<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>\n')
                    wrote = True
                new_lines.append(line)

            with open(abs_filename, "w") as f:
                if not wrote:
                    f.write(
                        '<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>\n')
                    f.write(
                        '<%@ taglib prefix="r" uri="/WEB-INF/tld/resource.tld" %>\n')
                    wrote = True

                    if text.count('http://java.sun.com/jsp/jstl/core') == 0:
                        f.write(
                            '<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>\n')
                        print '****', abs_filename
                    if re.match(r'.+contentType.+UTF-8.+', text):
                        print 'problem', abs_filename

                for line in new_lines:
                    f.write(line)
