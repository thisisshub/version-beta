import sys, codecs, qrcode, sh
import io
from jinja2 import Template
from urllib.parse import urljoin


# Functions ###################################################################

def main():
    if len(sys.argv) != 4:
        print (u'Usage: {file} <template.svg> <students_list.csv> <base_url>'.format(file=__file__))
        return 1
    
    template_file = sys.argv[1]
    students_list_file = sys.argv[2]
    base_url = sys.argv[3]
    
    for student in get_students_list(students_list_file, base_url):
        svg_file = u'{0}.svg'.format(student['short_name'])
        pdf_file = u'{0}.pdf'.format(student['short_name'])

        print (u'* Generating {0}...'.format(student['url']))
        template2svg(student, template_file, svg_file)
        svg2pdf(svg_file, pdf_file)

def get_students_list(students_list_file, base_url):
    students = []
    with codecs.open(students_list_file, encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            
            student_row = line.split(';')
            student_url = urljoin(base_url, '{0}.pdf'.format(student_row[0]))
            qrcode_img = get_qrcode(student_url)
            qrcode_dataurl = img2dataurl(qrcode_img)
            students.append({
                'short_name': student_row[0],
                'full_name': student_row[1],
                'graduation_date': student_row[2],
                'organization_complement': student_row[3],
                'url': student_url,
                'qrcode_url': qrcode_dataurl
            })
    return students

def get_qrcode(student_url):
    qrcode_img = qrcode.make(student_url, border=0)
    qrcode_img = img_white2transparent(qrcode_img)
    return qrcode_img

def img2dataurl(img):
    output = io.StringIO()
    img.save(output, 'PNG')
    img_base64 = output.getvalue().encode('base64')
    img_dataurl = 'data:image/png;base64,{0}'.format(img_base64)
    return img_dataurl

def img_white2transparent(img):
    img = img.convert("RGBA")
    datas = img.getdata()
    new_data = []
    for item in datas:
        if item[0] == 255 and item[1] == 255 and item[2] == 255:
            new_data.append((255, 255, 255, 0))
        else:
            new_data.append(item)
    img.putdata(new_data)
    return img

def template2svg(student, template_file, svg_file):
    with codecs.open(template_file, encoding='utf-8') as f:
        template = Template(f.read())

    svg_raw = template.render(**student)

    with codecs.open(svg_file, 'w+', encoding='utf-8') as f:
        f.write(svg_raw)

def svg2pdf(svg_file, pdf_file):
    rsvg_convert = sh.Command('rsvg-convert')
    rsvg_convert('-f', 'pdf', '-o', pdf_file, svg_file)

if __name__ == '__main__':
    return_code = main()
    sys.exit(return_code)