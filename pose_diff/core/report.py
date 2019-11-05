import os
import numpy as np
import matplotlib.pyplot as plt
import codecs
import pdfkit
from bs4 import BeautifulSoup
from time import gmtime, strftime


path_wkthmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
config = pdfkit.configuration(wkhtmltopdf=path_wkthmltopdf)

def insert_image_and_pictures(user_info, paragraph):
    '''
    html rendering and convert it to pdf

    Params
        user_info, paragraph는 변수로 받는다. 하지만 그림 같은 것은 경로를 고정한다. 현재 고정된 경로는 '../temp/'이다.
    Todo
        1. pdf로 변환시 글씨가 안보이고 페이지가 깨지는 오류가 있다.
    Limit
        1. 각종 basic info들의 길이가 너무 길면 짤린다. (운동이름, 사람 이름)
    '''
    relative_base_folder = os.path.join('..', 'temp')
    score_graph_file_name = os.path.join(relative_base_folder, 'score.png')
    gap_graph_file_name = [
    os.path.join(relative_base_folder, 'left_shoulder.png'),
    os.path.join(relative_base_folder, 'left_lebow.png'),
    os.path.join(relative_base_folder, 'left_wrist.png'),
    os.path.join(relative_base_folder, 'right_shoulder.png'),
    os.path.join(relative_base_folder, 'right_lebow.png'),
    os.path.join(relative_base_folder, 'right_wrist.png')
    ]

    html_file_name = 'html/analyze_report.html'
    html_doc = codecs.open(html_file_name, 'r')
    soup = BeautifulSoup(html_doc, features="lxml")
    # data
    print(user_info)
    user_name = user_info[2]
    tall_weigth = '%d cm / %d kg' % (user_info[5], user_info[4])
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

    soup.find(id='score_graph')['src'] = score_graph_file_name
    soup.find(id='divider_ek8').string.replace_with(score_graph_file_name)

    soup.find(id='detail_graph1')['src'] = gap_graph_file_name[0]
    soup.find(id='divider').string.replace_with(paragraph[0])

    soup.find(id='detail_graph2')['src'] = gap_graph_file_name[1]
    soup.find(id='divider_ek1').string.replace_with(paragraph[1])

    soup.find(id='detail_graph3')['src'] = gap_graph_file_name[2]
    soup.find(id='divider_ek2').string.replace_with(paragraph[2])

    soup.find(id='detail_graph4')['src'] = gap_graph_file_name[3]
    soup.find(id='divider_ek3').string.replace_with(paragraph[3])

    soup.find(id='detail_graph5')['src'] = gap_graph_file_name[4]
    soup.find(id='divider_ek4').string.replace_with(paragraph[4])

    soup.find(id='detail_graph6')['src'] = gap_graph_file_name[5]
    soup.find(id='divider_ek5').string.replace_with(paragraph[5])

    # save as html and pdf
    result_html_file_name="html/result.html"
    result_pdf_file_name="html/report.pdf"

    with open(result_html_file_name, "w") as file:
        file.write(str(soup))

    pdfkit.from_file(result_html_file_name, result_pdf_file_name, configuration=config)

def make_graph(graph_location, base_folder):
    score_graph_file_name = os.path.join(base_folder, 'score.png')
    gap_graph_file_name = [
    os.path.join(base_folder, 'left_shoulder.png'),
    os.path.join(base_folder, 'left_lebow.png'),
    os.path.join(base_folder, 'left_wrist.png'),
    os.path.join(base_folder, 'right_shoulder.png'),
    os.path.join(base_folder, 'right_lebow.png'),
    os.path.join(base_folder, 'right_wrist.png')
    ]
    # score
    graph_numpy = np.load(graph_location)
    score_numpy = graph_numpy[0]
    average_score = sum(score_numpy) / len(score_numpy)

    plt.plot(score_numpy)
    plt.ylim([0, 100])
    plt.axhline(y = average_score, c='r', ls='--', label='avergae score: %d' % average_score)
    plt.legend()
    plt.savefig(score_graph_file_name)

    # graph
    gap_numpy = graph_numpy[1:7]
    titles = ['left_shoulder', 'left_elbow', 'left_wrist', 'right_shoulder', 'right_elbow', 'right_wrist']
    for gap, title, file_name in zip(gap_numpy, titles, gap_graph_file_name):
        plt.figure()
        ax = plt.gca()
        xs, ys = list(zip(*gap))[0], list(zip(*gap))[1]
        x_max = max([abs(x) for x in xs])
        y_max = max([abs(y)for y in ys])
        ax.scatter(xs, ys)
        ax.set_xlim([-x_max, x_max])
        ax.set_ylim([-y_max, y_max])
        ax.grid(True)
        ax.axhline(y=0, c='black', ls='--')
        ax.axvline(x=0, c='black', ls='--')
        ax.set_title(title)
        plt.savefig(file_name)

    print("Done")

def make_paragraph(graph_location):
    '''
    return paragraph analyzing numpy files
    '''
    result = [
    '정말 잘했습니다.',
    '정말 잘했습니다.',
    '정말 잘했습니다.',
    '정말 잘했습니다.',
    '정말 잘했습니다.',
    '정말 잘했습니다.',
    '정말 잘했습니다.'
    ]

    return result
