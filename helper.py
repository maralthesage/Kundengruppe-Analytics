import datetime as dt
import pandas as pd

from datetime import datetime, date

def assign_age(aa):
    current_date = dt.datetime.now()
    aa['GEBURT'] = aa['GEBURT'].fillna("")
    aa['AGE'] = aa['GEBURT'].apply(lambda x: current_date.year - x.year - ((current_date.month, current_date.day) < (x.month, x.day)))

    # Define age groups
    def assign_age_group(age):
        if age <= 18:
            return "0-18"
        elif age <= 30:
            return "19-30"
        elif age <= 50:
            return "31-50"
        elif age <= 65:
            return "51-65"
        elif age >= 65:
            return "65+"
        else:
            return "NA"

    aa['AGE_GROUP'] = aa['AGE'].apply(assign_age_group)
    return aa


def process_id(data):
    data = data.astype(str)
    data = data.replace(".0","")
    data = data.str.zfill(10)
    return data

def process_date(data):
    return pd.to_datetime(data,format='mixed',errors='coerce')



def get_half_year_info(today: date = None):
    if today is None:
        today = date.today()
    
    # Base reference: H1 2025 -> number 49
    base_half_year_start = date(2025, 1, 1)
    base_number = 49

    # Determine if we're in H1 or H2
    if today.month <= 6:
        # H1 of current year
        current_half_index = 0
    else:
        # H2 of current year
        current_half_index = 1

    # Total number of half years since base
    years_diff = today.year - base_half_year_start.year
    half_year_offset = years_diff * 2 + current_half_index

    # Calculated number
    number = base_number + half_year_offset

    # Determine previous half-year
    if current_half_index == 0:
        # If we're in H1, previous half-year is H2 of last year
        prev_start = date(today.year - 1, 7, 1)
        prev_end = date(today.year - 1, 12, 31)
    else:
        # If we're in H2, previous half-year is H1 of same year
        prev_start = date(today.year, 1, 1)
        prev_end = date(today.year, 6, 30)

    return {
        'number': number,
        'prev_start': prev_start,
        'prev_end': prev_end
    }




def assign_sources(aa,column):

    aa['SOURCE'] = ""

    ## Amazon
    aa.loc[(aa[column].str[3:]=='921am'),"SOURCE"] = 'Amazon'
    ## AWIN
    aa.loc[(aa[column].str[3:6]=='929'),"SOURCE"] = 'AWIN'
    ## Blätterkatalog
    aa.loc[(aa[column].str[3:6]=='938'),"SOURCE"] = 'Blätterkatalog'
    ## Corporate Benefits
    aa.loc[(aa[column].str[3:6]=='943'),"SOURCE"] = 'Corporate Benefits'
    ## Genussmagazin
    aa.loc[(aa[column].str.contains(r'936gm|925gm',case=False,regex=True,na=False)),"SOURCE"] = 'Genussmagazin'
    ## Google Shopping
    aa.loc[(aa[column].str.contains(r'926gs|924gs',case=False,regex=True,na=False)),"SOURCE"] = 'Google Shopping'
    ## Internet Import
    aa.loc[(aa[column].str.contains(r'20i|INT',case=False,regex=True,na=False)),"SOURCE"] = 'Internet Import'
    ## Inventur Trost
    aa.loc[(aa[column].str[3:]=='022iv'),"SOURCE"] = 'Inventur Trost'
    ## Lionshome
    aa.loc[(aa[column].str[3:]=='921lh'),"SOURCE"] = 'Lionshome'
    ## Newsletter
    aa.loc[(aa[column].str[3:6]=='923'),"SOURCE"] = 'Newsletter'
    ## Newsletter Angebot
    aa.loc[(aa[column].str[3:]=='923na'),"SOURCE"] = 'Newsletter Angebot'
    ## Newsletter Rezept
    aa.loc[(aa[column].str[3:]=='923nr'),"SOURCE"] = 'Newsletter Rezept'
    ## Newsletter Thema
    aa.loc[(aa[column].str[3:]=='923nt'),"SOURCE"] = 'Newsletter Thema'
    ## Otto
    aa.loc[(aa[column].str[3:]=='921ot'),"SOURCE"] = 'Otto'
    ## Google SEA
    aa.loc[(aa[column].str[3:6]=='926'),"SOURCE"] = 'Google SEA'
    ## SEA Brand
    aa.loc[(aa[column].str[3:]=='926br'),"SOURCE"] = 'SEA Brand'
    ## SEA Non-Brand
    aa.loc[(aa[column].str[3:]=='926sa'),"SOURCE"] = 'SEA Non-Brand'
    ## SEO
    aa.loc[(aa[column].str[3:6]=='927'),"SOURCE"] = 'SEO'
    ## SEO Brand
    aa.loc[(aa[column].str[3:]=='927br'),"SOURCE"] = 'SEO Brand'
    ## SEO Non-Brand
    aa.loc[(aa[column].str[3:]=='927so'),"SOURCE"] = 'SEO Non-Brand'
    ## Social Media
    aa.loc[(aa[column].str[3:6]=='925'),"SOURCE"] = 'Social Media'
    ## Pinterest
    aa.loc[(aa[column].str.contains(r'925pi|925pt|932aa|pinterest',regex=True,case=False,na=False)),"SOURCE"] = 'Pinterest'
    ## Instagram
    aa.loc[(aa[column].str.contains(r'925ig',regex=True,case=False,na=False)),"SOURCE"] = 'Instagram'
    ## Facebook
    aa.loc[(aa[column].str.contains(r'925fb',regex=True,case=False,na=False)),"SOURCE"] = 'Facebook'
    ## Sovendus
    aa.loc[(aa[column].str.contains(r'928so|sov',regex=True,case=False,na=False)),"SOURCE"] = 'Sovendus'


    ## Fremdadressen
    aa.loc[(aa[column].str[3].isin(['1', '2', '3', '4'])) & (aa[column].str[4:6].isin(['01'])),"SOURCE"] = 'Fremdadressen'
    ## Katalog und Karte
    aa.loc[(aa[column].str[3].isin(['1', '2', '3', '4'])) & (aa[column].str[4:6].isin(['02', '03', '04'])),"SOURCE"] = 'Katalog und Karte'
    ## Beilage
    aa.loc[(aa[column].str[3:6].isin(['011', '012', '013'])),"SOURCE"] = 'Beilage'
    aa.loc[(aa[column].str[3:6].isin(['040'])),"SOURCE"] = 'Beilage'
    ## Geburtstagskarte
    aa.loc[(aa[column].str[3:6]=='060'),"SOURCE"] = 'Geburtstagskarte'
    ## Kataloganforderung
    aa.loc[(aa[column].str[3:6]=='000'),"SOURCE"] = 'Kataloganforderung'
    ## Freundschaftswerbung
    aa.loc[(aa[column].str[3:6]=='030'),"SOURCE"] = 'Freundschaftswerbung'
    ## Mailing
    aa.loc[(aa[column].str[3:6]=='014'),"SOURCE"] = 'Mailing'
    ## Blackweek
    aa.loc[(aa[column].str[3:6]=='016'),"SOURCE"] = 'Blackweek'
    ## Altcode
    aa.loc[(aa['SOURCE']==''), 'SOURCE'] = 'Altcode'

    aa["ON-OFF"] = ""
    ## SOURCE -> Online/Offline
    aa.loc[aa['SOURCE'].isin(['Amazon','AWIN','Blätterkatalog','Corporate Benefits','Genussmagazin','Google Shopping','Internet Import','Inventur Trost','Lionshome',
        'Otto','Google SEA','SEA Brand','SEA Non-Brand','SEO','SEO Brand','SEO Non-Brand', 'Social Media','Pinterest','Instagram','Facebook','Sovendus']),'ON-OFF'] = 'Online'
    aa.loc[aa['SOURCE'].isin(['Newsletter','Newsletter Angebot','Newsletter Rezept','Newsletter Thema']),'ON-OFF'] = 'Newsletter'
    aa.loc[aa['SOURCE'].isin(['Fremdadressen','Katalog und Karte','Beilage','Geburtstagskarte','Kataloganforderung','Freundschaftswerbung','Mailing','Blackweek']),'ON-OFF'] = 'Offline'
    aa.loc[aa['SOURCE'].isin(['Altcode']),'ON-OFF'] = 'Altcode'
    return aa


herkunft = { '1':'Schriftlich','2':'Fax','3':'Telefon','4':'Internet','5':'Call-Center',
    '6':'Ladenverkauf','7':'Vertreter','8':'E-Mail','9':'Anrufbeantworter/Mailbox',
    'B':'Beleglesung', 'E':'Marktplätze','F':'Amazon-Fulfillment','M':'Messe','S':'SMS','nan':'Ohne/Unbekannt'}


anrede = {
    '1': 'Herrn', '2': 'Frau', '3': 'Frau/Herr', '4': 'Firma', '5': 'Leer(Firmenadresse)', 
    '6': 'Fräulein', '7': 'Familie', 'X': 'Divers'
}

def process_anrede(value):
    value = str(value)
    if value.startswith('0'):  # Remove leading zeros for numeric values
        return value.replace('0', '')
    if value.endswith('.0'):  # Remove '.0' suffix
        return value.replace('.0', '')
    return value  # Return non-numeric values as they are
