#TaxCalc_app.py


import streamlit as st
import pandas as pd
from cryptography.fernet import Fernet
from io import BytesIO
import hashlib

# Load Fernet key from Streamlit secrets
fernet = Fernet(st.secrets["excel"]["key"].encode())

def verify_integrity(encrypted_bytes):
    try:
        with open("tools/integrity.sha256") as f:
            expected = f.read().strip()
    except:
        return True  # bypass if local file not present (Streamlit Cloud)

    sha = hashlib.sha256()
    sha.update(encrypted_bytes)
    actual = sha.hexdigest()

    return expected == actual


# ---------------------------------------------------------------
# 1. Load Excel Data
# ---------------------------------------------------------------


def load_data():
    key = st.secrets["excel"]["key"].encode()
    fernet = Fernet(key)

    # Load encrypted file
    with open("TaxdataR_encrypted.bin", "rb") as f:
        encrypted = f.read()

    # Optional: verify integrity
    # Verify integrity
    # If integrity file is not present (Streamlit) skip
    try:
        with open("tools/integrity.sha256") as f:
            checksum_expected = f.read().strip()

        checksum_actual = hashlib.sha256(encrypted).hexdigest()

        if checksum_actual != checksum_expected:
            st.error("⚠ Data integrity check failed! File may be tampered.")
            st.stop()
    except:
        pass # ignore locally if file missing

    # Decrypt
    decrypted_bytes = fernet.decrypt(encrypted)
    df = pd.read_excel(BytesIO(decrypted_bytes))
    return df

df_raw = load_data()
#st.dataframe(df_raw)

st.success("Secure data loaded successfully.")


st.title("ቀላል ታክስ ማሰብያ  Easy Tax Estimator ")



#@st.cache_data
##def load_data():
##    # Replace with the path to your Excel file
##    #file=r"C:\zGitDok\zleleoch\memokeria\TaxdataR.xlsx"
##    file=r"TaxdataR.xlsx"
##    sheet="Sheet1"
##    df_raw = pd.read_excel(file, sheet)
##
##    # Example: Ensure consistent column names
##    # Expected columns: Group, Product, Value, Other columns...
##    df_raw.columns = df_raw.columns.str.strip()
##    return df_raw

df_raw = load_data()


# ---------------------------------------------------------------
# 2. UI – Group and Product Selection
# ---------------------------------------------------------------

#st.title("Please choose Your sources and the amaount taxable")
st.markdown("<p style='font-size: larger; font-weight: bold; color: #800080;'>Please choose the tax revision, your income source and amount taxable carefully</p>", unsafe_allow_html=True)
st.markdown("<p style='font-size: larger; font-weight: bold; color: #800080;'>እባክዎ መጀመሪያ የታክስ ማሻሻያውን ይምረጡ እና ከዚያ የገቢ ምንጭዎን እና ታክስ የሚከፈልበትን መጠን በጥንቃቄ ያስገቡ።</p>", unsafe_allow_html=True)
st.markdown("<p style='font-size: smaller; font-weight: bold; color: #800800;'>Take note, this calculation may not be legally binding. It is meant only to provide estimates-ይህ ግብር ግምት ነው እና ከገቢ ባለስልጣናት ጋር ያረጋግጡ </p>", unsafe_allow_html=True)
# Get unique groups from the Excel file
group_options = sorted(df_raw["Revision"].unique())
selected_group = st.selectbox("Select Group:", group_options)

# Filter products by selected group
filtered_products = df_raw[df_raw["Revision"] == selected_group]["Category"].unique()
selected_product = st.selectbox("Select Product:", sorted(filtered_products))

# Amount input
amount_input = st.text_input("Enter Amount:", placeholder="e.g., 1000")


# ---------------------------------------------------------------
# 3. Handle Submission
# ---------------------------------------------------------------

if st.button("Submit"):

    if amount_input.strip() == "":
        st.error("Please enter an amount.")
    else:
        try:
            amount = float(amount_input)
        except ValueError:
            st.error("Amount must be a number.")
            st.stop()

        # -------------------------------------------------------
        # 4. Filter the dataframe to the user’s selection
        # -------------------------------------------------------
        df_filtered = df_raw[
            (df_raw["Revision"] == selected_group) &
            (df_raw["Category"] == selected_product)
        ]
        df2=df_filtered.reset_index(drop=True)

        # Example calculation:
        # Let's assume the Excel sheet has a column "Value"
        if "Value" in df_filtered.columns:
            base_value = df_filtered["Value"].iloc[0]
        else:
            base_value = 1  # fallback default if not found

        total_value = amount * base_value




        #*******************************************


        #  *** process the calculations *******
        max_idx = df2.index.max()
        value=amount
        item=selected_product
        version=selected_group
    
    

    
        if df2.loc[max_idx, "max"] <=value:
            
            df2.loc[max_idx, "max"] = value
        
        #else:
        #    df2.loc[max_idx, "max"] = df2.loc[max_idx, "min"]
    

        for i in range(len(df2)):
            

            # usable
            if value > df2.loc[i, 'max']:
                df2.loc[i, 'usable']=df2.loc[i, 'max']            
            else:
                df2.loc[i, 'usable']=value
            # scrut
            if df2.loc[i, 'usable']>0:
                df2.loc[i, 'scrut'] = df2.loc[i, 'usable'] - df2.loc[i, 'min']            
            
            else:
                df2.loc[i, 'scrut'] = df2.loc[i, 'usable'] - df2.loc[i, 'min']            

            # actual   
            if df2.loc[i, 'scrut'] < 0:
                df2.loc[i, 'actual'] = 0
                
            else:
                df2.loc[i, 'actual'] = df2.loc[i, 'scrut']            

            # TaxAmount   
            if df2.loc[i, 'actual'] >= 0:
                df2.loc[i, 'Tax_amt'] = df2.loc[i, 'taxpercnt'] * df2.loc[i, 'actual']
                
            else:
                df2.loc[i, 'Tax_amt'] = 0

        if len(df2)==1:
            df2.loc[max_idx, 'actual'] = value
            df2.loc[max_idx, 'Tax_amt'] = df2.loc[max_idx, 'taxpercnt'] * df2.loc[max_idx, 'actual']

        #********************************************************
        if item=="Category B - Tax on annual gross sales":
              
            df2.loc[max_idx, "max"] = value
            
            # usable
            df2.loc[i, 'usable']=df2.loc[i, 'max']
            df2.loc[i, 'scrut'] = df2.loc[i, 'usable'] - df2.loc[i, 'min']
            if df2.loc[i, 'scrut']<=0:
                df2.loc[i, 'actual']=0
            else:            
                df2.loc[i, 'actual'] = df2.loc[i, 'scrut']
            df2.loc[max_idx, 'Tax_amt'] = df2.loc[max_idx, 'taxpercnt'] * df2.loc[max_idx, 'actual']
            df2.loc[max_idx, 'Tax_amt']=df2.loc[max_idx, 'Tax_amt'].round(2)
            if value>2000000:
                st.error("Error- you entered over 2Million, please recheck the values!" )
        if item=="Income from employment" or item=="Employment Income (Monthly)" :
            st.error("Employment Income, check if you have subtracted pension amount!-የመቀጠር ገቢ ጡረታ ቀንሰዋል?" )
        #**********************************************************
        total_amount=0
        if "Tax_amt" in df2.columns:
            total_amount = df2["Tax_amt"].sum().round(2)
            
        else:
            total_amount = 0

        # --- Display results ---
        if version== "After2025Revision-በ2017 የተሻሻለ":
            gizew= "በተሻሻለ 2017 አሠራር"
        else:
            gizew="ከ2017 ማሻማሻያ በፊት"

        if item=="Business Income (Annual)":
            minch="የንግድ ገቢ (ዓመታዊ)"
        
        elif item=="Capital Gains (Immovable Property – Class A)":    
            minch="የካፒታል ትርፍ (የማይንቀሳቀስ ንብረት - ክፍል ሀ)"
            
        elif item=="Capital Gains (Shares/Bonds – Class B)":    
            minch="የካፒታል ትርፍ (አክሲዮኖች / ቦንዶች - ክፍል ለ)"
            
        elif item=="Category B - Tax on annual gross sales":    
            minch="ደረጃ ለ - ዓመታዊ ጠቅላላ ሽያጮች ላይ ግብር"
            
        elif item=="Dividends":    
            minch="የትርፍ ድርሻ"
            
        elif item=="Employment Income (Monthly)":    
            minch="የሥራ ገቢ (ወርሃዊ)"
            
        elif item=="Entertainer Performance Taking Place in Ethiopia":    
            minch="የመዝናኛ አገልግሎቶች ገቢ በኢትዮጵያ"
            
        elif item=="Games of Chance":    
            minch="የዕድል ጨዋታዎች ገቢ"
            
        elif item=="Income from Business":    
            minch="ከንግድ ገቢ"
            
        elif item=="Income From Digital Content Creation":    
            minch="ዲጂታል ይዘት አገልግሎቶች ገቢ "
            
        elif item=="Income from Dividends":    
            minch="ከትርፍ ክፍፍል የተገኘ ገቢ"
            
        elif item=="Income from employment":    
            minch="ከመቀጠር የሚገኝ ገቢ"
            
        elif item=="Income from Games of Chance":    
            minch="ከዕድል ጨዋታዎች የተገኘ ገቢ"
            
        elif item=="Income from Interest  on Deposits":    
            minch="የተቀማጭ ገንዘብ ወለድ"
            
        elif item=="Income from rental of buildings":    
            minch="ከህንፃዎች ኪራይ የተገኘ ገቢ"
            
        elif item=="Income from Rental of Property":    
            minch="ከንብረት ኪራይ የተገኘ ገቢ"
            
        elif item=="Income from Royalties":    
            minch="ከሮያሊቲ የተገኘ ገቢ"
            
        elif item=="Income from Technical Services":    
            minch="ከቴክኒክ አገልግሎቶች የተገኘ ገቢ"
            
        elif item=="Rental Income (Annual)":    
            minch="የኪራይ ገቢ (ዓመታዊ)"
            
        elif item=="Royalties":    
            minch="ከሮያሊቲ"

        elif item=="Insurance Premium":    
            minch="የኢንሹራንስ አረቦን"

        elif item=="Interest on Deposits":    
            minch="የተቀማጭ ገንዘብ ወለድ"

        elif item=="Management or Technical Services Fee":    
            minch="ከሥራ አመራር ወይም ቴክኒክ አገልግሎቶች የተገኘ ገቢ"

        elif item=="Offshore Indirect Transfers (Gains From Ethiopia)":    
            minch="ቀጥተኛ ያልሆኑ ዝውውሮች (ከኢትዮጵያ የተገኙ ትርፍ) የተገኘ ገቢ"

        elif item=="Royalties Related to Art and Culture":    
            minch="ከጥበብ እና ባህል ጋር የተዛመዱ ሮያሊቲ የተገኘ ገቢ"
            
        else:
            print("Please enter your data again /እንደገና ይሞክሩ ")


        status = (
        f"This tax is approximate and does not consider interests, fines, pension or deductions, if any, check with Revenue Authorities! "
        f"The tax rule you chose is {version} . The taxable Income source you chose is {item}. The Income you provided is {value}. "
        f"Thus, total expected tax is {total_amount}\n"
        f"____________\n"
        f"ይህ ግብር ግምት ነው እና ምንም አይነት ወለድ፥ ቅጣት፥ ጡረታ እና ተቀናሾችን ግምት ውስጥ አያስገባም። እባክዎን ከገቢ ባለስልጣናት ጋር ያረጋግጡ።"
        f"የመረጡት የግብር ህግ {gizew} ነው። የመረጡት የገቢ ምንጭ {minch} ነው። ሪፖርት ያደረጉት ግብር የሚከፈልበት ገቢ {value} ነው።"
        f"ስለዚህ, አጠቃላይ የሚጠበቀው ግብር {total_amount} ነው።"    )
    
    
    
        print("Is running well")
        df_tax=df2[["range",'taxpercnt','actual','Tax_amt']]
        
        df_tax = df_tax.rename({'range':'Income_Range', 'taxpercnt':'Tax_Rate','actual':'Actual','Tax_amt':'Tax_Estimate'}, axis='columns')    

        df_tax["Tax_Rate"]=(df_tax["Tax_Rate"]*100.0).round(2)
        
        
        if df_tax.loc[max_idx, "Income_Range"] =="Any":
            df_tax['Income_Range']=""
            
            inc=(f" {value}")    
            df_tax.loc[max_idx, "Income_Range"] = inc #value
        else:
            pass

        df_tax['Tax_Estimate'] = df_tax['Tax_Estimate'].round(2)
        df_tax = df_tax.rename({'Income_Range':'Range_ከ_እስከ','Tax_Rate' :'Tax_Rate_ፐርሰንት','Actual':'On_Actual_ከፊል','Tax_Estimate':'Tax_ታክስ'}, axis='columns') 
    

        #***********************************
        #totaltax_rate=0
        totalActual=0
        totalEstimate=0
        

        for _, row in df_tax.iterrows():    
            
            #trv.insert('', 'end', values=list(row))
            #totaltax_rate +=row[1]
            totalActual +=row[2]
            totalEstimate +=row[3]
        #totalEstimate=totalEstimate.round(2)
        #print("totalrow =",totalActual ," TotEst=",totalEstimate)
        TRow = pd.DataFrame({'Range_ከ_እስከ':["Total"], 'Tax_Rate_ፐርሰንት':"-",'On_Actual_ከፊል':[totalActual],'Tax_ታክስ':[totalEstimate]})
        
        df_tax1=pd.concat((df_tax, TRow))
        df_tax1['On_Actual_ከፊል']=(df_tax1['On_Actual_ከፊል']).round(2)
        df_tax1['Tax_ታክስ']=(df_tax1['Tax_ታክስ']).round(2)
        #print(df_tax1)


        st.success(status)

        # -------------------------------------------------------
        # 6. Show reduced DataFrame
        # -------------------------------------------------------
        st.subheader("See Details-ዝርዝሩ ይኼው:")
        st.write(f"የመረጡት የግብር ህግ {gizew} ነው። የመረጡት የገቢ ምንጭ {minch} ነው። ሪፖርት ያደረጉት ግብር የሚከፈልበት ገቢ {value} ነው።")
        st.table(df_tax1)
        st.caption("Thanks for using this App, please send comments or corrections to: mihretbizu9@gmail.com ,thank you!")
        st.caption("References used are: 1) Income Tax Amendment - Proclamation No. 1395_2025 and \n 2) The Federal Income Tax Proclamation No. 97912016!")
        


