import pandas as pd
from dateutil.parser import parse
from datetime import datetime

def main():
	print "Reading data..."
	data = pd.read_csv('workcomp_extract.csv')

	print "Parsing dates..."
	data['Collection_Date'] = [parse(x) for x in data['Collection_Date']]

	print "Start time conversion..."
	data['Dump_Time_Stamp'] = [change_date(x) for x in data['Dump_Time_Stamp'].astype(str)]
	data['Section_Code'] = [clean_district(x) for x in data['Section_Code']]
	
	print "Saving File..."
	data.to_csv('dsny_update.csv', index=False)
	
def change_date(date):
    if date == 'nan':
        return parse('2000-01-01')
    else:
        return parse(date)

def clean_district(district):
	print "Cleaning districts..."
    district = str(district).strip()
    if district[:2] == 'QS' or district[:2] == 'QN':
        return district[:1] + 'E' + district[2:]
    elif district[:1] == 'M':
        return 'MN' + district[2:]
    elif district[:2] == 'BX':
        return district[:2] + district[-3:]
    elif district[:2] == 'BK':
        if district[:3] == 'BKW':
            return 'BKS' + district[-3:]
        elif district[:3] == 'BKE':
            if district[-3:] in ['091', '092','093', '161','162','171', '172', '173','174','175']:
                return 'BKN' + district[-3:]
            else:
                return 'BKS' + district[-3:]
        else:
            return district[:]
    else:
        return district[:]
    
    
if __name__ == "__main__":
	main()
	print "Finished"