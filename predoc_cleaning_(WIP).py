import pandas as pd

df = pd.read_csv('predoc_job_raw_data.csv')

print(df.loc[0])

# ---------------- Consolidating Repeated Variables ----------------
# Consolidating field of research variables
print('TEST INITIAL --------------------------------------------------')
print(df['Fields of Research'].head(5))

string_list = ["field", "Field"]
varname_list = df.columns.tolist()
for x in string_list:
    for varname in varname_list:
        if x in varname:
            df['Fields of Research'] = df['Fields of Research'].combine_first(df[varname])

print('TESTING RESULT =================================================')           
print(df['Fields of Research'].head(5))

# Consolidating application deadline variables


# Saving clean data as CSV
df.to_csv('predoc_job_clean_data.csv')

