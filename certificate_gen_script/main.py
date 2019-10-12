from PIL import Image, ImageFont, ImageDraw
import gspread, oauth2client
from oauth2client.service_account import ServiceAccountCredentials

"""
link to the form: https://forms.gle/n23sWnecnGvJ4V4K6
save the image 

"""

scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('/home/shub/devel/personal/version-beta/certificate_gen_script/macro-dogfish-238009-6417513b1b38.json', scope)
client = gspread.authorize(creds)

sheet = client.open('Certificate_Registration (Responses)').sheet1
data = sheet.get_all_values()

image = Image.open('/home/shub/devel/personal/version-beta/images/blank_cert_template.jpg')
draw = ImageDraw.Draw(image)

#font declaration
font = ImageFont.truetype('/home/shub/devel/personal/version-beta/certificate_gen_script/fonts/OpenSans-Bold.ttf', size=45)

for candidate in range(2, sheet.row_count):
    candidate_name = sheet.row_values()

    


for date in sheet.col_values(1):
    (x,y) = 106,327
    color = 'rgb(0,0,0)'
    draw.text((x,y), date, fill=color, font=font)

for name_of_organisation in sheet.col_values(2):
    (x, y) = 50,50
    color = 'rgb(0,0,0)'
    draw.text((x,y), name_of_organisation, fill=color, font=font)

for name_of_the_person in sheet.col_values(4):
    (x,y) = 235,197
    color = 'rgb(0,0,0)'
    draw.text((x,y), name_of_the_person, fill=color, font=font)

for certification_for in sheet.col_values(6):
    (x,y) = 355,236
    color = 'rgb(0,0,0)'
    draw.text((x,y), certification_for, fill=color, font=font)

image.save('certificate' + str(sheet.row_count) + '.png')
