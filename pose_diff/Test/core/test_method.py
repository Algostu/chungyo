# from pose_diff.core import save_docx
from pose_diff.core.report import insert_image_and_pictures

def test_save_docx():
    '''
    Save document

    Todo
        1. Start html to PDF...Done
        2. Start html redering using beautify...Done
    '''
    print("save_docx testing...")
    insert_image_and_pictures()
    print("Done")
