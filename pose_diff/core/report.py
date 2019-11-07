import codecs
import math
import os
from time import gmtime, strftime

import matplotlib.pyplot as plt
import numpy as np
from bs4 import BeautifulSoup


def insert_image_and_pictures(user_info, paragraph):
    '''
    html rendering and convert it to pdf

    Params
        + user_info, paragraph는 변수로 받는다. 하지만 그림 같은 것은 경로를 고정한다. 현재 고정된 경로는 '../temp/'이다.
        + avg_score는 직접 계산한다.
    Todo
        1. pdf로 변환시 글씨가 안보이고 페이지가 깨지는 오류가 있다.
    Limit
        1. 각종 basic info들의 길이가 너무 길면 짤린다. (운동이름, 사람 이름)
    '''
    relative_base_folder = os.path.join('..', 'temp')
    pictures = [
    os.path.join(relative_base_folder,'skeleton.png'),
    os.path.join(relative_base_folder,'skeleton.png')
    ]
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
    soup = BeautifulSoup(html_doc, features='html.parser', from_encoding='utf-8')
    # data
    score = np.load('temp/graph.npy')[0]
    avg_score = sum(score)/len(score)
    if avg_score > 80:
        Grade = 'Outstanding'
    elif avg_score > 60:
        Grade = 'Exceed Expectation'
    elif avg_score > 40:
        Grade = 'Acceptable'
    elif avg_score > 20:
        Grade = 'Pool'
    else:
        Grade = 'Troll'
    user_name = user_info[2]
    tall_weigth = '%d cm / %d kg' % (user_info[5], user_info[4])
    age_sex = '%d age/ %s' % (21, 'M' if user_info[7] == 'men' else 'F')
    # 운동의 점수와 함께 유저의 점수를 알려준다.
    # 추가 정보를 알려준다.
    trainer = user_info[8]
    exercise_name = user_info[9]
    user_type = user_info[1]
    date = strftime("%Y/%m/%d", gmtime())
    test_picture = 'IU.jpg'

    # rendering
    soup.find(id='username_ek1').string.replace_with(user_name)
    soup.find(id='username').string.replace_with(user_name)
    soup.find(id='agesex').string.replace_with(age_sex)
    soup.find(id='tallweight').string.replace_with(tall_weigth)

    soup.find(id='trainername').string.replace_with(trainer)
    soup.find(id='exercise').string.replace_with(exercise_name)
    soup.find(id='times').string.replace_with("Grade: "+Grade)

    soup.find(id='affiliation').string.replace_with('Affiliation') # 소속이름
    soup.find(id='user_type').string.replace_with(user_type)
    soup.find(id='date').string.replace_with(date)

    # rendering image
    soup.find(id='avatar')['src'] = test_picture
    soup.find(id='initial_pose_graph')['src'] = pictures[0]
    soup.find(id='best_pose_graph')['src'] = pictures[1]

    soup.find(id='score_graph')['src'] = score_graph_file_name
    soup.find(id='divider_ek8').string.replace_with(paragraph[0])

    soup.find(id='detail_graph1')['src'] = gap_graph_file_name[0]
    soup.find(id='divider').string.replace_with(paragraph[1])

    soup.find(id='detail_graph2')['src'] = gap_graph_file_name[1]
    soup.find(id='divider_ek1').string.replace_with(paragraph[2])

    soup.find(id='detail_graph3')['src'] = gap_graph_file_name[2]
    soup.find(id='divider_ek2').string.replace_with(paragraph[3])

    soup.find(id='detail_graph4')['src'] = gap_graph_file_name[3]
    soup.find(id='divider_ek3').string.replace_with(paragraph[4])

    soup.find(id='detail_graph5')['src'] = gap_graph_file_name[4]
    soup.find(id='divider_ek4').string.replace_with(paragraph[5])

    soup.find(id='detail_graph6')['src'] = gap_graph_file_name[5]
    soup.find(id='divider_ek5').string.replace_with(paragraph[6])

    # save as html and pdf
    result_html_file_name="html/result.html"
    result_pdf_file_name="html/report.pdf"

    with open(result_html_file_name, "w") as file:
        file.write(str(soup))

    # pdfkit.from_file(result_html_file_name, result_pdf_file_name, configuration=config)

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
    plt.axhline(y = average_score, c='r', ls='--', label='user avergae score: %d' % average_score)
    plt.axhline(y = 64, c='g', ls='--', label='avergae score: %d' % 64)
    plt.legend()
    fig = plt.gcf()
    fig.savefig(score_graph_file_name)

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


def make_paragraph(graph_location):
    '''
    return paragraph analyzing numpy files
    '''
    graph_numpy = np.load(graph_location)
    score_numpy = graph_numpy[0]
    gap_numpy =graph_numpy[1:7]
    divide_score_numpy = graph_numpy[8]
    avg_score = sum(score_numpy) / len(score_numpy)
    if avg_score > 80:
        Grade = 'Outstanding'
        Grade_exp = "your exercise is as qualified as trainer. Perfect, well done!"
    elif avg_score > 60:
        Grade = 'Exceed Expectation'
        Grade_exp = "your exercise is almost as same as trainer's, but this does not mean to be satisfied with your work. If you work hard, you can achieve more better score. We are sure of it"
    elif avg_score > 40:
        Grade = 'Acceptable'
        Grade_exp = "you manage to repeat after trainer's exercise. So from now, focuse on details and timing during exercising."
    elif avg_score > 20:
        Grade = 'Pool'
        Grade_exp ="you have potential to become pro, but your work is messy now. So please exercise to copy trainer's work."
    else:
        Grade = 'Troll'
        Grade_exp ="you are slower starter. To be more better, try to learn by repeating a part of motion of exercise."

    lows = []
    for part_score in divide_score_numpy:
        lows.append(part_score.index(min(part_score)) / len(part_score))
    weak_part = sum(lows) / len(lows) * 100
    if weak_part < 25.0:
        weak = 'you push your arms upper early. It means that 0%~25% of total motion is most weak part of yours'
    elif weak_part < 50.0:
        weak = 'you push your arms upper lately. It means that 25%~50% of total motion is most weak part of yours'
    elif weak_part < 75.0:
        weak = 'you push your arms lower early. It means that 50%~75% of total motion is most weak part of yours'
    elif weak_part <= 100.0:
        weak = 'you push your arms lower lately. It means that 75%~100% of total motion is most weak part of yours'

    sums = []
    for gaps in gap_numpy:
        sums.append(sum(list(map(lambda x: math.sqrt(math.pow(x[0], 2)+math.pow(x[1], 2)), gaps))))
    titles = ['left shoulder', 'left elbow', 'left wrist', 'right shoulder', 'right elbow', 'right wrist']
    part = titles[sums.index(max(sums))]

    score_paragraph = f"Your grade is {Grade}. This means that {Grade_exp}. Worst part of your exercise is when {weak}. So try to focus on more better at here. Finally, the most wrong part of your body is {part}. please see below graphs for details. This score is just a number. If you keep exercising, it will be changed better."

    functions = [
    "anchor points and making itself isolated from interference of other muscle.",
    "connection point which is critical to move exact range.",
    "grabbing object tight and shouldn't move itself apart from elbow."
    ]*2
    detail_paragraphs = []
    for gaps, part_name, function in zip(gap_numpy, titles, functions):
        x_tendency = len(list(filter(lambda x: x[0]>0, gaps))) / len(gaps) * 100
        y_tendency = len(list(filter(lambda x: x[1]>0, gaps))) / len(gaps) * 100
        if x_tendency > 66.6:
            x_tendency = 'right'
        elif x_tendency > 33.3:
            x_tendency = ''
        else:
            x_tendency = 'left'

        if y_tendency > 66.6:
            y_tendency = 'upper'
        elif y_tendency > 33.3:
            y_tendency = ''
        else:
            y_tendency = 'lower'

        if x_tendency == '' and y_tendency == '':
            tendency = ""
        else:
            tendency = f'{part_name} has moved with {x_tendency},{y_tendency} biased.'

        detail_paragraphs.append(f"This graph is about {part_name}'s movement track data. {part_name} is used as {function} Above graph represents difference between trainer's {part_name} movement and user's. As range of x and y are getting wide, the gaps between them are getting bigger. {tendency}")

    result = [
    score_paragraph,
    *detail_paragraphs
    ]
    return result
