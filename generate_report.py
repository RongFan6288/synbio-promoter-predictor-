# generate_report.py
import markdown
import os

def md_to_html(md_file, output_html=None):
    """
    将 Markdown 文件转换为 HTML 报告
    :param md_file: 输入的 .md 文件路径（如 'design_report.md'）
    :param output_html: 输出的 HTML 路径（如 'report.html'），默认同名替换后缀
    """
    if output_html is None:
        output_html = os.path.splitext(md_file)[0] + ".html"

    # 读取 Markdown 内容
    with open(md_file, "r", encoding="utf-8") as f:
        md_content = f.read()

    # 转换为 HTML（支持代码块、表格等）
    html_content = markdown.markdown(
        md_content,
        extensions=["fenced_code", "tables", "codehilite"]
    )

    # 添加基础样式（让报告更美观）
    styled_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>{os.path.basename(md_file)}</title>
        <style>
            body {{ 
                font-family: "Segoe UI", "Microsoft YaHei", sans-serif; 
                line-height: 1.6; 
                max-width: 900px; 
                margin: 40px auto; 
                padding: 0 20px; 
                color: #333;
            }}
            h1, h2 {{ border-bottom: 1px solid #eee; padding-bottom: 8px; }}
            code {{ 
                background: #f5f5f5; 
                padding: 2px 6px; 
                border-radius: 4px; 
                font-size: 0.95em;
            }}
            pre {{ 
                background: #f9f9f9; 
                padding: 12px; 
                border-radius: 6px; 
                overflow-x: auto;
            }}
        </style>
    </head>
    <body>
        {html_content}
    </body>
    </html>
    """

    # 保存 HTML
    with open(output_html, "w", encoding="utf-8") as f:
        f.write(styled_html)

    print(f"✅ HTML 报告已生成: {output_html}")
    return output_html


if __name__ == "__main__":
    # 示例：转换你的设计报告
    md_to_html("design_report.md", "synbio_analysis_report.html")