import codecs
import pdfkit
from bs4 import BeautifulSoup
from time import gmtime, strftime


path_wkthmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
config = pdfkit.configuration(wkhtmltopdf=path_wkthmltopdf)

def insert_image_and_pictures():
    '''
    html rendering and convert it to pdf

    Todo
        1. pdf로 변환시 글씨가 안보이고 페이지가 깨지는 오류가 있다.
    Limit
        1. 각종 basic info들의 길이가 너무 길면 짤린다. (운동이름, 사람 이름)
    '''
    html_file_name = 'ui/analyze_report.html'
    html_doc = codecs.open(html_file_name, 'r')
    soup = BeautifulSoup(html_doc, features="lxml")
    # data
    user_name = 'daan'
    tall_weigth = '%d cm / %d kg' % (165, 45)
    age_sex = '%d age/ F' % 21
    trainer = 'hoon'
    exercise_name = 'shoulderPress'
    Times = '05m 16s'
    user_type = 'basic'
    date = strftime("%Y/%m/%d", gmtime())
    test_picture = 'IU.jpg'

    # rendering
    soup.find(id='username_ek1').string.replace_with(user_name)
    soup.find(id='username').string.replace_with(user_name)
    soup.find(id='agesex').string.replace_with(age_sex)
    soup.find(id='tallweight').string.replace_with(tall_weigth)

    soup.find(id='trainername').string.replace_with(trainer)
    soup.find(id='exercise').string.replace_with(exercise_name)
    soup.find(id='times').string.replace_with(Times)

    soup.find(id='affiliation').string.replace_with('Affiliation') # 소속이름
    soup.find(id='user_type').string.replace_with(user_type)
    soup.find(id='date').string.replace_with(date)

    # rendering image
    soup.find(id='avatar')['src'] = test_picture
    soup.find(id='initial_pose_graph')['src'] = test_picture
    soup.find(id='best_pose_graph')['src'] = test_picture

    soup.find(id='score_graph')['src'] = test_picture
    soup.find(id='divider_ek8').string.replace_with(test_picture)

    soup.find(id='detail_graph1')['src'] = test_picture
    soup.find(id='divider').string.replace_with(test_picture)

    soup.find(id='detail_graph2')['src'] = test_picture
    soup.find(id='divider_ek1').string.replace_with(test_picture)

    soup.find(id='detail_graph3')['src'] = test_picture
    soup.find(id='divider_ek2').string.replace_with(test_picture)

    soup.find(id='detail_graph4')['src'] = test_picture
    soup.find(id='divider_ek3').string.replace_with(test_picture)

    soup.find(id='detail_graph5')['src'] = test_picture
    soup.find(id='divider_ek4').string.replace_with(test_picture)

    soup.find(id='detail_graph6')['src'] = test_picture
    soup.find(id='divider_ek5').string.replace_with(test_picture)

    # save as html and pdf
    result_html_file_name="ui/result.html"
    result_pdf_file_name="temp/report.pdf"

    with open(result_html_file_name, "w") as file:
        file.write(str(soup))

    pdfkit.from_file(result_html_file_name, result_pdf_file_name, configuration=config)
