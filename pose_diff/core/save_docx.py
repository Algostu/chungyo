from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx import Document
from docx.shared import Inches
from save_graph import save_graph

def save_docx(docx_name):
    document=Document()
    save_graph(1,'겨드랑이')
    save_graph(2,'팔꿈치')

    # body=[]
    # body=('Neck','RShoulder','RElbow','RWrist','LShoulder','LElbow',
    #       'LWrist','RHip','RKnee','RAnkle','LHip','LKnee','LAnkle','REye','LEye','REar','LEar','Background')

    head=document.add_heading('운동 분석(User-Trainer)',0)
    head.alignment = WD_ALIGN_PARAGRAPH.CENTER
    sub1=document.add_paragraph('겨드랑이 각도(User-RED,Trainer-BLUE)')
    document.add_picture('겨드랑이.png',width=Inches(5))
    document.add_paragraph('팔꿈치 각도(User-RED,Trainer-BLUE)')
    document.add_picture('팔꿈치.png',width=Inches(5))
    document.add_page_break()

    document.add_heading('Trainer의 그래프보다 내 그래프가 앞(뒤)에 있는 경우',level=3)
    document.add_paragraph('Trainer 보다 먼저(늦게) 시작했다')
    document.add_paragraph('')
    document.add_heading('Trainer의 그래프보다 내 그래프가 위아래로 짧은 경우',level=3)
    document.add_paragraph('Trainer 보다 덜 팔이 구부려진다 또는 덜 움직인다.')
    document.add_paragraph('')
    document.add_heading('Trainer의 그래프보다 내 그래프가 넓은(좁은) 경우',level=3)
    document.add_paragraph('Trainer 보다 속도가 느리(빠르다)')
    document.add_paragraph('')
    document.add_heading('Trainer와 내가 비슷한 경우',level=3)
    document.add_paragraph('잘하는 중이다.')

    document.save(docx_name)




