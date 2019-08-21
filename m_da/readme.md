### input

```python
list1 = np.array([[x1,y1],[x2,y2],[x3,y3],[x4,y4],[x5,y5]])
```



### output

[[  1.   1. 255.]
 [  2.   5.   0.]
 [  6.   1.   0.]
 [  9.   4.   0.]
 [ 10.   6. 255.]]

---

#### def create

input으로 들어온 함수 값에 color라는 제 3요소 추가

----

#### def diff

create으로 생성된 list와 standard (표준,모범)list 비교

```python
if(x-1<=q<=x+1):
    pass
if(x-1>q or x+1<q):
    a[i][2] = 0
```

일단 오차 범위는 1로 했음 

비교했을 때 틀린 부분은 가로줄의 세번째 요소 값이 0이 되게 함.





