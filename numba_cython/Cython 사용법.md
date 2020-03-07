# Cython 사용법

---

1. installation

```bash
pip install Cython
```

2. pyx 파일 생성

``` python
print "Hello World"
```

cdef 등을 이용해 함수 정의, 데이터 타입 선언을 할 수 있다. 아래의 예시는 sin 함수를 이용하여 integrate 하는 함수의 예시이다. C의 외부 라이브러리도 불러올 수 있다. 

``` python
cdef extern from "math.h":
	double sin(double)

cdef double f(double x) except *:
	return sin(x**2)

def integrate(double a, double b, int N):
	cdef int i
	cdef double dx, s = 0
	dx = (b-a)/N
	for i in range(N):
		s += f(a+i*dx)
	return s*dx
```

3. setup.py 생성

```python
from distutils.core import setup
from Cython.Build import cythonize
setup( ext_modules = cythonize("helloworld.pyx") )
```

`setup.py`를 사용하지 않고 `cython file_name.pyx` 를 사용해서 `file_name.c` 파일로 빌드하는 방법도 있다. 일반적으로 `setup.py` 를 사용하는 것이 편리해서 이를 많이 사용한다고 한다. 

4. build

``` bash
python setup.py build_ext --inplace
```

빌드가 완료되면 build 폴더가 생성되며 일반 파이썬에서 `import` 하여 해당 함수를 사용할 수 있다. 

5. 실행

``` python
import helloworld
Hello World
```

실행 속도는 위의 예시 함수를 사용하였다. 약 44배 빨랐다.

![image-20200307230558282](/Users/jonghyunlee/Library/Application Support/typora-user-images/image-20200307230558282.png)

``` python
import datetime
import cypy
import pypy

a=0.0234
b=0.1234
N=10000000

sts = datetime.datetime.now()
r = cypy.integrate(a,b,N)
ets = datetime.datetime.now()
t1diff = ets - sts
print("cytest.integrate(a=%f, b=%f, N=%d) = %f takes %s" % (a,b,N,r, t1diff))

sts = datetime.datetime.now()
r = pypy.integrate(a,b,N)
ets = datetime.datetime.now()
t2diff = ets - sts
print("cytest2.integrate(a=%f, b=%f, N=%d) = %f takes %s" % (a,b,N,r, t2diff))

times = t2diff.total_seconds() / t1diff.total_seconds()
print("cypy is faster than pypy %d times" % int(times))
```

## 참고

- http://egloos.zum.com/mcchae/v/11072949