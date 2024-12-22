import streamlit as st
import os
import sys
import io
import contextlib
import tempfile
from pathlib import Path

class StreamlitIDE:
    def __init__(self):
        st.set_page_config(layout="wide", page_title="Streamlit IDE")
        self.setup_session_state()
        
    def setup_session_state(self):
        """Initialize session state variables"""
        if 'current_file' not in st.session_state:
            st.session_state.current_file = None
        if 'files' not in st.session_state:
            st.session_state.files = {}
        if 'output' not in st.session_state:
            st.session_state.output = ""
            
    def create_new_file(self):
        """Create a new file"""
        filename = st.sidebar.text_input("Enter file name:", key="new_file")
        if st.sidebar.button("Create File"):
            if filename and filename not in st.session_state.files:
                st.session_state.files[filename] = "# Write your code here"
                st.session_state.current_file = filename
                st.success(f"Created new file: {filename}")
            else:
                st.error("Please enter a unique file name")
                
    def file_explorer(self):
        """Display file explorer in sidebar"""
        st.sidebar.title("File Explorer")
        self.create_new_file()
        
        st.sidebar.markdown("---")
        st.sidebar.subheader("Open Files")
        
        for filename in st.session_state.files.keys():
            col1, col2 = st.sidebar.columns([3, 1])
            with col1:
                if st.button(filename, key=f"open_{filename}"):
                    st.session_state.current_file = filename
            with col2:
                if st.button("🗑️", key=f"delete_{filename}"):
                    del st.session_state.files[filename]
                    if st.session_state.current_file == filename:
                        st.session_state.current_file = None
                    st.rerun()
                    
    def code_editor(self):
        """Display code editor"""
        if st.session_state.current_file:
            st.subheader(f"Editing: {st.session_state.current_file}")
            
            # Code editor
            code = st.text_area(
                "Code Editor",
                value=st.session_state.files[st.session_state.current_file],
                height=400,
                key="code_editor"
            )
            st.session_state.files[st.session_state.current_file] = code
            
            # Buttons for save and run
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Save"):
                    st.success("File saved!")
            with col2:
                if st.button("Run"):
                    self.run_code(code)
        else:
            st.info("Create or select a file to start coding")
            
    def run_code(self, code):
        """Execute the code and capture output"""
        # Create a temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(code)
            temp_filename = f.name
        
        # Capture output
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            try:
                # Execute the code
                with open(temp_filename, 'r') as f:
                    exec(f.read())
                st.session_state.output = output.getvalue()
                st.success("Code executed successfully!")
            except Exception as e:
                st.session_state.output = f"Error: {str(e)}"
                st.error("Code execution failed!")
        
        # Clean up temporary file
        os.unlink(temp_filename)
        
    def output_terminal(self):
        """Display output terminal"""
        st.subheader("Output")
        st.text_area("Terminal", value=st.session_state.output, height=200, key="output_terminal")
        
        if st.button("Clear Output"):
            st.session_state.output = ""
            st.rerun()
            
    def show_settings(self):
        """Display settings in sidebar"""
        st.sidebar.markdown("---")
        st.sidebar.subheader("Settings")
        
        # Theme selection
        theme = st.sidebar.selectbox(
            "Theme",
            ["Light", "Dark"],
            key="theme"
        )
        
        # Font size
        font_size = st.sidebar.slider(
            "Font Size",
            min_value=8,
            max_value=24,
            value=14,
            key="font_size"
        )
        
    def run(self):
        """Main application loop"""
        st.title("Streamlit IDE")
        
        # Create two columns for main layout
        col1, col2 = st.columns([2, 1])
        
        with col1:
            self.code_editor()
            
        with col2:
            self.output_terminal()
            
        # Sidebar components
        self.file_explorer()
        self.show_settings()

if __name__ == "__main__":
    ide = StreamlitIDE()
    ide.run()