import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# -----------------------------------------------------------------------------
# 1. PAGE CONFIGURATION & STYLING
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Insights | Faith & Data",
    page_icon="📖",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .metric-card {
        background-color: #f0f2f6;
        border-radius: 10px;
        padding: 20px;
        text-align: center;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
    }
    div.stTabs > div > div > div > div {
        font-weight: bold;
        font-size: 1.2rem;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 2. DATA LOADING & PREPROCESSING
# -----------------------------------------------------------------------------
@st.cache_data
def load_data():
    # Load dataset (Ensure the file is in the same directory)
    df = pd.read_csv('rls_tableau_weighted_core1.csv')
    
    # --- Mappings for Ordinal Variables to Numeric Scores (0-5 Scale) ---
    # This allows us to calculate averages for Radar charts and Heatmaps
    maps = {
        'happiness': {'Very happy': 3, 'Pretty happy': 2, 'Not too happy': 1},
        'health_family': {'Excellent': 5, 'Very good': 4, 'Good': 3, 'Fair': 2, 'Poor': 1},
        'importance': {'Extremely important': 5, 'Very important': 4, 'Somewhat important': 3, 'Not too important': 2, 'Not at all important': 1},
        'freq': {'More than once a week': 6, 'Once a week': 5, 'Once or twice a month': 4, 'A few times a year': 3, 'Seldom': 2, 'Never': 1}
    }

    # Create Numeric Columns
    df['happiness_score'] = df['generally_how_happy_are_you_with_your_life_these_days_are_you'].map(maps['happiness'])
    df['health_score'] = df['would_you_say_your_health_in_general_is_excellent_very_good_good_fair'].map(maps['health_family'])
    df['family_score'] = df['would_you_say_your_family_life_is_excellent_very_good_good_fair_or'].map(maps['health_family'])
    df['bible_score'] = df['how_important_is_the_bible_in_your_life'].map(maps['importance'])
    df['online_score'] = df['how_often_do_you_watch_or_participate_in_religious_services_online_or'].map(maps['freq'])
    df['in_person_score'] = df['how_often_do_you_attend_religious_services_in_person'].map(maps['freq'])

    # Create Segments for Analysis
    df['Bible Engagement'] = np.where(df['bible_score'] >= 4, 'High Engagement', 'Low Engagement')
    
    def get_digital_segment(row):
        if row['online_score'] >= 5 and row['in_person_score'] <= 2:
            return 'Digital First'
        elif row['online_score'] >= 4 and row['in_person_score'] >= 4:
            return 'Hybrid'
        elif row['in_person_score'] >= 4:
            return 'In-Person Only'
        else:
            return 'Disconnected'
            
    df['User Type'] = df.apply(get_digital_segment, axis=1)
    
    return df

df = load_data()

# -----------------------------------------------------------------------------
# 3. SIDEBAR FILTERS
# -----------------------------------------------------------------------------
with st.sidebar:
    
    st.title("Analyst Portal")
    st.write("Exploratory Analysis of Faith, Tech, and Life Outcomes.")
    
    selected_years = st.multiselect("Select Years", options=sorted(df['year_in_which_survey_was_completed'].unique()), default=[2023, 2024])
    selected_gens = st.multiselect("Select Generations", options=df['decade_in_which_respondent_was_born'].dropna().unique(), default=['1980s', '1990s', '2000s'])

    # Apply Filters
    df_filtered = df[df['year_in_which_survey_was_completed'].isin(selected_years)]
    if selected_gens:
        df_filtered = df_filtered[df['decade_in_which_respondent_was_born'].isin(selected_gens)]

# -----------------------------------------------------------------------------
# 4. MAIN DASHBOARD TABS
# -----------------------------------------------------------------------------
st.title("🚀 Faith Based Product Intelligence Dashboard")
st.markdown("### *Does digital scripture engagement lead to a flourishing life?*")

tab1, tab2, tab3, tab4 = st.tabs([
    "🌱 The Flourishing Index", 
    "📱 The Digital Ecosystem", 
    "👥 Generational Trends",
    "🔬 Deep Correlations"
])

# --- TAB 1: IMPACT (The "Why") ---
with tab1:
    st.markdown("#### Measuring the 'Scripture Effect' on Quality of Life")
    
    col1, col2, col3 = st.columns(3)
    
    # VISUAL 1: Metrics
    total_pop = df_filtered['weight_final'].sum()
    high_bible_pct = (df_filtered[df_filtered['Bible Engagement'] == 'High Engagement']['weight_final'].sum() / total_pop) * 100
    avg_happy = df_filtered['happiness_score'].mean()
    
    col1.metric("Total Population Rep.", f"{int(total_pop):,}")
    col2.metric("High Bible Engagement", f"{high_bible_pct:.1f}%")
    col3.metric("Avg Happiness Score (1-3)", f"{avg_happy:.2f}")
    
    col_a, col_b = st.columns([1, 1])
    
    with col_a:
        # VISUAL 2: Radar Chart (The Flourishing Profile)
        st.subheader("1. The Flourishing Profile")
        radar_df = df_filtered.groupby('Bible Engagement')[['happiness_score', 'health_score', 'family_score']].mean().reset_index()
        
        # Normalize for radar (scale 0-1) roughly for visual
        categories = ['Happiness', 'Physical Health', 'Family Life']
        
        fig_radar = go.Figure()
        for segment in radar_df['Bible Engagement'].unique():
            d = radar_df[radar_df['Bible Engagement'] == segment]
            fig_radar.add_trace(go.Scatterpolar(
                r=[d['happiness_score'].values[0], d['health_score'].values[0], d['family_score'].values[0]],
                theta=categories,
                fill='toself',
                name=segment
            ))
        fig_radar.update_layout(polar=dict(radialaxis=dict(visible=True)), showlegend=True, height=400)
        st.plotly_chart(fig_radar, use_container_width=True)

    with col_b:
        # VISUAL 3: Violin Plot (Happiness Distribution)
        st.subheader("2. Happiness Distribution")
        fig_violin = px.violin(df_filtered, y="happiness_score", x="how_important_is_the_bible_in_your_life", 
                               color="Bible Engagement", box=True, points=False,
                               category_orders={"how_important_is_the_bible_in_your_life": ["Not at all important", "Somewhat important", "Extremely important"]},
                               title="Happiness density by Bible Importance")
        st.plotly_chart(fig_violin, use_container_width=True)
        
    # VISUAL 4: The Engagement Funnel
    st.subheader("3. The Disciple's Funnel")
    funnel_data = {
        'Stage': ['Religion Important', 'Attends Service (Any)', 'High Bible Engagement'],
        'Count': [
            df_filtered[df_filtered['how_important_is_religion_in_your_life'].isin(['Very important', 'Somewhat important'])]['weight_final'].sum(),
            df_filtered[df_filtered['User Type'] != 'Disconnected']['weight_final'].sum(),
            df_filtered[df_filtered['Bible Engagement'] == 'High Engagement']['weight_final'].sum()
        ]
    }
    fig_funnel = px.funnel(funnel_data, x='Count', y='Stage', color='Stage')
    st.plotly_chart(fig_funnel, use_container_width=True)

# --- TAB 2: ENGAGEMENT (The "How") ---
with tab2:
    st.markdown("#### Understanding the Shift: Physical vs. Digital")
    
    col_c, col_d = st.columns(2)
    
    with col_c:
        # VISUAL 5: Parallel Categories (The Ecosystem Flow)
        st.subheader("4. Ecosystem Flow: Gen -> Faith -> Habits")
        # Sample down for performance if needed, but weighted usually needs aggregation. 
        # For ParCats, we'll use raw counts of a sample or binned data.
        fig_parcats = px.parallel_categories(
            df_filtered.sample(n=min(2000, len(df_filtered))), # Sample for visual clarity
            dimensions=['decade_in_which_respondent_was_born', 'how_important_is_religion_in_your_life', 'User Type'],
            color="happiness_score", 
            color_continuous_scale=px.colors.sequential.Inferno,
            title="Flow of Faith: From Generation to Digital Habit"
        )
        st.plotly_chart(fig_parcats, use_container_width=True)
        
    with col_d:
        # VISUAL 6: Sunburst (Hierarchy)
        st.subheader("5. Engagement Hierarchy")
        fig_sun = px.sunburst(
            df_filtered, 
            path=['User Type', 'how_important_is_the_bible_in_your_life'], 
            values='weight_final',
            title="User Segments Breakdown"
        )
        st.plotly_chart(fig_sun, use_container_width=True)
        
    # VISUAL 7: Donut Chart
    st.subheader("6. The 'Hybrid' Believer Share")
    fig_donut = px.pie(df_filtered, names='User Type', values='weight_final', hole=0.5, title="Market Share of Digital vs Physical")
    st.plotly_chart(fig_donut, use_container_width=True)

# --- TAB 3: DEMOGRAPHICS (The "Who") ---
with tab3:
    st.markdown("#### Generational shifts in Faith & Technology")
    
    # VISUAL 8: Animated Bubble Chart
    st.subheader("7. Generational Clusters (Animated by Year)")
    # Aggregate for bubble
    bubble_df = df.groupby(['decade_in_which_respondent_was_born', 'year_in_which_survey_was_completed']).agg({
        'online_score': 'mean',
        'in_person_score': 'mean',
        'bible_score': 'mean',
        'weight_final': 'sum'
    }).reset_index()
    
    fig_bubble = px.scatter(
        bubble_df, 
        x="online_score", y="in_person_score", 
        size="weight_final", color="bible_score",
        animation_frame="year_in_which_survey_was_completed",
        hover_name="decade_in_which_respondent_was_born",
        range_x=[1,6], range_y=[1,6],
        title="The Matrix: Online vs In-Person Attendance by Generation",
        labels={"online_score": "Online Frequency (Score)", "in_person_score": "In-Person Frequency (Score)"}
    )
    st.plotly_chart(fig_bubble, use_container_width=True)
    
    col_e, col_f = st.columns(2)
    
    with col_e:
        # VISUAL 9: Grouped Bar
        st.subheader("8. Attendance Gap")
        gap_df = df_filtered.groupby('decade_in_which_respondent_was_born')[['online_score', 'in_person_score']].mean().reset_index()
        gap_melt = gap_df.melt(id_vars='decade_in_which_respondent_was_born', var_name='Type', value_name='Score')
        fig_bar = px.bar(gap_melt, x='decade_in_which_respondent_was_born', y='Score', color='Type', barmode='group', title="Online vs In-Person Intensity")
        st.plotly_chart(fig_bar, use_container_width=True)

    with col_f:
        # VISUAL 10: Trend Line
        st.subheader("9. The Bible 'Cliff'")
        line_df = df_filtered.groupby('decade_in_which_respondent_was_born')['bible_score'].mean().reset_index()
        fig_line = px.line(line_df, x='decade_in_which_respondent_was_born', y='bible_score', markers=True, title="Avg Bible Importance by Decade")
        st.plotly_chart(fig_line, use_container_width=True)

# --- TAB 4: DEEP DIVE (Data Science) ---
with tab4:
    st.markdown("#### Statistical Correlations")
    
    col_g, col_h = st.columns(2)
    
    with col_g:
        # VISUAL 11: Heatmap
        st.subheader("10. Correlation Matrix")
        corr_cols = ['happiness_score', 'health_score', 'family_score', 'bible_score', 'online_score', 'in_person_score']
        corr_matrix = df_filtered[corr_cols].corr()
        fig_heat = px.imshow(corr_matrix, text_auto=True, color_continuous_scale='RdBu_r', title="Variable Correlations")
        st.plotly_chart(fig_heat, use_container_width=True)
        
    with col_h:
        # VISUAL 12: 100% Stacked Bar (Worldview)
        st.subheader("11. Happiness vs Bible (Detailed)")
        # Grouping for stacked bar
        stack_df = df_filtered.groupby(['how_important_is_the_bible_in_your_life', 'generally_how_happy_are_you_with_your_life_these_days_are_you'])['weight_final'].sum().reset_index()
        # Calculate percentages
        stack_df['percentage'] = stack_df.groupby('how_important_is_the_bible_in_your_life')['weight_final'].transform(lambda x: x / x.sum())
        
        fig_stack = px.bar(stack_df, x="how_important_is_the_bible_in_your_life", y="percentage", 
                           color="generally_how_happy_are_you_with_your_life_these_days_are_you", 
                           title="Happiness Composition by Bible Importance",
                           category_orders={"how_important_is_the_bible_in_your_life": ["Not at all important", "Somewhat important", "Extremely important"]})
        st.plotly_chart(fig_stack, use_container_width=True)
    
    # VISUAL 13 (Bonus): Ridgeline / Histogram
    st.subheader("12. Age Distribution by Happiness")
    fig_hist = px.histogram(df_filtered, x="decade_in_which_respondent_was_born", color="generally_how_happy_are_you_with_your_life_these_days_are_you", 
                            barmode="overlay", title="Who are the happy ones?")
    st.plotly_chart(fig_hist, use_container_width=True)

st.markdown("---")
st.caption("Dashboard Prototype generated for YouVersion Application | Data Source: Weighted Survey Core")