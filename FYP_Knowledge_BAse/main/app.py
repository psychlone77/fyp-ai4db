import streamlit as st
import pandas as pd
import io

# Set page configuration
st.set_page_config(
    page_title="Workload Upload System",
    page_icon="📊",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .section-header {
        font-size: 1.5rem;
        color: #2c3e50;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
        border-bottom: 2px solid #1f77b4;
        padding-bottom: 0.5rem;
    }
    .info-box {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    </style>
""", unsafe_allow_html=True)

# Main header
st.markdown('<h1 class="main-header">📊 OLAP & OLTP Workload Upload System</h1>', unsafe_allow_html=True)

# System Resources Section
st.markdown('<div class="section-header">💻 System Resources Configuration</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    ram_gb = st.number_input(
        "RAM (GB)",
        min_value=1,
        max_value=1024,
        value=16,
        step=1,
        help="Enter the available RAM in gigabytes"
    )

with col2:
    cpu_cores = st.number_input(
        "Number of CPU Cores",
        min_value=1,
        max_value=256,
        value=8,
        step=1,
        help="Enter the number of CPU cores available"
    )

# Display selected resources
#st.markdown('<div class="info-box">', unsafe_allow_html=True)
st.write(f"**Selected Configuration:** {ram_gb} GB RAM, {cpu_cores} CPU Cores")
st.markdown('</div>', unsafe_allow_html=True)

st.divider()

# OLAP Workload Section
st.markdown('<div class="section-header">📈 OLAP Workload Upload</div>', unsafe_allow_html=True)

st.info("**OLAP (Online Analytical Processing)**: Upload query plans, internal metrics, and workload files")

col1, col2, col3 = st.columns(3)

with col1:
    query_plan_file = st.file_uploader(
        "Upload Query Plan File",
        type=['txt'],
        key='query_plan_uploader',
        help="Upload query execution plans in text format"
    )
    
    if query_plan_file is not None:
        st.success(f"✅ Query plan file uploaded: {query_plan_file.name}")
        
        # Show file details
        col_a, col_b = st.columns(2)
        col_a.metric("Size", f"{query_plan_file.size / 1024:.2f} KB")
        col_b.metric("Type", "TXT")
        
        # Preview option
        if st.checkbox("Preview Query Plans", key='preview_query_plans'):
            try:
                content = query_plan_file.read().decode('utf-8')
                st.text_area("Query Plans Preview", content[:2000], height=300)
                if len(content) > 2000:
                    st.caption("Showing first 2000 characters")
            except Exception as e:
                st.error(f"Error reading file: {str(e)}")

with col2:
    internal_metrics_file = st.file_uploader(
        "Upload Internal Metrics File",
        type=['json'],
        key='internal_metrics_uploader',
        help="Upload internal metrics data in JSON format"
    )
    
    if internal_metrics_file is not None:
        st.success(f"✅ Internal metrics file uploaded: {internal_metrics_file.name}")
        
        # Show file details
        col_a, col_b = st.columns(2)
        col_a.metric("Size", f"{internal_metrics_file.size / 1024:.2f} KB")
        col_b.metric("Type", "JSON")
        
        # Preview option
        if st.checkbox("Preview Internal Metrics", key='preview_internal_metrics'):
            try:
                import json
                content = internal_metrics_file.read().decode('utf-8')
                metrics_data = json.loads(content)
                st.json(metrics_data)
            except Exception as e:
                st.error(f"Error reading file: {str(e)}")

with col3:
    olap_workload_file = st.file_uploader(
        "Upload OLAP Workload File",
        type=['sql'],
        key='olap_workload_uploader',
        help="Upload OLAP workload SQL file"
    )
    
    if olap_workload_file is not None:
        st.success(f"✅ OLAP workload file uploaded: {olap_workload_file.name}")
        
        # Show file details
        col_a, col_b = st.columns(2)
        col_a.metric("Size", f"{olap_workload_file.size / 1024:.2f} KB")
        col_b.metric("Type", "SQL")
        
        # Preview option
        if st.checkbox("Preview OLAP Workload", key='preview_olap_workload'):
            try:
                content = olap_workload_file.read().decode('utf-8')
                st.text_area("SQL Workload Preview", content[:1000], height=200)
                if len(content) > 1000:
                    st.caption("Showing first 1000 characters")
            except Exception as e:
                st.error(f"Error reading file: {str(e)}")

st.divider()

# OLTP Workload Section
st.markdown('<div class="section-header">⚡ OLTP Workload Upload</div>', unsafe_allow_html=True)

st.info("**OLTP (Online Transaction Processing)**: Suitable formats include CSV, Excel, JSON, SQL dump")

oltp_file = st.file_uploader(
    "Upload OLTP Workload File",
    type=['csv', 'xlsx', 'xls', 'json', 'sql', 'txt'],
    key='oltp_uploader',
    help="Upload transactional workload data (INSERT, UPDATE, DELETE operations)"
)

if oltp_file is not None:
    st.success(f"✅ OLTP file uploaded: {oltp_file.name}")
    
    # Show file details
    file_details = {
        "Filename": oltp_file.name,
        "File Size": f"{oltp_file.size / 1024:.2f} KB",
        "File Type": oltp_file.type
    }
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Filename", file_details["Filename"])
    col2.metric("Size", file_details["File Size"])
    col3.metric("Type", oltp_file.name.split('.')[-1].upper())
    
    # Preview option
    if st.checkbox("Preview OLTP Data", key='preview_oltp'):
        try:
            if oltp_file.name.endswith('.csv'):
                df = pd.read_csv(oltp_file)
                st.dataframe(df.head(10), use_container_width=True)
                st.caption(f"Showing first 10 rows of {len(df)} total rows")
            elif oltp_file.name.endswith(('.xlsx', '.xls')):
                df = pd.read_excel(oltp_file)
                st.dataframe(df.head(10), use_container_width=True)
                st.caption(f"Showing first 10 rows of {len(df)} total rows")
            elif oltp_file.name.endswith('.json'):
                df = pd.read_json(oltp_file)
                st.dataframe(df.head(10), use_container_width=True)
                st.caption(f"Showing first 10 rows of {len(df)} total rows")
            elif oltp_file.name.endswith(('.sql', '.txt')):
                content = oltp_file.read().decode('utf-8')
                st.text_area("File Content Preview", content[:1000], height=200)
                if len(content) > 1000:
                    st.caption("Showing first 1000 characters")
        except Exception as e:
            st.error(f"Error reading file: {str(e)}")

st.divider()

# Process Button
st.markdown('<div class="section-header">🚀 Process Workloads</div>', unsafe_allow_html=True)

if st.button("Process Workloads", type="primary", use_container_width=True):
    if (query_plan_file is None or internal_metrics_file is None or olap_workload_file is None) and oltp_file is None:
        st.warning("⚠️ Please upload OLAP files (query plans, internal metrics, and workload) or OLTP workload file before processing.")
    else:
        with st.spinner("Processing workloads..."):
            # Summary of what will be processed
            st.success("✅ Workload processing initiated!")
            
            summary_data = {
                "Configuration": ["RAM", "CPU Cores", "Query Plan File", "Internal Metrics File", "OLAP Workload File", "OLTP File"],
                "Value": [
                    f"{ram_gb} GB",
                    str(cpu_cores),
                    query_plan_file.name if query_plan_file else "Not uploaded",
                    internal_metrics_file.name if internal_metrics_file else "Not uploaded",
                    olap_workload_file.name if olap_workload_file else "Not uploaded",
                    oltp_file.name if oltp_file else "Not uploaded"
                ]
            }
            
            summary_df = pd.DataFrame(summary_data)
            st.table(summary_df)
            
            # Placeholder for actual processing logic
            st.info("💡 **Next Steps**: The workload files can now be processed based on the system resources configuration.")

# Sidebar with information
with st.sidebar:
    st.header("ℹ️ Information")
    
    st.subheader("OLAP vs OLTP")
    st.write("""
    **OLAP (Analytical)**:
    - Complex queries
    - Read-heavy operations
    - Data aggregation
    - Historical analysis
    
    **OLTP (Transactional)**:
    - Simple queries
    - Write-heavy operations
    - Real-time processing
    - Current data
    """)
    
    st.subheader("Supported Formats")
    st.write("""
    **OLAP**: 
    - Query Plan File (TXT)
    - Internal Metrics File (JSON)
    - OLAP Workload File (SQL)
    
    **OLTP**: CSV, Excel, JSON, SQL, TXT
    """)
    
    st.divider()
    st.caption("Built with Streamlit")