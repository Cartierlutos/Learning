import os
import sys
import csv
import time
import string
import rosbag
import shutil


def Rosbag2csv(base_dir):
    count = 0
    rosbag_list = []
    for root_dir, file_folder, files_list in os.walk(base_dir):
        """
        root_dir    
        file_folder : list
        files       : list
        """
        for file in files_list:
            print(file)
            res = os.path.splitext(file)
            if res[1] == '.bag':
                rosbag_list.append(file)
    for rosbag_file in rosbag_list:
        count += 1
        print(f"Reading file  {count} / {len(rosbag_list)} : {rosbag_file} ")
        bag = rosbag.Bag(rosbag_file)
        bagContents = bag.read_messages()
        bagName = bag.filename

        output_folder = str.strip(bagName, ".bag")
        try:
            os.mkdir(output_folder)
        except:
            pass
        shutil.copyfile(bagName, output_folder + '/' + bagName)

        topicList = []
        for topic, msg, t in bagContents:
            if topic not in topicList:
                topicList.append(topic)
        for topicName in topicList:
            fileName = output_folder + '/' + topicName + '.csv'
            with open(fileName, "w+") as csvFile:
                fileWriter = csv.writer(csvFile, delimiter=',')
                firstIteration = True
                for subtopic, msg, t in bag.read_messages(topicName):
                    msgString = str(msg)
                    msgList = str.split(msgString, '\n')
                    dataList = []
                    for dataValue in msgList:
                        data_split = str.split(dataValue, ":")
                        for i in range(len(data_split)):
                            data_split[i] = str.strip(data_split[i])
                        dataList.append(data_split)
                    if firstIteration:
                        headers = ["rosbagTimestamp"]
                        for header_data in dataList:
                            headers.append(header_data[0])
                        fileWriter.writerow(headers)
                        firstIteration = False
                    values = [str(t)]
                    for tdata in dataList:
                        if len(tdata) > 1:
                            values.append(tdata[1])
                    fileWriter.writerow(values)
        bag.close()
    print(f"---Have transformed all the {len(rosbag_list)} bag files---")

Rosbag2csv('/home/itcast/rosbbag')
