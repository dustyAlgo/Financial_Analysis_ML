#!/usr/bin/env python3
"""
Convert PROJECT_DOCUMENTATION.md to PDF
=======================================

This script converts the markdown documentation to a professionally formatted PDF.
"""

import markdown
import weasyprint
from pathlib import Path
import sys

def convert_md_to_pdf(md_file, pdf_file):
    """Convert markdown file to PDF with custom styling"""
    
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
            @page {{
                margin: 1in;
                size: A4;
            }}
            
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                line-height: 1.6;
                color: #333;
                max-width: 100%;
                margin: 0;
                padding: 20px;
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
            
            .highlight {{
                background-color: #fff3cd;
                padding: 10px;
                border-radius: 5px;
                border-left: 4px solid #ffc107;
                margin: 15px 0;
            }}
            
            .info-box {{
                background-color: #d1ecf1;
                border: 1px solid #bee5eb;
                border-radius: 5px;
                padding: 15px;
                margin: 15px 0;
            }}
            
            .warning-box {{
                background-color: #fff3cd;
                border: 1px solid #ffeaa7;
                border-radius: 5px;
                padding: 15px;
                margin: 15px 0;
            }}
            
            .success-box {{
                background-color: #d4edda;
                border: 1px solid #c3e6cb;
                border-radius: 5px;
                padding: 15px;
                margin: 15px 0;
            }}
            
            .architecture-diagram {{
                text-align: center;
                margin: 20px 0;
                font-family: monospace;
                background-color: #f8f9fa;
                padding: 20px;
                border-radius: 5px;
            }}
            
            .project-structure {{
                background-color: #f8f9fa;
                border: 1px solid #e9ecef;
                border-radius: 5px;
                padding: 15px;
                font-family: monospace;
                white-space: pre-wrap;
                margin: 15px 0;
            }}
            
            .footer {{
                margin-top: 40px;
                padding-top: 20px;
                border-top: 1px solid #eee;
                text-align: center;
                color: #666;
                font-size: 0.9em;
            }}
            
            .page-break {{
                page-break-before: always;
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
    
    # Convert HTML to PDF
    try:
        weasyprint.HTML(string=html_document).write_pdf(pdf_file)
        print(f"✅ Successfully converted {md_file} to {pdf_file}")
        return True
    except Exception as e:
        print(f"❌ Error converting to PDF: {e}")
        return False

def main():
    """Main function to convert documentation to PDF"""
    md_file = "PROJECT_DOCUMENTATION.md"
    pdf_file = "PROJECT_DOCUMENTATION.pdf"
    
    # Check if markdown file exists
    if not Path(md_file).exists():
        print(f"❌ Error: {md_file} not found!")
        return False
    
    print(f"📄 Converting {md_file} to PDF...")
    print("⏳ This may take a few moments...")
    
    # Convert to PDF
    success = convert_md_to_pdf(md_file, pdf_file)
    
    if success:
        print(f"🎉 PDF created successfully: {pdf_file}")
        print(f"📁 Location: {Path(pdf_file).absolute()}")
    else:
        print("❌ Failed to create PDF")
        return False
    
    return True

if __name__ == "__main__":
    main() 