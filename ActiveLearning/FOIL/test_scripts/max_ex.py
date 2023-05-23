import json

if __name__ == '__main__':
    with open('FOIL/resultdata/bird/bird5strip4_result_5_10_5.json') as f:
        data = json.load(f)
        data = data[1:]

        max_val = 0
        max_stra = None
        max_val_idx = 1000000
        
        for strategy in data:
            curr_max = max(strategy['test_acc'])
            curr_max_idx = strategy['test_acc'].index(curr_max)
            if curr_max > max_val:
                max_val = curr_max
                max_stra = strategy['name']
                max_val_idx = curr_max_idx
            elif curr_max == max_val:
                if curr_max_idx < max_val_idx:
                    max_stra = strategy['name']
                    max_val_idx = curr_max_idx
    print(f'{max_stra}: {max_val} at index {max_val_idx}')

    # filepath = 'FOIL/resultdata/medical/med_result_10_20_5.json'
    # with open(filepath) as f:
    #     data = json.load(f)
    #     data = data[3:]

    #     bar = 0.75

    #     result_lst = []

    #     for strategy in data:
    #         curr_max = max(strategy['test_acc'])
    #         curr_max_idx = strategy['test_acc'].index(curr_max)
    #         if curr_max > bar:
    #             result_lst.append({
    #                 'name': strategy['name'],
    #                 'max': curr_max,
    #                 'max_idx': curr_max_idx
    #             })
    #     result_lst.sort(key=lambda x: (-x['max'], x['max_idx']))

    #     with open(f'med_result_10_20_5_above{bar*100}.json', 'w') as f:
    #         json.dump(result_lst, f)


    # file_names = ['FOIL/resultdata/bird/result_PART0.json', 'FOIL/resultdata/bird/result_PART1_1.json', 'FOIL/resultdata/bird/result_PART1_2.json', 
    #    'FOIL/resultdata/bird/result_PART2.json', 'FOIL/resultdata/bird/result_PART3.json']
    # for file_name in file_names:
    #     result = []
    #     with open(file_name, 'r') as f:
    #         data = json.load(f)
    #         result.extend(data)
    #     with open('FOIL/resultdata/bird/bird4_result_5_20_5.json', 'w') as f:
    #         json.dump(result, f)


    # name_lst = ['random', 'entropy', 'conflict', 'sim1_lambda02', 'sim1_lambda06', 'sim1_lambda1', 'sim2_lambda02', 'sim2_lambda06', 'sim2_lambda1',
    #                 'sim3_lambda02', 'sim3_lambda06']
    # for name in name_lst:
    #     import pickle
    #     result = []
    #     with open(f'FOIL/resultdata/bird/{name}', 'rb') as f:
    #         data = pickle.load(f)
    #         result.append(data)

    #     with open(f'FOIL/resultdata/bird/result_PART0.json', 'w') as f:
    #         json.dump(result, f)