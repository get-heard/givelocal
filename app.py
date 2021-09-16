#import packages
import streamlit as st
import pandas as pd
import numpy as np

#the heading of the app
st.title('Charities Near Me')

# add image
st.image(image="Image by Tumisu from Pixabay.png")

#creates a cached dataframe which only needs to load once
df = st.cache(pd.read_csv)("CharityBase.zip")

st.sidebar.title("Did you know?")

#counts the total number of charities, adds comma separator and displays
total_number_of_charities = len(df.index)
total_number_of_charities = ("{:,}".format(total_number_of_charities)) 
st.sidebar.write('Number of charities registered with the UK Charity Commission:',total_number_of_charities)

# adds total income of all charities, converts to integer, formats with comma separator and displays
total = df['Income'].sum()
total = int(total)
total = ("{:,}".format(total)) 
st.sidebar.write('Total annual income of registered charities: £',total)

# staff total
staff = df['Employees'].sum()
staff = int(staff)
staff = ("{:,}".format(staff)) 
st.sidebar.write('Total number of employees: ',staff)

# volunteers total
volunteers = df['Volunteers'].sum()
volunteers = int(volunteers)
volunteers = ("{:,}".format(volunteers)) 
st.sidebar.write('Total number of volunteers: ',volunteers)

# trustees total
trustees = df['Trustees'].sum()
trustees = int(trustees)
trustees = ("{:,}".format(trustees)) 
st.sidebar.write('Total number of trustees: ',trustees)


# acknowledgment
st.sidebar.write('All data from: https://charitybase.uk')

# subheading
st.markdown("### Search for charities in your area")

# prompts for postcode and makes first letter upper case
authority= st.text_input("To find nearby charities in England or Wales please enter all or part of your local authority name and press return")
authority= authority.capitalize()

# this runs if an entry is made in the box
if authority:
	#creates a new dataframe df1 with rows containing the authority
	df1=df[df['LAUA'].str.contains(authority, na=False)]
	
	#sets index column to charity name
	df1=df1.set_index('Name')
	
	# renames these columns so Streamlit recognises them for the mapping
	df1=df1.rename(columns ={'Latitude': 'latitude'})
	df1=df1.rename(columns ={'Longitude':'longitude'})

	# sorts records by high to low income
	df1.sort_values(by=['Income'], inplace=True, ascending=False)

	# new dataframe df2 with fewer column headings
	df2=df1[['Address','Postcode','Income', 'Spending', 'Financial Year','LAUA']]
	
	# counts number of charities in area and displays
	number_of_charities = len(df2.index)
	number_of_charities = ("{:,}".format(number_of_charities)) 
	st.write('Number of charities in this area is:', number_of_charities)

	# finds biggest charity formats as integer with comma separator and displays
	max = df2['Income'].max()
	max = int(max)
	max = ("{:,}".format(max)) 
	st.write('The biggest charity in this area has annual income of: £', max)
	
	# find total income overall formats as integer with comma separator and displays
	sum = df2['Income'].sum()
	sum = int(sum)
	sum = ("{:,}".format(sum)) 
	st.write('The total annual income of all charities in this area is: £',sum)

	# average income per charity
	average	= df2['Income'].sum()/len(df2.index)
	average = round(average,2)
	average = ("{:,}".format(average)) 
	st.write('The average annual income per charity in this area is: £',average)

# subheading
st.markdown("### To view data select one or more boxes")

# checkbox for top 20
is_check = st.checkbox("Show top twenty by income")
if is_check:
    st.write(df2.head(20))

# checkbox for all
is_check = st.checkbox("Show all")
if is_check:
    st.write(df2)

# checkbox for bar chart with ward breakdown
is_check = st.checkbox("Show breakdown by ward")
if is_check:
    st.bar_chart(df1["Ward"].value_counts())

# checkbox for map
is_check = st.checkbox("Show charities on a map")
if is_check:
    st.map(df1)
