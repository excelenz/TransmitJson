#!/usr/bin/python3
import json
import logging
import re
from datetime import datetime,timezone,timedelta

class ParserJson:
    def __init__(self):
        self.DEBUG=1
        logging.basicConfig(filename='transmitter.log',format="%(asctime)s:  %(message)s \n",datefmt='%Y-%m-%d,%H:%M',level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        self.logger.info(__name__)
        self.tz = timedelta(hours=3)
        self.timegap = datetime.now()-timedelta(days=7)
        self.my_list={'0000':[],'83':[],'84':[]}
        self.bad_list={'transmitter':[],'time':[],'type':[]}

    def main(self):

        data_list = json_object.input_from_file()
        for item in data_list['datas']:
            json_object.validation(item)
        print("\n\ngood list ************\n")
        print(self.my_list)
        print("\n\nBad list ************\n")
        print(self.bad_list)
        return True

    def validation(self,data):
        if not self.is_valid_transmitter(data):
            self.bad_list['transmitter'].append(data)
            return "not a valid transmitter in message"
        if not self.is_valid_time(data):
            self.bad_list['time'].append(data)
            return "not a fresh time in message"
        if not self.is_valid_type(data):
            self.bad_list['type'].append(data)
            return "not a valid type in message"
        else:
            type=data['msg_type']
            self.my_list['{}'.format(type)].append(data)
        return 1

    def is_valid_type(self,json):
        try:
            if json['msg_type'] in ('0000',83,84):
                return json['msg_type']
            else:
                return False
        except:
            if self.DEBUG:
                raise
            return False

    def is_valid_transmitter(self, json):
        try:
            transmitter=json['transmitter']
            pattern='^([a-zA-Z]{3}):(\d)'
            match = re.search(pattern, transmitter)
            if match:
                self.logger.info("match success %s \n" % transmitter)
                print(transmitter)
                return True
            else:
                self.logger.info("not match %s \n" % transmitter)
                print("not match %s" % transmitter)
                return False
        except:
            if self.DEBUG:
                raise
            return False

    def is_valid_time(self,json):
        try:
            msg_time_original=json['msg_time']
            msg_time=datetime.strptime(msg_time_original, '%Y-%m-%dT%H:%M:%S.%fZ')
            if self.timegap<(msg_time + self.tz) and (msg_time + self.tz)<=datetime.now():
                self.logger.info("the message is fresh %s" % self.timegap)
                print("the message is fresh %s" % self.timegap)
                return True
            else:
               self.logger.info("time is rotten %s" % msg_time)
               print("time is rotten %s" % msg_time)
               return False
        except:
            if self.DEBUG:
                raise
            return False


    def input_from_file(self):
        try:
            with open('data.txt','r') as data_list:
                data = json.loads(data_list.read())
            return data
        except Exception as e:
            self.logger.info("ERROR ON LOAD file %s" % e)
            return False

    def json_output(self,json,key,error):
        with open("data_file_{}.json".format(key), "w") as write_file:
            json.dump('"data":"{}","option":"{}"'.format(json,error), write_file)


if __name__== '__main__':
    json_object=ParserJson()
    json_object.main()


