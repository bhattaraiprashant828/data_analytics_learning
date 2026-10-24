import PyPDF2

pdfFiles=['1.pdf', '2.pdf']
merger=PyPDF2.PdfMerger()

for filename in pdfFiles:
    pdfFile=open(filename,'rb')
    merger.append(pdfFile)

merger.write('merged.pdf')
merger.close()
