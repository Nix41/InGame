
import pdfkit 

html = '''<h1 align="center">PyFPDF HTML Demo</h1>
    <p>This is regular text</p>
    <p>You can also <b>bold</b>, <i>italicize</i> or <u>underline</u>
    <img src="/home/nix/Documents/Yasmany/Latest/web/img/Work/Games/5image.jpeg"/>
    '''

pdfkit.from_string(html,'images.pdf') 

