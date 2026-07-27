import pandas as pd
import io

def analyses_to_csv(rows):
    df=pd.DataFrame(rows)
    return df.to_csv(index=False).encode("utf-8")
