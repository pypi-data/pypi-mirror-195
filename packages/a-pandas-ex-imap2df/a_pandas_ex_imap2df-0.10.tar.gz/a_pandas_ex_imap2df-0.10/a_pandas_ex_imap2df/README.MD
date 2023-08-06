# imap to pandas DataFrame

## pip install a-pandas-ex-imap2df


```python
import pandas as pd
from a_pandas_ex_imap2df import pd_add_imap2df
pd_add_imap2df()
df = pd.Q_imap2df(
    number=10, 
    username="XZXXXXX@outlook.com",
    password="XXXXX",
    imap_server="outlook.office365.com",
)

...
347   Conten...   image/...   b'Cont...        Conten...      ([[Con...             2       Messag...   \r\n\t... 
348   Conten...   image/...   b'Cont...        Conten...      ([[Con...             2       Conten...       en-US 
349   Conten...   image/...   b'Cont...        Conten...      ([[Con...             2       X-MS-H...         yes 
350   Conten...   image/...   b'Cont...        Conten...      ([[Con...             2       X-Auto...         All 
351   Conten...   image/...   b'Cont...        Conten...      ([[Con...             2       X-MS-E...          -1 
352   Conten   image/...   b'Cont...        Conten...      ([[Con...             2       X-MS-T...             
353   Conten...   image/...   b'Cont...        Conten...      ([[Con...             2       X-MS-E...           0 
354   Conten...   image/...   b'Cont...        Conten...      ([[Con...             2       Conten...   multip... 
355   Conten...   image/...   b'Cont...        Conten...      ([[Con...             2       MIME-V...         1.0 
356   Conten...   colors...   b'Cont...        Conten...      ([[Con...             2            From   Outloo... 
...

```