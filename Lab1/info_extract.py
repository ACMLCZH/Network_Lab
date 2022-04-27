import json
import msgpack


class WiFi_parser:
    def __init__(self):
        self.data_str = None
        self.myid = None
        self.mymac = None
        self.collect_time = None
        self.num_collection = None
        self.collect_list = None

    def load_data(self, data):
        self.data_str = data

    def parse(self):
        js_dict = json.loads(self.data_str)
        try:
            self.myid = js_dict["id"]
            self.mymac = js_dict["mmac"]
            self.collect_time = js_dict["time"]
            self.num_collection = len(js_dict["data"])
            self.collect_list = list()
            for i in range(self.num_collection):
                info_list = list()  # IsDevice, MAC, RSSI(-dbm, float), Range(float)
                if "router" in js_dict["data"][i]:
                    info_list.append(False)
                else:
                    info_list.append(True)
                info_list.append(js_dict["data"][i]["mac"])
                RSSI = [int(js_dict["data"][i]["rssi"])]
                for j in range(4):
                    if f"rssi{j + 1}" in js_dict["data"][i]:
                        RSSI.append(int(js_dict["data"][i][f"rssi{j + 1}"]))
                    else:
                        break
                info_list.append(RSSI)
                info_list.append(float(js_dict["data"][i]["range"]))
                self.collect_list.append(info_list)
        except:
            return True
        return False


class BlueToothParser:
    def __init__(self):
        self.data_str = None
        self.msgid = None
        self.gatemac = None
        self.gateip = None
        self.collect_time = None
        self.num_collection = None
        self.collect_list = None

    def load_data(self, data):
        self.data_str = data

    def parse(self):
        msp_dict = msgpack.loads(self.data_str)
        self.msgid = msp_dict["mid"]
        self.gatemac = msp_dict["mac"]
        self.gateip = msp_dict["ip"]
        self.collect_time = msp_dict["time"]
        self.num_collection = len(msp_dict["devices"])
        self.collect_list = list()

        for i in range(self.num_collection):
            print(msp_dict["devices"][i])
            info_list = list()  # MAC(b, 6 bytes), RSSI(-dbm, int)
            info_list.append(msp_dict["devices"][i][1:7])
            info_list.append(msp_dict["devices"][i][7] - 256)
            self.collect_list.append(info_list)
