from scholarly import scholarly
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from fpdf import FPDF
import time
from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai

# Step 1: Fetch Author Data
def fetch_author_data(author_name):
    """Fetches Google Scholar data for the author by name."""
    search_query = scholarly.search_author(author_name)
    try:
        author = next(search_query)
        author = scholarly.fill(author)
        return author
    except StopIteration:
        print(f"No author found for the name: {author_name}")
        return None

# Step 2: Extract Publications Data
def extract_publications_data(author, max_publications=10):
    """Extracts publication data from the author's profile, limiting results to a certain number."""
    publication_list = []
    
    # Process up to max_publications for performance improvement
    for i, pub in enumerate(author['publications']):
        if i >= max_publications:
            break
        try:
            scholarly.fill(pub)  # Retrieve detailed publication info
            publication_list.append({
                "title": pub['bib'].get('title', 'N/A'),
                "authors": pub['bib'].get('author', 'N/A'),
                "year": pub['bib'].get('pub_year', 'N/A'),
                "venue": pub['bib'].get('venue', 'N/A'),
                "citation_count": pub.get('num_citations', 0),
                "url": pub.get('pub_url', 'N/A')
            })
        except Exception as e:
            print(f"Error processing publication: {e}")
    
    if len(publication_list) == 0:
        print("No publications found or data fetching failed.")
    
    return pd.DataFrame(publication_list)

# Step 3: Summarize Publication Data
def summarize_publications(df, sort_by="citation_count", start_year=None, end_year=None):
    """Summarizes the publication data based on user preferences."""
    if start_year:
        df = df[df['year'] >= start_year]
    if end_year:
        df = df[df['year'] <= end_year]
    
    summary = {
        'Total Publications': df.shape[0],
        'Total Citations': df['citation_count'].sum(),
        'Average Citations per Publication': round(df['citation_count'].mean(), 2) if df.shape[0] > 0 else 0
    }

    if not df.empty:
        summary['Most Cited Publication'] = df.loc[df['citation_count'].idxmax()]['title']
    
    df = df.sort_values(by=sort_by, ascending=False)  # Sort by user preference
    return summary, df

# Step 4: Generate Visual Report
def generate_visual_report(df):
    """Creates visual charts for publication and citation trends."""
    if df.empty:
        print("No data available for visualization.")
        return
    
    plt.figure(figsize=(10, 6))
    
    # Plot 1: Publication Count by Year
    plt.subplot(1, 2, 1)
    sns.countplot(data=df, x='year')
    plt.title("Publications by Year")
    
    # Plot 2: Citation Trends by Year
    plt.subplot(1, 2, 2)
    df_grouped = df.groupby('year')['citation_count'].sum().reset_index()
    sns.lineplot(data=df_grouped, x='year', y='citation_count')
    plt.title("Citation Count Trends by Year")

    plt.tight_layout()
    plt.show()

# Step 5: Export Report to PDF
def export_report_to_pdf(summary, df, author_name):
    """Exports a summarized report of the author's publications to a PDF."""
    if df.empty:
        print("No data to export.")
        return
    
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    # Title and summary
    pdf.cell(200, 10, txt=f"Publication Report for {author_name}", ln=True, align='C')
    pdf.ln(10)
    
    for key, value in summary.items():
        pdf.cell(200, 10, txt=f"{key}: {value}", ln=True)
    
    pdf.ln(10)
    pdf.cell(200, 10, txt="Top 5 Publications:", ln=True)
    
    # Publication List
    for i, row in df.head(5).iterrows():
        pdf.cell(200, 10, txt=f"{i + 1}. {row['title']} ({row['year']})", ln=True)
    
    pdf.output(f"{author_name}_publication_report.pdf")
    print(f"PDF report saved as {author_name}_publication_report.pdf")

# Step 6: Generate Summary with Google Generative AI
def generate_summary(data):
    summary_prompt = f"Write a concise 200-word summary about {data['name']}, a professor at {data['affiliation']}. Include key details like research interests, citations, H-index, co-authors, and notable publications."
    response = chat.send_message(summary_prompt)
    summary = "".join([chunk.text for chunk in response])
    return summary

# Step 7: Main Function to Run the Process
def main(author_name, sort_by="citation_count", start_year=None, end_year=None, max_publications=10):
    # Fetch and Extract Data
    start_time = time.time()
    
    author = fetch_author_data(author_name)
    if not author:
        return
    
    df_publications = extract_publications_data(author, max_publications)
    
    # Summarize the Data
    summary, df_sorted = summarize_publications(df_publications, sort_by, start_year, end_year)

    # Display Summary
    print("Summary Report:", summary)

    # Generate Visual Report
    generate_visual_report(df_sorted)

    # Export Report to PDF
    export_report_to_pdf(summary, df_sorted, author_name)

    end_time = time.time()
    print(f"Process completed in {round(end_time - start_time, 2)} seconds.")

# Streamlit app starts here
if __name__ == "__main__":
    load_dotenv()  # Load all the environment variables
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))  # Load Google Generative AI API key

    st.title("🤖 Research Snap")

    # Input for author name
    user_question = st.text_input("Enter the name of the person to make profile Summary:", 
                                  "Gunasekaran Raja")
    
    if st.button("🚀 Generate Summary"):
        main(user_question, sort_by="citation_count", start_year=2023, end_year=2024, max_publications=10)
