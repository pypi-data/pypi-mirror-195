import glob
import os
import time

import win32com.client as win32


def remove_meta():
    stop_word = "stresstest_lab"

    excel = win32.gencache.EnsureDispatch("Excel.Application")
    excel.Visible = False
    excel.DisplayAlerts = False
    excel.AskToUpdateLinks = False

    filetypes = ["**/*.xls", "**/*.xlsx", "**/*.xlsm"]

    for filetype in filetypes:
        for file in glob.iglob(filetype, recursive=True):
            absolute_path = os.path.abspath(file)
            print("Working with file:", absolute_path)
            try:
                wb = excel.Workbooks.Open(absolute_path)
                time.sleep(1)
            except:
                print("Error occurred when tried to open file:", absolute_path)
                continue

            workbook_links = wb.LinkSources()
            if workbook_links:
                bad_links = list(filter(lambda link: stop_word in link, workbook_links))
                if bad_links:
                    with open(
                        file="links_log.txt", mode="a+", encoding="utf-8"
                    ) as links_log:
                        links_log.write(f"In file {absolute_path} found bad links:\n")
                        for bad_link in bad_links:
                            links_log.write(f"- {bad_link}\n")
                        links_log.write("---\n\n")

            wb.RemovePersonalInformation = True
            wb.Save()
            wb.Close()

    excel.Quit()
