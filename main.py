import os
from PyPDF2 import PdfFileWriter, PdfFileReader, PdfFileMerger
from PIL import Image
from hashlib import md5 as md5_
from pdf2image import convert_from_path as convertPDF

EXIT = -1

def md5(x):
    md = md5_()
    md.update(x.encode())
    return md.hexdigest()

def filename(fnm):
    return fnm[max(fnm.rfind('\\') + 1, fnm.rfind('/') + 1, 0):]

def selection(pages):
    oper = {}
    for i, k in enumerate(pages):
        print(f"{str(i + 1).rjust(3)}: {k}")
        oper[i + 1] = pages[k]
    choice = int(input('请选择: '))
    while choice not in range(1, len(pages) + 1):
        choice = int(input(f"请重新选择[1-{len(pages)}]: "))
    def safe_call():
        try:
            return oper[choice]()
        except:
            print('执行出错')
            return None
    return safe_call()

def inquire(hint, checker, errhint):
    def safe_checker(x):
        try:
            return checker(x)
        except:
            return False
    ret = input(hint)
    while not safe_checker(ret):
        print(errhint)
        ret = input("请重新输入：")
    return ret

def splitPDF():
    pdf_path = inquire("请拖入需要拆分的PDF文件：",
        os.path.exists,
        '文件不存在')
    input_stream = open(pdf_path, 'rb')
    reader = PdfFileReader(input_stream)
    writer = PdfFileWriter()
    start = int(inquire("需要从第几页开始截取：",
        lambda x: 0 < int(x) < len(reader.pages),
        '页码超出范围'))
    end = int(inquire("需要截取到第几页: ",
        lambda x: 0 < int(x) < len(reader.pages),
        '页码超出范围'))
    output_fnm = f"截取{start}-{end}.pdf"
    for j in range(start - 1, end):
        page = reader.getPage(j)
        writer.addPage(page)
    out_stream = open(output_fnm, 'wb')
    writer.write(out_stream)
    out_stream.close()
    input_stream.close()
    print(f'已经保存到文件{os.getcwd()}\\{output_fnm}')

def mergePDF():
    file_merger = PdfFileMerger()
    file_list = []
    n = int(inquire('请输入需要合并的PDF文件数量：',
        lambda x: int(x) > 0,
        '请输入非负整数'))
    for _ in range(n):
        fnm = inquire('请按次序拖入需要合并的PDF文件：',
            os.path.exists,
            '文件不存在')
        file_list.append(filename(fnm))
        file_merger.append(fnm)
    output_fnm = f"合并-{str(n)}-{md5('.'.join(file_list))}.pdf"
    file_merger.write(output_fnm)
    file_merger.close()
    print(f'已经保存到文件{os.getcwd()}\\{output_fnm}')

def fromImage():
    file_list = []
    img = []
    n = int(inquire('请输入需要合并的图片数量：',
        lambda x: int(x) > 0,
        '请输入非负整数'))
    for _ in range(n):
        fnm = inquire('请按次序拖入需要合并的图片：',
            os.path.exists,
            '图片不存在')
        file_list.append(filename(fnm))
        img.append(Image.open(fnm))
    print(file_list)
    print(img)
    print(md5('.'.join(file_list)))
    output_fnm = f"合并-{str(n)}-{md5('.'.join(file_list))}.pdf"
    img[0].save(output_fnm, 'pdf', save_all=True, append_images=img[1:])
    print(f'已经保存到文件{os.getcwd()}\\{output_fnm}')

def toImage():
    path = inquire("请拖入需要拆分的PDF文件：",
        os.path.exists,
        '文件不存在')
    image = convertPDF(path)
    cur_page = 0
    for img in image:
        cur_page += 1
        img.save(f'Page-{cur_page}.png', 'png')
    print(f'已经保存到文件夹{os.getcwd()}，共计输出{cur_page}页')

def main():
    return selection({
        '拆分PDF': splitPDF,
        '合并PDF': mergePDF,
        '从图片生成PDF': fromImage,
        'PDF拆分为图片': toImage,
        '退出': lambda :EXIT
    })

if __name__ == '__main__':
    while True:
        if main() == EXIT:
            break
        print()