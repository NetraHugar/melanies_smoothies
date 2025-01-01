# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session

# Write directly to the app
st.title(":cup_with_straw: Create Your Smoothie! :cup_with_straw:")
st.write(
   "Choose the fruits you want in your custom Smoothie!"
)
from snowflake.snowpark.functions import col
from snowflake.snowpark.functions import when_matched

cnx = st.connection("snowflake")
session = cnx.session()
#my_dataframe = session.table("smoothies.public.fruit_options").select(col('fruit_name'))
#st.dataframe(data=my_dataframe, use_container_width=True)

my_dataframe = session.table("smoothies.public.orders").filter(col("ORDER_FILLED")==0).collect()
editable_df = st.data_editor(my_dataframe)

submitted = st.button('Submit')

if submitted:
    st.success('Someone clicked the button', icon = '👍')

    og_dataset = session.table("smoothies.public.orders")
    edited_dataset = session.create_dataframe(editable_df)
    try:
        og_dataset.merge(edited_dataset
                     , (og_dataset['ORDER_UID'] == edited_dataset['ORDER_UID'])
                     , [when_matched().update({'ORDER_FILLED': edited_dataset['ORDER_FILLED']})]
                    )

        st.success('Order(s) updated!', icon = '👍')
    except:
        st.write('Something went wrong.')
