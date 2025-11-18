# 📖 Faith Based Survey Intelligence Dashboard  
### Digital Discipleship, Data, and Human Flourishing  

## 🚀 Overview  

Does engaging with digital Scripture actually improve quality of life?

This project is a **Product Intelligence Dashboard** that analyzes weighted survey data to explore the relationship between:

- Scripture engagement  
- Digital faith habits (online, hybrid, in person)  
- Core life outcomes (Happiness, Health, Family connection)  

The dashboard is built with **Streamlit** and **Plotly**, and is designed to showcase **Senior Data Analytics** capability in a faith based context:

- Translating raw survey microdata into **strategic, product level insights**  
- Quantifying the impact of **digital discipleship** on human flourishing  

---

## 📊 Dashboard Architecture  

The app is organized into **4 strategic tabs** with **12 high fidelity visualizations**.

### 1. 🌱 The Flourishing Index (Impact Analysis)  
**Focus: Proving the value proposition.**

- **Flourishing Radar**  
  - Multi variable radar chart for **Happiness**, **Health**, and **Family**  
  - Compares **High Engagement** vs **Low Engagement** Scripture users  

- **Happiness Violin Plots**  
  - Distribution of happiness across levels of **Scripture importance**  
  - Shows shape and spread, not just averages  

- **Disciple’s Funnel**  
  - Funnel from:  
    - Religious interest  
    - General faith importance  
    - Active Scripture engagement  
  - Highlights drop off points in the journey from belief to practice  

---

### 2. 📱 The Digital Ecosystem (Engagement Flow)  
**Focus: Understanding user behavior.**

- **Ecosystem Flow (Parallel Categories)**  
  - Tracks user journey:  
    - **Generation** → **Faith Importance** → **Digital / Hybrid / In Person** status  

- **Engagement Sunburst**  
  - Hierarchical breakdown of user segments:  
    - Digital first  
    - Hybrid  
    - Disconnected / low engagement  

- **Market Share Donut**  
  - Ratio of:  
    - Hybrid believers  
    - Purely Online  
    - Purely In Person  

---

### 3. 👥 Generational Trends (Demographics)  
**Focus: Strategic growth areas.**

- **The Matrix (Animated Bubble Chart)**  
  - Animated across survey years (for example 2023 to 2024)  
  - Bubbles represent generations (for example Boomers, Gen X, Millennials, Gen Z)  
  - Position shows Online vs In Person intensity  

- **Attendance Gap**  
  - Compares online vs physical participation by **decade of birth**  

- **Scripture Cliff**  
  - Trend line of **Scripture importance by age cohort**  
  - Visualizes where perceived importance drops or holds steady  

---

### 4. 🔬 Deep Correlations (Data Science)  
**Focus: Statistical validation.**

- **Correlation Matrix Heatmap**  
  - Correlations between:  
    - Online participation  
    - In person attendance  
    - Scripture importance  
    - Happiness, Health, Family satisfaction  

- **Worldview Stacked Bar (100 percent normalized)**  
  - Composition of happiness levels within key segments  
  - Each bar sums to 100 percent for direct comparison  

- **Demographic Histograms**  
  - Age distribution overlays  
  - Used to contextualize digital vs traditional engagement patterns  

---

## 🛠️ Technical Implementation  

### Data Pipeline  

- **Weighted Analysis**  
  - Uses `weight_final` so all visuals represent the real target population, not just the raw sample  
  - All counts are based on `SUM(weight_final)`  

- **Ordinal Mapping**  
  - Categorical responses (for example “Extremely important”, “Once a week”, “Never”)  
  - Mapped to numeric scores (for example 0 to 5)  
  - Enables radar charts, trend lines, and correlation analysis  

- **Performance**  
  - Uses `@st.cache_data` to load and preprocess the CSV once per session  
  - Keeps tab switching responsive even on large survey files  

### Key Libraries  

- **Streamlit**  
  - Application framework, layout, and user interaction  

- **Plotly Express / Graph Objects**  
  - Interactive charts with zoom, hover, and filter awareness  

- **Pandas / NumPy**  
  - Data cleaning, transformation, weighting, and aggregation  

---

## 💻 Installation and Setup  

To run the dashboard locally:

```bash
# Clone the repository
git clone https://github.com/rlancaster243/Faith-Based-Survey-Intelligence-Dashboard.git
cd Faith-Based-Survey-Intelligence-Dashboard

# Install dependencies
pip install -r requirements.txt

# Run the Streamlit app
streamlit run app.py
```
## 🔮 Future Roadmap

If promoted from portfolio project to production analytics, the next steps would include:

### Real Time Telemetry  
Connect to live application event streams such as:  
- Reading streaks  
- Plans completed  
- Notification interactions  

### NLP Sentiment Analysis  
Analyze open text responses such as *“Why do you engage with Scripture?”* using:  
- NLTK  
- spaCy  
- External LLM APIs  
to extract key themes and emotional tone.

### A/B Test Experiment Tracking  
Create dedicated views to measure uplift from:  
- Daily reminder notifications  
- New Scripture engagement surfaces  
- Other product experiments  

### Multi Dataset Integration  
Combine survey data with in app event streams to produce richer, behavior driven models for:  
- Engagement prediction  
- Recommendation systems  
- Personalized discipleship pathways

Created by **Russell Lancaster** as part of a **Data Analyst portfolio**, focused on **Faith Based Product Intelligence** and **Digital Discipleship**.
