import numpy as np
from some_module import get_helloworld

def test_get_helloworld():
	assert 'hello world' == get_helloworld()

if __name__=='__main__':
    test_get_helloworld()


