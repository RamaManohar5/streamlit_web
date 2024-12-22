import streamlit as st
import sys
import io
import contextlib
import subprocess
import ast
import black
import autopep8
from pathlib import Path
import tempfile

class PythonIDE:
    def __init__(self):
        st.set_page_config(layout="wide", page_title="Python IDE")
        self.setup_session_state()
        
    def setup_session_state(self):
        if 'current_file' not in st.session_state:
            st.session_state.current_file = None
        if 'files' not in st.session_state:
            st.session_state.files = {}
        if 'output' not in st.session_state:
            st.session_state.output = ""
        if 'python_version' not in st.session_state:
            st.session_state.python_version = sys.version
            
    def code_editor(self):
        """Python code editor with syntax checking"""
        if st.session_state.current_file:
            st.subheader(f"Editing: {st.session_state.current_file}")
            
            # Code editor
            code = st.text_area(
                "Python Code Editor",
                value=st.session_state.files[st.session_state.current_file],
                height=400,
                key="code_editor"
            )
            st.session_state.files[st.session_state.current_file] = code
            
            # Editor tools
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                if st.button("Run Code"):
                    self.run_python_code(code)
            with col2:
                if st.button("Format Code"):
                    self.format_code(code)
            with col3:
                if st.button("Check Syntax"):
                    self.check_syntax(code)
            with col4:
                if st.button("Clear Output"):
                    st.session_state.output = ""
                    st.rerun()
                    
    def run_python_code(self, code):
        """Execute Python code and capture output"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(code)
            temp_filename = f.name
            
        try:
            # Run code in a separate process
            result = subprocess.run(
                [sys.executable, temp_filename],
                capture_output=True,
                text=True
            )
            
            if result.stdout:
                st.session_state.output = result.stdout
                st.success("Code executed successfully!")
            if result.stderr:
                st.session_state.output = result.stderr
                st.error("Execution error!")
                
        except Exception as e:
            st.session_state.output = f"Error: {str(e)}"
            st.error("Code execution failed!")
            
        Path(temp_filename).unlink()
        
    def format_code(self, code):
        """Format Python code using black and autopep8"""
        try:
            # First apply autopep8
            formatted_code = autopep8.fix_code(code)
            # Then apply black
            formatted_code = black.format_str(formatted_code, mode=black.FileMode())
            st.session_state.files[st.session_state.current_file] = formatted_code
            st.success("Code formatted successfully!")
            st.rerun()
        except Exception as e:
            st.error(f"Formatting error: {str(e)}")
            
    def check_syntax(self, code):
        """Check Python syntax"""
        try:
            ast.parse(code)
            st.success("Syntax is correct!")
        except SyntaxError as e:
            st.error(f"Syntax error: {str(e)}")
            
    def file_manager(self):
        """Python file management"""
        st.sidebar.title("Python Files")
        
        # Create new Python file
        new_file = st.sidebar.text_input("New Python file:")
        if st.sidebar.button("Create"):
            if new_file and not new_file.endswith('.py'):
                new_file += '.py'
            if new_file and new_file not in st.session_state.files:
                st.session_state.files[new_file] = "# Python code here"
                st.session_state.current_file = new_file
                st.success(f"Created: {new_file}")
            else:
                st.error("Please enter a unique file name")
                
        # File explorer
        st.sidebar.markdown("---")
        st.sidebar.subheader("Files")
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
                    
    def python_tools(self):
        """Python development tools"""
        st.sidebar.markdown("---")
        st.sidebar.subheader("Python Tools")
        
        # Python version info
        st.sidebar.info(f"Python {sys.version_info.major}.{sys.version_info.minor}")
        
        # PEP 8 checking
        if st.sidebar.button("Check PEP 8"):
            if st.session_state.current_file:
                code = st.session_state.files[st.session_state.current_file]
                try:
                    # Use autopep8 to check PEP 8
                    issues = autopep8.fix_code(code, options={'verbose': True})
                    if issues != code:
                        st.warning("PEP 8 issues found. Click 'Format Code' to fix.")
                    else:
                        st.success("Code follows PEP 8!")
                except Exception as e:
                    st.error(f"PEP 8 check failed: {str(e)}")
                    
    def output_console(self):
        """Python output console"""
        st.subheader("Console Output")
        st.text_area(
            "Output",
            value=st.session_state.output,
            height=200,
            key="output_console"
        )
        
    def run(self):
        """Main IDE interface"""
        st.title("Python Development IDE")
        
        # Main layout
        col1, col2 = st.columns([2, 1])
        
        with col1:
            self.code_editor()
            
        with col2:
            self.output_console()
            
        # Sidebar components
        self.file_manager()
        self.python_tools()

if __name__ == "__main__":
    ide = PythonIDE()
    ide.run()