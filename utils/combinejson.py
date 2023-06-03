import json
import os


def get_lst_id(data):
    lst_id = []
    for i in range(len(data)):
        lst_id.append(data[i]['imageId'])
    return lst_id


def change_id(jsonfile, used_id):
    lst = used_id
    with open(jsonfile) as f:
        data = json.load(f)
    for i in range(len(data)):
        if data[i]['imageId'] in lst:
            data[i]['imageId'] = len(lst) + 1
            lst.append(data[i]['imageId'])
    with open(jsonfile, 'w') as f:
        json.dump(data, f)
    return lst


def combine_json(lst_jsonfile):
    data = []
    for jsonfile in lst_jsonfile:
        with open(jsonfile) as f:
            data += json.load(f)
    return data

if __name__ == '__main__':
    init_jsonfile = '../dataset_json/downtown.json'
    with open(init_jsonfile) as f:
        data = json.load(f)
    init_id = get_lst_id(data)
    json_lst = ['../dataset_json/highway.json', '../dataset_json/mountainroad.json']
    for json_path in json_lst:
        init_id = change_id(json_path, init_id)
    print(init_id)
    data = combine_json(['../dataset_json/downtown.json', '../dataset_json/highway.json', '../dataset_json/mountainroad.json'])
