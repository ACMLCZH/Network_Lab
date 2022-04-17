import json


class WiFi_parser:
    def __init__(self):
        self.data_str = None
        self.id = None
        self.myid = None
        self.mymac = None
        self.collect_time = None
        self.num_collection = None

    def load_data(self, data):
        self.data_str = data

    def parse(self):
        js_dict = json.load(self.data_str)
        self.myid = js_dict["id"]
        self.mymac = js_dict["mmac"]
        self.collect_time = js_dict["time"]
        self.num_collection = len(js_dict["data"])
        for i in range(self.num_collection):
            info_list = list()      # IsDevice, MAC, RSSI(-dbm, float), Range(float)
            if "router" in js_dict["data"][i]:
                info_list.append(False)
            else:
                info_list.append(True)
            info_list.append(js_dict["data"][i]["mac"])
            RSSI = [float(js_dict["data"][i]["rssi"])]
            for j in range(4):
                if f"rssi{j + 1}" in js_dict["data"][i]:
                    RSSI.append(float(js_dict["data"][i][f"rssi{j + 1}"]))
                else:
                    break
            info_list.append(RSSI)
            info_list.append(float(js_dict["data"][i]["range"]))

class BlueToothParser:
    