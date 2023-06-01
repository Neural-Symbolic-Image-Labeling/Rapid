import json

data_path = 'FOIL/data_file/prof/prof_new.json'
train_status_ref = 'FOIL/data_file/prof/prof_new_train.json'
test_status_ref = 'FOIL/data_file/prof/prof_new_test.json'
val_status_ref = 'FOIL/data_file/prof/prof_new_val.json'
output_path = 'FOIL/data_file/prof/config_prof_new.json'
if __name__ == '__main__':
    result = []
    with open(data_path, 'r') as f:
        data = json.load(f)

        for img in data:
            img_info = {
                'imageId': img['imageId'],
                'train': False,
                'test': False,
                'val': False
            }
            result.append(img_info)
    
    if train_status_ref is not None:
        with open(train_status_ref, 'r') as f:
            train_status = json.load(f)
            for img in train_status:
                for img_info in result:
                    if img_info['imageId'] == img['imageId']:
                        img_info['train'] = True
                        break
    if test_status_ref is not None:
        with open(test_status_ref, 'r') as f:
            test_status = json.load(f)
            for img in test_status:
                for img_info in result:
                    if img_info['imageId'] == img['imageId']:
                        img_info['test'] = True
                        break
    if val_status_ref is not None:
        with open(val_status_ref, 'r') as f:
            val_status = json.load(f)
            for img in val_status:
                for img_info in result:
                    if img_info['imageId'] == img['imageId']:
                        img_info['val'] = True
                        break
    with open(output_path, 'w') as f:
        json.dump(result, f)


