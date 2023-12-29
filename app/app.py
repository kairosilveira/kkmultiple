import streamlit as st
import markdown
from data.fetch_data import get_historical_crypto_data
import pandas as pd

class CryptoOptApp:
    def __init__(self):
        self.title = "CryptoOpt App"
        self.sidebar_options = [
            "Home", "Optimization", "Experiments", "Metrics"]
        self.current_page = "Home"

    def load_markdown(self,file_name):
        with open(file_name, 'r') as file:
            markdown_text = file.read()

        return markdown.markdown(markdown_text)

    def run(self):
        st.set_page_config(page_title=self.title,
                           page_icon=":chart_with_upwards_trend:")

        self.sidebar()

        if self.current_page == "Home":
            self.home_page()
        elif self.current_page == "Optimization":
            self.optimization_page()
        elif self.current_page == "Experiments":
            self.experiments_page()
        elif self.current_page == "Metrics":
            self.metrics_page()

    def sidebar(self):
        st.sidebar.title(self.title)
        self.current_page = st.sidebar.radio(
            "Navigation", self.sidebar_options)

    def home_page(self):
        st.title("Welcome to KK Multiple App")
        st.markdown("""
        <br>
        <br>
        """,unsafe_allow_html=True)
        
        data = get_historical_crypto_data('2014-01-01', '2023-12-31', 'Close', 'BTC-USD')
        df = pd.DataFrame(data, columns= data.columns)
        df['date'] = df['date'].astype('datetime64[ns]')
        st.line_chart(data= df, x='date', y='price', color=None, width=0, height=0, use_container_width=True)
        
        html_content = self.load_markdown("app/markdown_files/main_page.md")
        st.markdown(html_content, unsafe_allow_html=True)
        st.latex(r"Multiple = \frac{Price}{MA_n}")
        st.markdown("where Price is the current price of Bitcoin and $MA_n$ is N day moving average value", unsafe_allow_html=True)

        # st.markdown(html_content, unsafe_allow_html=True)

    def optimization_page(self):
        st.title("Optimization Page")
        st.write("This page is for optimizing parameters.")

    def experiments_page(self):
        st.title("Experiments Page")
        st.write("This page is for running experiments.")

    def metrics_page(self):
        st.title("Metrics Page")
        st.write("This page is for calculating metrics.")


if __name__ == "__main__":
    crypto_opt_app = CryptoOptApp()
    crypto_opt_app.run()
