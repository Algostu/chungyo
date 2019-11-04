from pose_diff.core import save_docx

def test_save_docx():
    '''
    Save document

    Todo
        1. html to PDF
        2. html redering using beautify
    '''
    print("save_docx testing...", end=' ')
    user_numpy_file_name = 'pose_diff/Test/core/test_data/exercise_numpy.npy'
    applied_trainer_numpy_file_name = 'pose_diff/Test/core/test_data/upgraded.npy'
    documentation_file_name = 'pose_diff/Test/core/test_result/doc.docx'
    save_docx.save_docx(user_numpy_file_name, applied_trainer_numpy_file_name, documentation_file_name)
    print("Done")
