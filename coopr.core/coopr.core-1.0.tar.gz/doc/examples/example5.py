from coopr.core import *

# @main:
@coopr_api(namespace='utility')
def f1(data, x=0, y=1):
    """A simple example.

    Required:
        x: A required keyword argument

    Optional:
        y: An optional keyword argument

    Return:
        a: A return value
        b: Another return value
    """
    return CooprAPIData(a=2*data.z, b=x+y)
# @:main

# @create:
g = CooprAPIFactory('utility.f1')
# @:create
# @exec:
data = CooprAPIData(z=1)
val = g(data, x=2)
# @:exec
print val
