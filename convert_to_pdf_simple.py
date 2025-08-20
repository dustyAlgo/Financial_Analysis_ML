#!/usr/bin/env python3
"""
Convert PROJECT_DOCUMENTATION.md to PDF (Simple Version)
=======================================================

This script converts the markdown documentation to PDF using simpler libraries.
"""

import markdown
import os
from pathlib import Path
import subprocess
import sys

def convert_md_to_html(md_file, html_file):
    """Convert markdown to HTML with styling"""
    
    # Read markdown content
    with open(md_file, 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    # Convert markdown to HTML
    html_content = markdown.markdown(md_content, extensions=['tables', 'fenced_code', 'codehilite'])
    
    # Create complete HTML document with styling
    html_document = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Financial Analysis ML Project Documentation</title>
        <style>
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                line-height: 1.6;
                color: #333;
                max-width: 100%;
                margin: 0;
                padding: 20px;
                background-color: white;
            }}
            
            h1 {{
                color: #2c3e50;
                border-bottom: 3px solid #3498db;
                padding-bottom: 10px;
                font-size: 2.2em;
                margin-top: 0;
            }}
            
            h2 {{
                color: #34495e;
                border-bottom: 2px solid #ecf0f1;
                padding-bottom: 5px;
                font-size: 1.8em;
                margin-top: 30px;
            }}
            
            h3 {{
                color: #2c3e50;
                font-size: 1.4em;
                margin-top: 25px;
            }}
            
            h4 {{
                color: #34495e;
                font-size: 1.2em;
                margin-top: 20px;
            }}
            
            code {{
                background-color: #f8f9fa;
                padding: 2px 4px;
                border-radius: 3px;
                font-family: 'Courier New', monospace;
                font-size: 0.9em;
            }}
            
            pre {{
                background-color: #f8f9fa;
                border: 1px solid #e9ecef;
                border-radius: 5px;
                padding: 15px;
                overflow-x: auto;
                margin: 15px 0;
            }}
            
            pre code {{
                background-color: transparent;
                padding: 0;
            }}
            
            blockquote {{
                border-left: 4px solid #3498db;
                margin: 15px 0;
                padding-left: 15px;
                color: #555;
                font-style: italic;
            }}
            
            table {{
                border-collapse: collapse;
                width: 100%;
                margin: 15px 0;
            }}
            
            th, td {{
                border: 1px solid #ddd;
                padding: 8px 12px;
                text-align: left;
            }}
            
            th {{
                background-color: #f8f9fa;
                font-weight: bold;
            }}
            
            tr:nth-child(even) {{
                background-color: #f9f9f9;
            }}
            
            ul, ol {{
                margin: 15px 0;
                padding-left: 30px;
            }}
            
            li {{
                margin: 5px 0;
            }}
            
            .footer {{
                margin-top: 40px;
                padding-top: 20px;
                border-top: 1px solid #eee;
                text-align: center;
                color: #666;
                font-size: 0.9em;
            }}
            
            @media print {{
                body {{
                    font-size: 12pt;
                }}
                
                h1 {{
                    font-size: 18pt;
                }}
                
                h2 {{
                    font-size: 16pt;
                }}
                
                h3 {{
                    font-size: 14pt;
                }}
            }}
        </style>
    </head>
    <body>
        {html_content}
        
        <div class="footer">
            <p><strong>Financial Analysis ML Project Documentation</strong></p>
            <p>Version 1.0 | Last Updated: December 2024</p>
            <p>Generated from PROJECT_DOCUMENTATION.md</p>
        </div>
    </body>
    </html>
    """
    
    # Write HTML file
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(html_document)
    
    print(f"✅ HTML file created: {html_file}")
    return True

def convert_html_to_pdf(html_file, pdf_file):
    """Convert HTML to PDF using system tools"""
    
    # Try different methods to convert HTML to PDF
    
    # Method 1: Try wkhtmltopdf if available
    try:
        result = subprocess.run(['wkhtmltopdf', '--version'], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            print("📄 Using wkhtmltopdf to convert to PDF...")
            subprocess.run(['wkhtmltopdf', '--page-size', 'A4', '--margin-top', '1in', 
                          '--margin-bottom', '1in', '--margin-left', '1in', '--margin-right', '1in',
                          html_file, pdf_file], check=True)
            return True
    except (subprocess.TimeoutExpired, FileNotFoundError, subprocess.CalledProcessError):
        pass
    
    # Method 2: Try pandoc if available
    try:
        result = subprocess.run(['pandoc', '--version'], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            print("📄 Using pandoc to convert to PDF...")
            subprocess.run(['pandoc', html_file, '-o', pdf_file, '--pdf-engine=wkhtmltopdf'], check=True)
            return True
    except (subprocess.TimeoutExpired, FileNotFoundError, subprocess.CalledProcessError):
        pass
    
    # Method 3: Try Chrome/Chromium headless
    try:
        chrome_paths = [
            'chrome',
            'google-chrome',
            'chromium',
            'chromium-browser',
            r'C:\Program Files\Google\Chrome\Application\chrome.exe',
            r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe'
        ]
        
        for chrome_path in chrome_paths:
            try:
                result = subprocess.run([chrome_path, '--version'], 
                                      capture_output=True, text=True, timeout=5)
                if result.returncode == 0:
                    print(f"📄 Using {chrome_path} to convert to PDF...")
                    subprocess.run([
                        chrome_path, '--headless', '--disable-gpu', 
                        '--print-to-pdf=' + pdf_file,
                        '--print-to-pdf-no-header',
                        'file://' + os.path.abspath(html_file)
                    ], check=True)
                    return True
            except (subprocess.TimeoutExpired, FileNotFoundError, subprocess.CalledProcessError):
                continue
    except Exception:
        pass
    
    return False

def main():
    """Main function to convert documentation to PDF"""
    md_file = "PROJECT_DOCUMENTATION.md"
    html_file = "PROJECT_DOCUMENTATION.html"
    pdf_file = "PROJECT_DOCUMENTATION.pdf"
    
    # Check if markdown file exists
    if not Path(md_file).exists():
        print(f"❌ Error: {md_file} not found!")
        return False
    
    print(f"📄 Converting {md_file} to PDF...")
    
    # Step 1: Convert markdown to HTML
    print("⏳ Step 1: Converting markdown to HTML...")
    if not convert_md_to_html(md_file, html_file):
        print("❌ Failed to create HTML file")
        return False
    
    # Step 2: Convert HTML to PDF
    print("⏳ Step 2: Converting HTML to PDF...")
    if convert_html_to_pdf(html_file, pdf_file):
        print(f"🎉 PDF created successfully: {pdf_file}")
        print(f"📁 Location: {Path(pdf_file).absolute()}")
        
        # Clean up HTML file
        try:
            os.remove(html_file)
            print("🧹 Cleaned up temporary HTML file")
        except:
            pass
        
        return True
    else:
        print("❌ Could not convert to PDF automatically")
        print("\n💡 Alternative options:")
        print("1. Open the HTML file in your browser and use Print to PDF")
        print(f"   HTML file: {Path(html_file).absolute()}")
        print("2. Install wkhtmltopdf: https://wkhtmltopdf.org/downloads.html")
        print("3. Install pandoc: https://pandoc.org/installing.html")
        print("4. Use online converters with the HTML file")
        
        return False

if __name__ == "__main__":
    main() 