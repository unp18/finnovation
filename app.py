import streamlit as st
import pandas as pd
import requests
import urllib.parse
import time
from io import StringIO

# Page configuration
st.set_page_config(
    page_title="Social Profile Finder",
    page_icon="🔍",
    layout="wide"
)

# Storing SerpAPI key here
SERPAPI_KEY = "5698f6ba6f17f7bbbaadc795d500668520f4185c8dfccb07d34bfd4779eb1523"  

# Initialize session state
if 'results_df' not in st.session_state:
    st.session_state.results_df = None
if 'search_complete' not in st.session_state:
    st.session_state.search_complete = False

def find_social_profiles(name, city=None, email=None):
    """Find social media profiles for a given person"""
    if not SERPAPI_KEY:
        return []
    
    query = name
    if city:
        query += f" {city}"
    if email:
        query += f" {email}"

    params = {
        "q": query,
        "location": "India",
        "hl": "en",
        "gl": "in",
        "api_key": SERPAPI_KEY,
        "engine": "google"
    }

    try:
        response = requests.get("https://serpapi.com/search", params=params, timeout=10)
        results = response.json()
        
        links = []
        for result in results.get("organic_results", []):
            link = result.get("link", "")
            if any(domain in link for domain in ["facebook.com", "linkedin.com", "instagram.com", "twitter.com"]):
                links.append(link)
        
        return links
    except Exception as e:
        st.error(f"Error searching for {name}: {str(e)}")
        return []

def process_single_search(name, city, email):
    """Process a single person search"""
    profiles = find_social_profiles(name, city, email)
    return {
        "Name": name,
        "City": city if city else "N/A",
        "Email": email if email else "N/A",
        "Profiles Found": profiles,
        "Profile Count": len(profiles)
    }

def process_bulk_search(df, progress_bar, status_text):
    """Process bulk search from uploaded CSV"""
    social_data = []
    total_rows = len(df)
    
    for index, row in df.iterrows():
        name = row['Name'] if 'Name' in row else row.iloc[0]
        city = row.get('City', None)
        email = row.get('Email', None)
        
        status_text.text(f"Searching for: {name} ({index + 1}/{total_rows})")
        
        profiles = find_social_profiles(name, city, email)
        
        social_data.append({
            "Name": name,
            "City": city if city else "N/A",
            "Email": email if email else "N/A",
            "Profiles Found": profiles,
            "Profile Count": len(profiles)
        })
        
        # Update progress
        progress_bar.progress((index + 1) / total_rows)
        
        # Add a small delay to avoid rate limiting
        time.sleep(0.5)
    
    return pd.DataFrame(social_data)

# Main app
def main():
    st.title("🔍 Social Profile Finder")
    
    # No sidebar API key input, key is stored in backend

    # Main content tabs
    tab1, tab2, tab3 = st.tabs(["Single Search", "Bulk Search", "Results"])
    
    with tab1:
        st.header("Search for Individual")
        
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Name *", placeholder="Enter full name")
            city = st.text_input("City (Optional)", placeholder="Enter city")
        
        with col2:
            email = st.text_input("Email (Optional)", placeholder="Enter email address")
            
        if st.button("Search Profiles", disabled=not name):
            if name:
                with st.spinner("Searching for social profiles..."):
                    result = process_single_search(name, city, email)
                    
                    st.success(f"Search completed for {name}")
                    
                    # Display results
                    col1, col2 = st.columns([1, 2])
                    
                    with col1:
                        st.metric("Profiles Found", result["Profile Count"])
                    
                    with col2:
                        if result["Profiles Found"]:
                            st.write("**Found Profiles:**")
                            for profile in result["Profiles Found"]:
                                st.write(f"• {profile}")
                        else:
                            st.info("No social profiles found")
    
    with tab2:
        st.header("Bulk Search from CSV")
        
        # File upload
        uploaded_file = st.file_uploader(
            "Upload CSV file", 
            type=['csv'],
            help="CSV should contain columns: Name (required), City (optional), Email (optional)"
        )
        
        if uploaded_file is not None:
            try:
                # Read the uploaded file
                df = pd.read_csv(uploaded_file)
                
                st.write("**Preview of uploaded data:**")
                st.dataframe(df.head())
                
                st.write(f"**Total records:** {len(df)}")
                
                # Validate required columns
                if 'Name' not in df.columns and len(df.columns) == 0:
                    st.error("CSV must contain at least a 'Name' column")
                else:
                    if st.button("Start Bulk Search"):
                        # Progress tracking
                        progress_bar = st.progress(0)
                        status_text = st.empty()
                        
                        # Process the search
                        results_df = process_bulk_search(df, progress_bar, status_text)
                        
                        # Store results in session state
                        st.session_state.results_df = results_df
                        st.session_state.search_complete = True
                        
                        status_text.text("Search completed!")
                        st.success(f"Processed {len(results_df)} records successfully!")
                        
                        # Show summary
                        total_profiles = results_df['Profile Count'].sum()
                        people_with_profiles = len(results_df[results_df['Profile Count'] > 0])
                        
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Total Records", len(results_df))
                        with col2:
                            st.metric("People with Profiles", people_with_profiles)
                        with col3:
                            st.metric("Total Profiles Found", total_profiles)
                    
            except Exception as e:
                st.error(f"Error reading CSV file: {str(e)}")
    
    with tab3:
        st.header("Search Results")
        
        if st.session_state.results_df is not None:
            results_df = st.session_state.results_df
            
            # Display results summary
            st.subheader("Summary")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Total Records", len(results_df))
            with col2:
                people_with_profiles = len(results_df[results_df['Profile Count'] > 0])
                st.metric("People with Profiles", people_with_profiles)
            with col3:
                total_profiles = results_df['Profile Count'].sum()
                st.metric("Total Profiles Found", total_profiles)
            
            # Filter options
            st.subheader("Filter Results")
            col1, col2 = st.columns(2)
            
            with col1:
                show_only_with_profiles = st.checkbox("Show only people with profiles found")
            
            with col2:
                min_profiles = st.slider("Minimum profiles found", 0, 10, 0)
            
            # Apply filters
            filtered_df = results_df.copy()
            if show_only_with_profiles:
                filtered_df = filtered_df[filtered_df['Profile Count'] > 0]
            if min_profiles > 0:
                filtered_df = filtered_df[filtered_df['Profile Count'] >= min_profiles]
            
            # Display filtered results
            st.subheader(f"Results ({len(filtered_df)} records)")
            
            # Create a display dataframe with clickable links
            display_df = filtered_df.copy()
            for idx, row in display_df.iterrows():
                if row['Profiles Found']:
                    # Convert list of URLs to clickable links
                    links_html = []
                    for url in row['Profiles Found']:
                        domain = url.split('/')[2].replace('www.', '')
                        links_html.append(f'<a href="{url}" target="_blank">{domain}</a>')
                    display_df.at[idx, 'Profiles Found'] = ' | '.join(links_html)
                else:
                    display_df.at[idx, 'Profiles Found'] = "No profiles found"
            
            # Display as HTML to render links
            st.write(display_df.to_html(escape=False, index=False), unsafe_allow_html=True)
            
            # Download button
            if len(filtered_df) > 0:
                csv = filtered_df.to_csv(index=False)
                st.download_button(
                    label="Download Results as CSV",
                    data=csv,
                    file_name="social_profiles_results.csv",
                    mime="text/csv"
                )
        else:
            st.info("No results to display. Please run a bulk search first.")
    
    # Footer
    st.markdown("---")

if __name__ == "__main__":
    main()
