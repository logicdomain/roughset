# roughset
A roughset library

# How to use?
```
import pandas as pd
from logic.roughset import Roughset as rs
df = ... # pd.DataFrame
A = ['attr1','attr2'] # list
r = rs(df,A).init()

X=... # pd.DataFrame
# r.set_X(X) # deprecated
r.X = X
print(r.lower)
print(r.upper)

```
