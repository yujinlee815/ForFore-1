import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# Page configuration
st.set_page_config(page_title="Job Search", page_icon="🧑‍💼", layout="wide")

# Sample job data (can be fetched from DB or API in production)
@st.cache_data
def load_job_data():
    jobs = [
        # ---------- SERVICE ----------
        {
            "id": 1,
            "title": "Cafe Barista",
            "company": "Starbucks Gangnam",
            "location": "Seoul, Gangnam-gu",
            "salary": "₩10,000 per hour",
            "type": "Part-time",
            "visa": ["F-2", "F-4", "F-5", "F-6"],
            "description": "Looking for a friendly barista with a passion for coffee. Experience in coffee making is a plus.",
            "requirements": "Intermediate Korean, available 5 days per week",
            "posted": datetime.now() - timedelta(days=2),
            "category": "Service"
        },
        {
            "id": 2,
            "title": "Restaurant Server",
            "company": "Bonjuk by TheBorn Korea",
            "location": "Seoul, Jongno-gu",
            "salary": "₩9,500 per hour",
            "type": "Part-time",
            "visa": ["D-2", "D-4", "F-2", "F-4", "F-5", "F-6", "H-2"],
            "description": "Serve food and assist customers in a Korean restaurant.",
            "requirements": "Basic Korean communication, friendly attitude",
            "posted": datetime.now() - timedelta(days=1),
            "category": "Service"
        },
        {
            "id": 3,
            "title": "Convenience Store Night Shift",
            "company": "CU Convenience Store",
            "location": "Seoul, Gwanak-gu",
            "salary": "₩11,000 per hour (including night bonus)",
            "type": "Part-time",
            "visa": ["D-2", "D-4", "F-2", "F-4", "F-5", "F-6", "H-2"],
            "description": "Night shift position (10 PM – 6 AM). Cashier and stocking duties.",
            "requirements": "Basic Korean, responsible personality",
            "posted": datetime.now() - timedelta(hours=12),
            "category": "Service"
        },
        {
            "id": 4,
            "title": "Hotel Waiter / Waitress",
            "company": "Shilla Hotel",
            "location": "Seoul, Jung-gu",
            "salary": "₩10,500 per hour",
            "type": "Part-time",
            "visa": ["F-2", "F-4", "F-5", "F-6", "H-2"],
            "description": "Serve guests at hotel restaurants and banquets.",
            "requirements": "Intermediate Korean and English communication skills",
            "posted": datetime.now() - timedelta(days=3),
            "category": "Service"
        },

        # ---------- LOGISTICS / DELIVERY ----------
        {
            "id": 5,
            "title": "Warehouse Packaging Staff",
            "company": "Coupang Logistics Center",
            "location": "Bucheon, Gyeonggi-do",
            "salary": "₩12,000 per hour",
            "type": "Short-term",
            "visa": ["E-9", "H-2", "F-2", "F-4", "F-5"],
            "description": "Work includes packing and preparing goods for shipment in a warehouse environment.",
            "requirements": "Physically fit, basic Korean understanding",
            "posted": datetime.now() - timedelta(days=1),
            "category": "Logistics/Delivery"
        },
        {
            "id": 6,
            "title": "Delivery Rider",
            "company": "Baemin Delivery",
            "location": "Incheon, Namdong-gu",
            "salary": "₩15,000 per delivery hour (average)",
            "type": "Part-time",
            "visa": ["H-2", "F-4", "F-5", "F-6"],
            "description": "Deliver food orders around local neighborhoods using a motorbike.",
            "requirements": "Motorcycle license, smartphone with GPS",
            "posted": datetime.now() - timedelta(days=1),
            "category": "Logistics/Delivery"
        },
        {
            "id": 7,
            "title": "Warehouse Loader",
            "company": "CJ Logistics",
            "location": "Gimpo, Gyeonggi-do",
            "salary": "₩11,500 per hour",
            "type": "Full-time",
            "visa": ["E-9", "H-2", "F-4", "F-5"],
            "description": "Loading and unloading parcels and organizing warehouse space.",
            "requirements": "Physically strong and able to lift packages up to 20kg",
            "posted": datetime.now() - timedelta(days=2),
            "category": "Logistics/Delivery"
        },

        # ---------- IT / DEVELOPMENT ----------
        {
            "id": 8,
            "title": "Backend Developer (Python/Django)",
            "company": "Tech Startup Korea",
            "location": "Seoul, Gangnam-gu",
            "salary": "₩40M–₩60M per year",
            "type": "Full-time",
            "visa": ["E-7", "F-2", "F-5"],
            "description": "We are looking for an experienced backend engineer to build scalable systems.",
            "requirements": "3+ years of Python experience, AWS experience preferred",
            "posted": datetime.now() - timedelta(days=7),
            "category": "IT/Development"
        },
        {
            "id": 9,
            "title": "Frontend Developer (React)",
            "company": "NextGen Web Labs",
            "location": "Seoul, Mapo-gu",
            "salary": "₩45M–₩65M per year",
            "type": "Full-time",
            "visa": ["E-7", "F-2", "F-5"],
            "description": "Develop responsive web interfaces using React and TypeScript.",
            "requirements": "2+ years frontend experience, portfolio preferred",
            "posted": datetime.now() - timedelta(days=5),
            "category": "IT/Development"
        },
        {
            "id": 10,
            "title": "Data Analyst Intern",
            "company": "K-Digital Analytics",
            "location": "Seoul, Seocho-gu",
            "salary": "₩2,000,000 per month",
            "type": "Internship",
            "visa": ["D-2", "D-10", "F-2", "F-5", "F-6"],
            "description": "Assist data team with SQL queries, dashboards, and basic data visualization.",
            "requirements": "Knowledge of Python, Excel, and data analytics tools",
            "posted": datetime.now() - timedelta(days=3),
            "category": "IT/Development"
        },

        # ---------- EDUCATION ----------
        {
            "id": 11,
            "title": "English Instructor",
            "company": "ABC Language Academy",
            "location": "Seoul, Songpa-gu",
            "salary": "₩2,500,000 per month",
            "type": "Full-time",
            "visa": ["E-2", "F-2", "F-5", "F-6"],
            "description": "Teach conversational English to elementary school students in small classes.",
            "requirements": "Native-level English, teaching experience preferred",
            "posted": datetime.now() - timedelta(days=5),
            "category": "Education"
        },
        {
            "id": 12,
            "title": "Math Tutor",
            "company": "Bright Minds Academy",
            "location": "Seoul, Seongdong-gu",
            "salary": "₩25,000 per hour",
            "type": "Part-time",
            "visa": ["F-2", "F-5", "F-6"],
            "description": "Private tutoring for middle school math students. Materials provided.",
            "requirements": "Fluent Korean or English, tutoring experience a plus",
            "posted": datetime.now() - timedelta(days=2),
            "category": "Education"
        },

        # ---------- MANUFACTURING ----------
        {
            "id": 13,
            "title": "Factory Line Worker",
            "company": "Samsung Electronics Partner",
            "location": "Suwon, Gyeonggi-do",
            "salary": "₩2,200,000 per month",
            "type": "Full-time",
            "visa": ["E-9", "H-2", "F-4", "F-5"],
            "description": "Assemble electronic devices on production lines. Dormitory provided.",
            "requirements": "Hardworking, night shift availability preferred",
            "posted": datetime.now() - timedelta(days=4),
            "category": "Manufacturing"
        },
        {
            "id": 14,
            "title": "Machine Operator",
            "company": "Hyundai Precision Parts",
            "location": "Ulsan, Nam-gu",
            "salary": "₩2,500,000 per month",
            "type": "Full-time",
            "visa": ["E-9", "H-2", "F-4", "F-5"],
            "description": "Operate metal-cutting and assembly machines in an auto parts plant.",
            "requirements": "Basic Korean, manufacturing experience preferred",
            "posted": datetime.now() - timedelta(days=3),
            "category": "Manufacturing"
        },

        # ---------- MARKETING / PR ----------
        {
            "id": 15,
            "title": "Marketing Intern",
            "company": "Global Marketing Co.",
            "location": "Seoul, Yeongdeungpo-gu",
            "salary": "₩1,800,000 per month",
            "type": "Internship",
            "visa": ["D-2", "D-10", "F-2", "F-5", "F-6"],
            "description": "Assist in social media marketing, content creation, and campaign analysis.",
            "requirements": "Advanced Korean, interest in digital marketing",
            "posted": datetime.now() - timedelta(days=2),
            "category": "Marketing/PR"
        },
        {
            "id": 16,
            "title": "Social Media Manager",
            "company": "Seoul Trend Agency",
            "location": "Seoul, Gangnam-gu",
            "salary": "₩3,000,000 per month",
            "type": "Full-time",
            "visa": ["E-7", "F-2", "F-5", "F-6"],
            "description": "Manage Instagram, TikTok, and YouTube accounts for brand clients.",
            "requirements": "Experience in influencer marketing, fluent English",
            "posted": datetime.now() - timedelta(days=4),
            "category": "Marketing/PR"
        },

        # ---------- TRANSLATION / INTERPRETATION ----------
        {
            "id": 17,
            "title": "Chinese Translator",
            "company": "Global Translation Agency",
            "location": "Seoul, Mapo-gu",
            "salary": "Negotiable per project",
            "type": "Freelance",
            "visa": ["F-2", "F-4", "F-5", "F-6"],
            "description": "Translation between Chinese and Korean. Remote work available.",
            "requirements": "Native Chinese proficiency, 2+ years translation experience",
            "posted": datetime.now() - timedelta(days=3),
            "category": "Translation/Interpretation"
        },
        {
            "id": 18,
            "title": "Japanese Interpreter",
            "company": "Korea Trade Center",
            "location": "Busan, Haeundae-gu",
            "salary": "₩250,000 per day",
            "type": "Freelance",
            "visa": ["F-2", "F-4", "F-5", "F-6"],
            "description": "Interpret for business meetings between Korean and Japanese clients.",
            "requirements": "Fluent in Japanese and Korean, experience in trade preferred",
            "posted": datetime.now() - timedelta(days=2),
            "category": "Translation/Interpretation"
        },
    ]
    return pd.DataFrame(jobs)


# Load data
df = load_job_data()

# Title
st.title("🧑‍💼 Job Search")
st.write("Find job opportunities in Korea tailored for foreign residents.")

# Sidebar filters
with st.sidebar:
    st.header("🔍 Filters")
    
    # Search
    search_query = st.text_input("🔎 Search", placeholder="Search by job title, company...")
    
    # Location filter
    locations = ["All"] + sorted(df["location"].unique().tolist())
    selected_location = st.selectbox("📍 Location", locations)
    
    # Category filter
    categories = ["All"] + sorted(df["category"].unique().tolist())
    selected_category = st.selectbox("💼 Category", categories)
    
    # Employment type filter
    job_types = ["All"] + sorted(df["type"].unique().tolist())
    selected_type = st.selectbox("⏰ Employment Type", job_types)
    
    # Visa type filter
    all_visas = sorted(set([visa for visas in df["visa"] for visa in visas]))
    selected_visa = st.multiselect("🛂 Visa Type", all_visas, help="Select your visa type")
    
    st.markdown("---")
    st.caption("💡 Tip: Select multiple filters to find your perfect job match!")

# Apply filters
filtered_df = df.copy()

# Search filter
if search_query:
    filtered_df = filtered_df[
        filtered_df["title"].str.contains(search_query, case=False, na=False) |
        filtered_df["company"].str.contains(search_query, case=False, na=False) |
        filtered_df["description"].str.contains(search_query, case=False, na=False)
    ]

# Location filter
if selected_location != "All":
    filtered_df = filtered_df[filtered_df["location"] == selected_location]

# Category filter
if selected_category != "All":
    filtered_df = filtered_df[filtered_df["category"] == selected_category]

# Employment type filter
if selected_type != "All":
    filtered_df = filtered_df[filtered_df["type"] == selected_type]

# Visa type filter
if selected_visa:
    filtered_df = filtered_df[filtered_df["visa"].apply(lambda x: any(v in x for v in selected_visa))]

# Display results
st.markdown(f"### Total {len(filtered_df)} Job Listings")

if len(filtered_df) == 0:
    st.info("🔍 No jobs found matching your criteria. Try adjusting your filters!")
else:
    # Display job cards
    for idx, row in filtered_df.iterrows():
        with st.container():
            col1, col2 = st.columns([3, 1])
            
            with col1:
                # Title and company
                st.markdown(f"### 💼 {row['title']}")
                st.markdown(f"**🏢 {row['company']}**")
                
                # Basic information
                cols = st.columns(4)
                cols[0].markdown(f"📍 {row['location']}")
                cols[1].markdown(f"💰 {row['salary']}")
                cols[2].markdown(f"⏰ {row['type']}")
                cols[3].markdown(f"📂 {row['category']}")
                
                # Details
                with st.expander("📄 View Details"):
                    st.markdown(f"**Job Description:**")
                    st.write(row['description'])
                    st.markdown(f"**Requirements:**")
                    st.write(row['requirements'])
                    st.markdown(f"**Eligible Visa Types:**")
                    st.write(", ".join(row['visa']))
                    st.markdown(f"**Posted:** {row['posted'].strftime('%Y-%m-%d')}")
            
            with col2:
                # Action buttons
                if st.button("📋 Apply", key=f"apply_{row['id']}", use_container_width=True):
                    st.success("✅ Application submitted successfully!")
                    st.balloons()
                
                if st.button("❤️ Save", key=f"save_{row['id']}", use_container_width=True):
                    st.info("💾 Job saved to your favorites!")
            
            st.markdown("---")

# Bottom information
st.markdown("---")
st.info("""
📢 **Usage Guide**
- This page provides job listings specifically for foreign residents in Korea.
- Please verify that your visa type allows you to work in the listed position before applying.
- For any questions, feel free to ask the ForFore chatbot!
""")

# Footer
st.caption("© 2025 ForFore - Administrative & Life Assistant for Foreign Residents")

