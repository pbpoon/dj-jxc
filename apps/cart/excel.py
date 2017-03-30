import xlrd

def excel_table_byname(file= 'file.xls',colnameindex=0):
   data = xlrd.open_workbook(file_contents=file)
   # table = data.sheet_by_name(by_name)
   table = data.sheets()[0]
   nrows = table.nrows #行数
   colnames = table.row_values(colnameindex) #某一行数据
   print(colnames)
   list =[]
   for rownum in range(1,nrows):
     row = table.row_values(rownum)
     if row:
       app = {}
       for i in range(len(colnames)):
         app[colnames[i]] = str(row[i])
       list.append(app)
   return list

