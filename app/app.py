import streamlit as st

class CryptoOptApp:
    def __init__(self):
        self.title = "CryptoOpt App"
        self.sidebar_options = ["Home", "Optimization", "Experiments", "Metrics"]
        self.current_page = "Home"

    def run(self):
        st.set_page_config(page_title=self.title, page_icon=":chart_with_upwards_trend:")

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
        self.current_page = st.sidebar.radio("Navigation", self.sidebar_options)

    def home_page(self):
        st.title("Welcome to CryptoOpt App")
        st.write("Explore different functionalities using the sidebar.")

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
