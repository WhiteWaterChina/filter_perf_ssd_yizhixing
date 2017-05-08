#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:yanshuo@inspur.com

import matplotlib.pyplot as plyt
import numpy
import time
import os
import sys
import subprocess
import re
import shutil


def get_data(filename_test, filename_result):
    filename_display = "%s.result" % filename_test
    fio_process = subprocess.call("./fio %s >> results/%s" % (filename_test, filename_display), shell=True)
    if fio_process == 0:
        print "Run %s successfully!" % filename_test
    else:
        print "FIO run fail! Please check!"
    if filename_result != "None":
        data_list_temp = []
        data_time = []
        data_over_list = []
        filename_to_filter = os.path.join("results", filename_result)
        file_data = open(filename_to_filter, mode='r')
        for item_file_data in file_data:
            if item_file_data != os.linesep:
                data_data = item_change_devicename.split(',')[1]
                data_list_temp.append(int(data_data.strip()))
        data_list_temp.reverse()
        data_list = data_list_temp[:2700]
        data_list.reverse()
        length = len(data_list)
        for i in range(1, length + 1):
            data_time.append(i)
        average_data = float(sum(data_list)) / float(len(data_list))
    #    print "Average data is %s" % average_data
        data_high = average_data * 1.1
        data_low = average_data * 0.9
        data_higest = max(data_list)
        index_higest = data_list.index(data_higest)
        data_lowest = min(data_list)
        index_lowest = data_list.index(data_lowest)
        for item_data in data_list:
            if item_data <= data_low or item_data >= data_high:
                data_over_list.append(item_data)
        data_yizhixing = 1 - round(float(len(data_over_list)) / float(len(data_list)), 3)
    #    print "current yizhixing is %s" % data_yizhixing
        data_x = numpy.array(data_time)
        data_y = numpy.array(data_list)
        data_high_list = []
        data_low_list = []
        for count in range(len(data_list)):
            data_high_list.append(data_high)
            data_low_list.append(data_low)
        filename_to_write = filename_test.split('.')[0]
        figure_1 = plyt.figure(filename_to_write)
        figure = figure_1.add_subplot(111)
        plyt.title(filename_to_write)
        plyt.plot(data_x, data_y, color='red')
        plyt.plot(data_x, numpy.array(data_high_list), color='blue')
        plyt.plot(data_x, numpy.array(data_low_list), color='blue')
        figure.annotate('High = %s' % data_high, xy=(1000, data_high), xytext=(1500, data_high))
        figure.annotate('Low = %s' % data_low, xy=(1000, data_low), xytext=(1500, data_low))
        figure.annotate('Average = %s' % average_data, xy=(1000, average_data), xytext=(1500, average_data))
        figure.annotate('yizhixing = %s' % data_yizhixing, xy=(200, average_data), xytext=(300, average_data))
        figure.annotate('Highest(xy) = (%s,%s)' % (index_higest, data_higest), xy=(index_higest, data_higest), xytext=(index_higest, data_higest))
        figure.annotate('Lowest(xy) = (%s,%s)' % (index_lowest, data_lowest), xy=(index_lowest, data_lowest), xytext=(index_lowest, data_lowest))
        time.sleep(1)
        filename_to_write_all = filename_to_write + '_image.png'
        filename_to_save = os.path.join("results", filename_to_write_all)
        figure_1.savefig(filename_to_save)


def change_devicename(filename_test):
    pattern = re.compile(r"filename=.*")
    file_under_filter = open(filename_test, mode='r')
    text_under_filter = file_under_filter.read()
    file_under_filter.close()
    new_text = re.sub(pattern=pattern, repl="filename=%s" % sys.argv[1], string=text_under_filter)
    file_under_filter = open(filename_test, mode='w')
    file_under_filter.write(new_text)
    file_under_filter.close()


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print "Usage: python2.7 filter_perf_ssd /dev/sdx or /dev/nvme0n1"
        sys.exit(1)
    devicename_to_test = sys.argv[1]
    filename_test_list = ["seqprecondition.fio", "seqwrite.fio", "seqread.fio", "randomprecondition.fio", "randomwrite.fio", "randomread.fio"]
    filename_result_list = ["None", "seqwrite_bw.1.log", "seqread_bw.1.log", "None", "randomwrite_iops.1.log", "randomread_iops.1.log"]
    print "Begin to test %s" % devicename_to_test
    print "Begin Time is %s" % time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    chmod = subprocess.call("chmod 777 fio", shell=True)
    if os.path.exists("results") and os.path.isdir("results"):
        shutil.rmtree("results")
    os.mkdir("results")
    for item_change_devicename in filename_test_list:
        change_devicename(item_change_devicename)
    for index, item in enumerate(filename_test_list):
        print "Begin to test %s" % item
        get_data(item, filename_result_list[index])
    print "End Time is %s" % time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
