import json

class Config:
    def __init__(self):
        self.file1_path = "result_highaccsim.json"
        self.file2_path = "100000rounds_max.json"

        self.file1_acc_struct = ["comps", 20, "max_acc"] # file1 json path to target accuracy
        self.file1_compare_init_struct = ["comps", 20, "init_imgs"] # file1 json path to init imgs
        self.file1_compare_query_struct = ["comps", 20, "query_imgs"] # file1 json path to query imgs

        self.file2_acc_struct = ["max_rounds", 0, "acc"] # file2 target accuracy
        self.file2_compare_init_struct = ["max_rounds", 0, "initial_imageIds"] # file2 json path to init imgs
        self.file2_compare_query_struct = ["max_rounds", 0, "query_imageIds"] # file2 json path to query imgs

        self.output_path = "common_imgs.json"


def find_json_item(json, json_struct):
    target = json
    for key in json_struct:
        if isinstance(target, list):
            target = target[key]
        elif isinstance(target, dict):
            target = target[key]
    return target

if __name__ == '__main__':
    config = Config()

    json1 = json.load(open(config.file1_path))
    json2 = json.load(open(config.file2_path))

    file1_init_imgs = find_json_item(json1, config.file1_compare_init_struct)
    print(f'file1 init imgs: {len(file1_init_imgs)}, {len(set(file1_init_imgs))}')
    file1_query_imgs = find_json_item(json1, config.file1_compare_query_struct)
    print(f'file1 query imgs: {len(file1_query_imgs)}, {len(set(file1_query_imgs))}')

    file2_init_imgs = find_json_item(json2, config.file2_compare_init_struct)
    print(f'file2 init imgs: {len(file2_init_imgs)}, {len(set(file2_init_imgs))}')
    file2_query_imgs = find_json_item(json2, config.file2_compare_query_struct)
    print(f'file2 query imgs: {len(file2_query_imgs)}, {len(set(file2_query_imgs))}')

    file1_imgs = file1_init_imgs + file1_query_imgs
    file2_imgs = file2_init_imgs + file2_query_imgs

    common_imgs = set(file1_imgs).intersection(set(file2_imgs))
    unique1 = set(file1_imgs).difference(common_imgs)
    unique2 = set(file2_imgs).difference(common_imgs)

    result = {
        'file1': config.file1_path,
        'file2': config.file2_path,
        'file1_top1_acc': find_json_item(json1, config.file1_acc_struct),
        'file2_top1_acc': find_json_item(json2, config.file2_acc_struct),
        'common_imgs': list(common_imgs),
        'file1_unique_imgs': list(unique1),
        'file2_unique_imgs': list(unique2)
    }

    with open('common_imgs.json', 'w') as f:
        json.dump(result, f)