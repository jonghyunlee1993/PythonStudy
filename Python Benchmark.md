# Python Benchmark

코드의 실행 속도를 확인해서 성능을 개선해야할 때 여러 가지 방법이 있다.



1. Time 라이브러리

시작 시간, 끝 시간을 구한 후 빼주는 방식

```python
import time

tic = time.time()

for i in range(1000):
    a = i ** i
   
toc = time.time() - tic

print("TIME: {:2.2f}".format(toc))
```



2. Timeit 라이브러리

간단한 함수를 호출할 때, 해당 함수의 실행 시간을 체크하기 위한 3가지 방법

`python3 -m timeit '"-".join(str(n) for n in range(100))'`

`timeit.timeit(lambda: "-".join(map(str, range(100))), number=10000)`

```python
import timeit

timeit.timeit('"-".join(str(n) for n in range(100))', number=10000)
```



3. cProfile

복잡한 프로그램에서 적합한 방법

`python -m cProfile my_code.py`

해당 코드가 실행되면서 발생하는 시간을 함수별로 체크해준다. 

```bash
1007 function calls in 0.061 CPU seconds

Ordered by: standard name
ncalls  tottime  percall  cumtime  percall filename:lineno(function)
    1    0.000    0.000    0.061    0.061 <string>:1(<module>)
 1000    0.051    0.000    0.051    0.000 euler048.py:2(<lambda>)
    1    0.005    0.005    0.061    0.061 euler048.py:2(<module>)
    1    0.000    0.000    0.061    0.061 {execfile}
    1    0.002    0.002    0.053    0.053 {map}
    1    0.000    0.000    0.000    0.000 {method 'disable' of '_lsprof.Profiler objects}
    1    0.000    0.000    0.000    0.000 {range}
    1    0.003    0.003    0.003    0.003 {sum}
```

| 항목            | 설명                                       |
| --------------- | ------------------------------------------ |
| ncalls          | 함수의 호출 횟수                           |
| tottime         | 함수에서 소비된 총 시간                    |
| percall         | 호출 횟수당 사용 시간                      |
| cumtime         | 다른 함수 호출을 포함한 함수에서 보낸 시간 |
| filename:lineno | 파일명과 해당하는 행의 번호                |

아래의 링크에서는 cProfile 라이브러리르 보기 좋게 정리해주는 툴을 받을 수 있는 듯하다.

https://github.com/rkern/line_profiler