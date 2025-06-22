# 🏗️ UIA SDG Assessment Toolkit

A comprehensive web application for evaluating architecture projects' alignment with the UN Sustainable Development Goals (SDGs). Built with Streamlit and designed for the International Union of Architects (UIA).

## 🌟 Features

- **Comprehensive SDG Assessment**: Evaluate projects across all 17 UN Sustainable Development Goals
- **5Ps Framework Integration**: Analysis based on People, Planet, Prosperity, Peace, and Partnership
- **Interactive Visualizations**: Radar charts, pie charts, and performance breakdowns
- **Mobile-First Design**: Fully responsive interface optimized for all devices
- **Phase-Specific Recommendations**: Actionable insights for Design, Construction, and Operation phases
- **Synergy Analysis**: Recognition of how high performance in one SDG contributes to others

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/uia-sdg-assessment-toolkit.git
   cd uia-sdg-assessment-toolkit
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**
   - **Windows:**
     ```bash
     venv\Scripts\activate
     ```
   - **macOS/Linux:**
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Run the application**
   ```bash
   streamlit run app.py
   ```

6. **Open your browser**
   Navigate to `http://localhost:8501`

## 📊 How to Use

1. **Start Assessment**: Click "Begin Assessment" to start the evaluation process
2. **Answer Questions**: Complete the questionnaire across different SDG categories
3. **Review Results**: View comprehensive analysis with visualizations and insights
4. **Get Recommendations**: Access phase-specific recommendations for improvement

## 🏗️ Project Structure

```
uia-sdg-assessment-toolkit/
├── app.py                 # Main Streamlit application
├── toolkit_logic.py       # Core assessment logic and calculations
├── requirements.txt       # Python dependencies
├── README.md             # Project documentation
└── .gitignore           # Git ignore rules
```

## 🛠️ Technology Stack

- **Frontend**: Streamlit
- **Data Visualization**: Plotly
- **Data Processing**: Pandas, NumPy
- **Styling**: Custom CSS with mobile-first design
- **Deployment**: Streamlit Cloud ready

## 📱 Mobile Optimization

The application features:
- Responsive design for all screen sizes
- Touch-friendly interface
- Optimized navigation for mobile devices
- Enhanced visualizations for small screens

## 🎯 Assessment Framework

The toolkit evaluates projects based on:
- **Direct SDG Impact**: How directly the project addresses each SDG
- **Synergy Bonuses**: Recognition of cross-SDG benefits
- **5Ps Framework**: People, Planet, Prosperity, Peace, Partnership
- **Performance Levels**: Exemplary, Advanced, Basic, Minimal, No Score

## 📈 Visualizations

- **Radar Charts**: SDG performance overview
- **Pie Charts**: 5Ps framework distribution
- **Bar Charts**: Individual SDG breakdowns
- **Performance Distribution**: Overall assessment results

## 🔧 Customization

The toolkit can be customized by:
- Modifying question weights in `toolkit_logic.py`
- Adjusting color schemes in `app.py`
- Adding new SDG categories or questions
- Customizing recommendation algorithms

## 🚀 Deployment

### Streamlit Cloud Deployment

1. **Push to GitHub**: Ensure your code is in a public GitHub repository
2. **Connect to Streamlit Cloud**: 
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Sign in with GitHub
   - Select your repository
   - Deploy

### Local Deployment

```bash
streamlit run app.py --server.port 8501 --server.address 0.0.0.0
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **UIA (International Union of Architects)** for the framework
- **UN Sustainable Development Goals** for the assessment criteria
- **Streamlit** for the web application framework
- **Plotly** for data visualization capabilities

## 📞 Support

For support and questions:
- Create an issue in the GitHub repository
- Contact the development team
- Check the documentation in the code comments

## 🔄 Version History

- **v1.0.0**: Initial release with basic SDG assessment
- **v1.1.0**: Enhanced mobile optimization and visualizations
- **v1.2.0**: Added 5Ps framework and synergy analysis

---

**Built with ❤️ for sustainable architecture** 