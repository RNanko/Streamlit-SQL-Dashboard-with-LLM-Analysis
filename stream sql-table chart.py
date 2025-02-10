import streamlit as st
import plotly.express as px
from sqlalchemy import create_engine, inspect
from langchain_ollama.llms import OllamaLLM
import pandas as pd
from sqlalchemy.exc import OperationalError
import time


st.set_page_config(layout="wide")

# Ensure session state keys exist
if "table" not in st.session_state:
    st.session_state.table = None


if "query" not in st.session_state:
    st.session_state.query = None  # Default empty query

if "connection_string" not in st.session_state:
    st.session_state.connection_string = None

if 'analysis' not in st.session_state:
    st.session_state.analysis = None



col_1, col_2 = st.columns(2)

with col_1:

    c_1, c_2 = st.columns([15, 70])

    c_2.write("#### Set Up/Check connection to MySQL database")
    

    with c_1.popover('MySQL setup'):  # Popover for MySQL configuration
        st.markdown('### Enter MySQL Connection Details')

        # User inputs
        db_host = st.text_input("Host", value="localhost")
        db_port = st.text_input("Port", value="3306")
        db_user = st.text_input("Username", value="newuser")
        db_password = st.text_input("Password", type='password')
        db_name = st.text_input("Database Name", value="classicmodels")

        # Button to confirm and save the connection string
        if st.button("Confirm"):
            st.session_state.connection_string = f"mysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
            st.success("Connection string saved successfully!")
        

        # SQL Query Input
    st.session_state.query = st.text_area("Enter SQL query", height=200)
    if st.session_state.query:
        try:
            # Ensure connection string is set
            if not st.session_state.connection_string:
                st.warning("MySQL connection string is missing! Please set it in MySQL Setup.", icon="⚠️")
            else:
                # Create database engine
                engine = create_engine(st.session_state.connection_string)

                # Execute query and fetch data into DataFrame
                with engine.connect() as conn:
                    st.session_state.table = pd.read_sql(st.session_state.query, conn)


        except OperationalError as e:
            alert_1 = st.error("❌ **Database Connection Failed**")
            alert_2 = st.warning(f"Error: {e}", icon="⚠️")
            time.sleep(3) # Wait for 2 seconds
            alert_1.empty()
            alert_2.empty()

        except Exception as e:

            alert_1 = st.error("❌ **Database Connection Failed**")
            alert_2 = st.warning(f"SQL Error: {e}", icon="⚠️")
            time.sleep(3) # Wait for 2 seconds
            alert_1.empty()
            alert_2.empty()
    

    with st.container(height=700):
        if st.session_state.table is not None:
            st.write("#### Table Preview")
            edited_df = st.data_editor(
                            st.session_state.table,
                            hide_index=True,
                            use_container_width=True,
                            height=int(35.2*(len(st.session_state.table)+1))
                        )
        else:
            st.write("Run the query to see the table!")



with col_2:
        
        tab_chart, tab_analysis = st.tabs(["Chart", "Analysis"])

        with tab_chart:

            if st.session_state.table is None:
                st.write("Run the query to see the table!")
                st.write('### DB schema')
                st.image("Schema.png")
            else:  # Editable Table
                st.write("### Table-Chart")

            if st.session_state.table is not None:

                col1, col2, col3 = st.columns(3)
                # Hue (Z-axis) selection
                z = col1.selectbox("Color", list(st.session_state.table.columns), index=None, placeholder="Choose an option")

                # X-axis selection
                x = col2.selectbox("X-axis", list(st.session_state.table.columns), index=None,
                                placeholder="Choose an option")

                # Y-axis selection (multiple for comparison)
                y = col3.multiselect("Y-axis", list(st.session_state.table.columns))

                cl_1, cl_2 = st.columns([30, 70])

                # Checkbox to mark X as a date column
                check_box_data = cl_1.checkbox('X is data column')
 
                try:
                    if check_box_data:
                        # Drop empty rows
                        edited_df = edited_df.dropna(subset=[x])
                        # Convert X column to date
                        edited_df[x] = pd.to_datetime(edited_df[x]).dt.date  

                        # Date range filter using select_slider
                        date_range = st.select_slider(
                            "Select a date range",
                            options=sorted(edited_df[x].unique()),  # Ensure proper ordering
                            value=(edited_df[x].min(), edited_df[x].max())  # Default range
                        )
                        
                        # Apply filtering
                        edited_df = edited_df[(edited_df[x] >= date_range[0]) & (edited_df[x] <= date_range[1])]

                except Exception as e:
                    st.warning(f"⚠️ Error processing dates: {e}")


                if x and y: 
                    with st.expander("Edited Table"):
                        edited_df = st.data_editor(
                            edited_df,
                            hide_index=True,
                            use_container_width=True)
                    

                chart_type = st.segmented_control("Chart Type",
                                                ["Line", "Bar", "Pie", "Dot", "Grouped Bar", "Area"])


                fig = None  # Initialize figure

                if x and y:
  
                # Line Chart
                    if chart_type == "Line":
                        fig = px.line(edited_df.sort_values(by=x), x=x, y=y, color=z if z else None, title="Line Chart")
                        fig.update_traces(hoverinfo="x+y", hovertemplate="X: %{x}<br>Y: %{y}")

                    # Bar Chart
                    elif chart_type == "Bar":
                        edited_df[y] = edited_df[y].astype(float)
                        fig = px.bar(edited_df, x=x, y=y, color=z if z else None, title="Bar Chart", barmode="group")
                        fig.update_traces(hoverinfo="x+y", hovertemplate="X: %{x}<br>Y: %{y}")

                    # Pie Chart (only supports one Y variable)
                    elif chart_type == "Pie":
                        if len(y) > 1:
                            st.warning("⚠️ Pie chart only supports one Y variable.")
                        else:
                            fig = px.pie(edited_df, names=x, values=y[0], color=z if z else None, title="Pie Chart")
                            fig.update_traces(hoverinfo="label+percent+value", hovertemplate="%{label}: %{percent} (%{value})")

                    # Scatter (Dot) Chart
                    elif chart_type == "Dot":
                        fig = px.scatter(edited_df, x=x, y=y, color=z if z else None, title="Scatter Plot")
                        fig.update_traces(mode="markers", hoverinfo="x+y", hovertemplate="X: %{x}<br>Y: %{y}")

                    # Grouped Bar Chart
                    elif chart_type == "Grouped Bar":
                        fig = px.bar(edited_df, x=x, y=y, color=z if z else None, barmode="group", title="Grouped Bar Chart")
                        fig.update_traces(hoverinfo="x+y", hovertemplate="X: %{x}<br>Y: %{y}")

                    # Area Chart
                    elif chart_type == "Area":
                        fig = px.area(edited_df, x=x, y=y, color=z if z else None, title="Area Chart")
                        fig.update_traces(hoverinfo="x+y", hovertemplate="X: %{x}<br>Y: %{y}")

  

                    # Display the chart
                    if fig:
                        st.plotly_chart(fig, use_container_width=True)

        with tab_analysis:
            st.write("### LLM Analysis of Table")
            
            if st.button("Run Analysis", use_container_width=True):
                
                with st.status("Running analysis..."):
                        # phi4  llama3.1
                    model = OllamaLLM(model='phi4', max_tokens=4096)
                    # , temperature=0.5, repeat_penalty=1.15, top_k=50,
                    # Convert DataFrame to JSON format
                    data_json = st.session_state.table.to_json(orient="records", indent=4)

                    # Construct the prompt for the language model using JSON data
                    prompt = f"""
                    You famous data analyst. Using analytical skills give a summary about data.
                    Short descriptive Min, max, moda, median statistics in text form.
                    Recommendation and Nuances what you see. Try to identify any trends or patterns.

                    The data retrieved from the query is in JSON format:
                    {data_json}

                    Write only text summary in one format.
                    """
                    st.session_state.analysis = model.invoke(prompt)
            
            if st.session_state.analysis:
                st.write(st.session_state.analysis)
            
            else:
                st.write("No analysis to show")
   