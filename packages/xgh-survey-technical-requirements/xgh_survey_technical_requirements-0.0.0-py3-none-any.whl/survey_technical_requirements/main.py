from pathlib import Path
import subprocess
from jinja2 import Environment
from jinja2 import FileSystemLoader
import yaml
import argparse


def load_data(data_fp):
    with open(data_fp, 'r', encoding='UTF8') as f:
        data = yaml.safe_load(f)
    return data


def get_template(template_fp):
    enviroment = Environment(loader=FileSystemLoader('.'))
    template = enviroment.get_template(template_fp)
    return template


def output_md(md_fp, content):
    with open(md_fp, 'w', encoding='UTF8') as f:
        f.write(content)
    print(f"格式化后的文件写入到： {md_fp}")


def render_md(data_fp, template_fp, out_fp):
    data = load_data(data_fp)
    template = get_template(template_fp)
    content = template.render(data)
    output_md(out_fp, content)


def convert_md2docx(md_fp, docx_fp, Reference_doc):
    subprocess.run(['pandoc', '-i', md_fp, '-o', docx_fp,
                   f'--reference-doc={Reference_doc}'])
    print(f"勘察要求写入到：{docx_fp}")


def main(argv=None):
    parser = argparse.ArgumentParser(prog='生成勘察技术要求文档')
    parser.add_argument('-d', '--data_fp', help="数据文件")
    parser.add_argument('-o', '--out_fp', help="成果文件名称")
    parser.add_argument(
        '-s', '--switch', choices=["xz", "ck", "xk"], default="xk",  help="勘察阶段：xz 选址；ck 初勘；xk 详勘")
    args = parser.parse_args(argv)
    print(args)

    template_fp = "survey_technical_requirements/templates/template_详勘技术要求.md"
    Reference_doc = Path(
        r"survey_technical_requirements\templates\template_reference.docx").absolute()
    data_fp = args.data_fp
    out_fp = args.out_fp
    docx_fp = Path(out_fp).with_suffix('.docx')

    render_md(data_fp, template_fp, out_fp)
    convert_md2docx(out_fp, docx_fp, Reference_doc)


if __name__ == "__main__":
    main()
