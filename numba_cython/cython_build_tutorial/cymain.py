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