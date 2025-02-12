# 🚀 Streamlit SQL Dashboard with LLM Analysis  


https://github.com/user-attachments/assets/ecb5de97-9484-45c5-9111-8df2de38d3a3

This **interactive Streamlit dashboard** allows users to **connect to a MySQL database, run SQL queries, visualize data, and analyze results** using an **LLM (Large Language Model)**.  

---

## **📌 Features**
✅ **MySQL Connection Setup**  
- Users can enter **host, port, username, password, and database name** to establish a connection.  

✅ **SQL Query Execution**  
- Users can write and execute **SELECT, INSERT, UPDATE, DELETE** queries.  
- Results are displayed as an **editable table**.  

✅ **Data Visualization**  
- Supports multiple chart types: **Line, Bar, Pie, Scatter, Grouped Bar, and Area Charts**.  
- Interactive **date filtering** for time-based data.  

✅ **AI-Powered Data Analysis**  
- Uses **LangChain Ollama LLM (e.g., Phi-4, LLaMA3.1)** to **analyze the dataset** and provide **descriptive statistics and insights**.  

✅ **Error Handling & Security**  
- Handles **database connection errors** gracefully.  
- **Prevents SQL injection** with **parameterized queries**.  


## **Tech Stack**
+ Streamlit → Interactive UI
+ SQLAlchemy → Database connection
+ MySQL → Backend database
+ Pandas → Data processing
+ Plotly → Data visualization
+ LangChain + Ollama → AI-powered analysis

## **How It Works**
1. Set up MySQL connection in the UI.
2. Enter and run SQL queries to fetch data.
3. View & edit the data in a table.
4. Create charts using dropdown selections.
5. Run AI analysis on the dataset with LLM insights.

## **Future Improvements**
- Support for PostgreSQL
- Advanced filtering options
- Integration with OpenAI GPT models using API

## Contribution
Feel free to fork this project, submit pull requests, or report issues!

## License
This project is licensed under the MIT License.

## Useful references
- [Ollama phi4](https://ollama.com/library/phi4)
- [Streamlit](https://streamlit.io)
- [Data base: clasicmodels](https://www.mysqltutorial.org/getting-started-with-mysql/mysql-sample-database/)


