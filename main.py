import os
from PyPDF2 import PdfFileWriter, PdfFileReader, PdfFileMerger

EXIT = -1

def split(pdf_file, out_filename, start, end):
    if not os.path.exists(pdf_file):
        print('文件不存在')
        return False
    input_stream = open(pdf_file, 'rb')
    pdf_input = PdfFileReader(input_stream)
    
    pdf_out = PdfFileWriter()
    for j in range(start - 1, end):
        page = pdf_input.getPage(j)
        pdf_out.addPage(page)
    out_stream = open(out_filename, 'wb')
    pdf_out.write(out_stream)
    out_stream.close()
    input_stream.close()
    print('成功')
    return True

def selection(pages):
    oper = {}
    for i, k in enumerate(pages):
        print(f"{str(i + 1).rjust(3)}: {k}")
        oper[i + 1] = pages[k]
    choice = int(input('请选择: '))
    while choice not in range(1, len(pages) + 1):
        choice = int(input(f"请重新选择[1-{len(pages)}]: "))
    return oper[choice]()

def splitPDF():
    pdf_path = input("请按拖入需要拆分的PDF文件：")
    start = int(input("需要从第几页开始截取："))
    end = int(input("需要截取到第几页: "))
    output_fnm = f"截取{start}-{end}.pdf"
    if split(pdf_path, output_fnm, start, end):
        print(f'已经保存到文件{os.getcwd()}\\{output_fnm}')

def mergePDF():
    file_merger = PdfFileMerger()
    file_list = []
    n = int(input('请输入需要合并的PDF文件数量：'))
    for i in range(n):
        fnm = input('请按次序拖入需要合并的PDF文件：')
        file_list.append(fnm[max(fnm.rfind('\\') + 1, fnm.rfind('/') + 1, 0):])
        file_merger.append(fnm)
    output_fnm = f"合并-{'.'.join(file_list)}.pdf"
    file_merger.write(output_fnm)
    print(f'已经保存到文件{os.getcwd()}\\{output_fnm}')

def main():
    return selection({
        '拆分PDF': splitPDF,
        '合并PDF': mergePDF,
        '退出': lambda :EXIT
    })

if __name__ == '__main__':
    while True:
        if main() == EXIT:
            break
        print()