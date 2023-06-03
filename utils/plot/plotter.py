import pickle
import matplotlib.pyplot as plt
import numpy as np
import json

sim_lambda_dataset_labels = ["Random", r"Sim{0} lambd=0.2", r"Sim{0} lambd=0.6", r"Sim{0} lambd=1"]
size_test_labels = ["Random", r"Sim1 lambd={0} size=20", r"Sim1 lambd={0} size=50", r"Sim1 lambd={0} size=100",
                    r"Sim2 lambd={0} size=20", r"Sim2 lambd={0} size=50", r"Sim2 lambd={0} size=100", 
                    r"Sim3 lambd={0} size=20", r"Sim3 lambd={0} size=50", r"Sim3 lambd={0} size=100"]
compare_all_labels = ["Random", "Conflict", "Entropy", "Sim1 lambd=0.6 size=50", "Sim2 lambd=0.6 size=50", "Sim3 lambd=0.6 size=50"]

# def plot_helper(acc_data_lst, hr_data_lst, label_lst, file_name="result.png"):
#     with plt.style.context('seaborn-whitegrid'):
#             plt.figure(figsize=(10, 10))
#
#             # Accuracy
#             plt.subplot(2, 1, 1)
#             ax = plt.gca()
#             ax.xaxis.set_major_locator(plt.MaxNLocator(integer=True))
#             plt.xticks(np.arange(0, 20, 1))
#             plt.xlabel(f"Query instance(s) per round)", fontsize=14)
#             plt.ylabel('Accuracy', fontsize=14)
#             for idx, item in enumerate(acc_data_lst):
#                 plt.plot(np.arange(len(item), dtype=int), item, label=f"{label_lst[idx]}")
#             plt.legend()
#
#             # Hit rate
#             plt.subplot(2, 1, 2)
#             plt.xlabel(f"Query instance(s) per round)")
#             plt.ylabel('Hit rate')
#             for idx, item in enumerate(hr_data_lst):
#                     plt.plot(np.arange(len(item), dtype=int), item, label=f"{label_lst[idx]}")
#             plt.legend()
#
#             plt.savefig(file_name)
#             # plt.show()

def plot_helper(data_lst, label_lst, file_name="result.png", name="Accuracy"):
    with plt.style.context('seaborn-whitegrid'):
            plt.figure(figsize=(10, 5))
            ax = plt.gca()
            ax.xaxis.set_major_locator(plt.MaxNLocator(integer=True)), 
            ax.xaxis.grid(False)
            plt.xticks(np.arange(1, 31, 2), fontsize=13)
            # plt.xlabel(f"Query (5 instances per round)", fontsize=18)
            plt.xlabel(f"Iteration", fontsize=20)

            # prof 0-0.85
            # plt.ylim(0,0.85)
            # plt.yticks(np.arange(0,0.85, 0.05), fontsize=13)

            #bird 0.2-0.65
            plt.ylim(0.1, 0.8)
            plt.yticks(np.arange(0.1, 0.8, 0.05), fontsize=13)

            # plt.ylim(0,0.9)
            # plt.yticks(np.arange(0,0.9, 0.05), fontsize=13)
            # plt.ylim(0.4, 0.9)
            # plt.yticks(np.arange(0.4, 0.9, 0.05), fontsize=13)

            plt.ylabel(name, fontsize=20)
            for idx, item in enumerate(data_lst):
                plt.plot(np.arange(1,len(item)+1, dtype=int), item, label=f"{label_lst[idx]}",marker ='.', markersize=10, linewidth=2)
            plt.legend(fontsize=16, frameon=True)
            plt.savefig(file_name, format="pdf")

def plot_helper_hit(data_lst, label_lst, file_name="result.png", name="Hit Rate"):
    with plt.style.context('seaborn-whitegrid'):
            plt.figure(figsize=(10, 5))
            ax = plt.gca()
            ax.xaxis.set_major_locator(plt.MaxNLocator(integer=True)), 
            ax.xaxis.grid(False)
            plt.xticks(np.arange(1, 40, 2), fontsize=13)
            # plt.xlabel(f"Query (5 instances per round)", fontsize=18)
            plt.xlabel(f"Iteration", fontsize=20)

            plt.ylim(0 - 0.1, 1.1)
            plt.yticks(fontsize=13)
            plt.ylabel(name, fontsize=20)
            for idx, item in enumerate(data_lst):
                plt.plot(np.arange(1,len(item)+1, dtype=int), item, label=f"{label_lst[idx]}",marker ='.', markersize=10, linewidth=2)
            plt.legend(fontsize=16, frameon=True, loc='lower left')
            plt.savefig(file_name, format="pdf")

def plot_sim_lambda_ds(data, sim_idx, file_name="sim_lambda_dataset.png"):
    plot_helper(data[0::2], data[1::2], [label.format(sim_idx) for label in sim_lambda_dataset_labels], file_name)

def plot_size_test(data, lambd, file_name="sizetest.png"):
    plot_helper(data[0::2], data[1::2], [label.format(lambd) for label in size_test_labels], file_name)

def plot_compare_all(data, file_name="compareall.png"):
    plot_helper(data[0::2], data[1::2], compare_all_labels, file_name)
    
def plot_all(prefix="ad_"):
    with open(f'{prefix}_sim1_lambdatest', 'rb') as f:
        data = pickle.load(f)
        plot_sim_lambda_ds(data, 1, f"{prefix}_sim1.png")
    with open(f'{prefix}_sim2_lambdatest', 'rb') as f:
        data = pickle.load(f)
        plot_sim_lambda_ds(data, 2, f"{prefix}_sim2.png")
    with open(f'{prefix}_sim3_lambdatest', 'rb') as f:
        data = pickle.load(f)
        plot_sim_lambda_ds(data, 3, f"{prefix}_sim3.png")
    with open(f'{prefix}_sizetest02', 'rb') as f:
        data = pickle.load(f)
        plot_size_test(data,0.2, f"{prefix}_sizetest02.png")
    with open(f'{prefix}_sizetest06', 'rb') as f:
        data = pickle.load(f)
        plot_size_test(data,0.6, f"{prefix}_sizetest06.png")
    with open(f'{prefix}_sizetest1', 'rb') as f:
        data = pickle.load(f)
        plot_size_test(data,1, f"{prefix}_sizetest1.png")
    with open(f'{prefix}_compare_all', 'rb') as f:
        data = pickle.load(f)
        plot_compare_all(data, f"{prefix}_compareall.png")

if __name__ == "__main__":
    # Make sure all data file names are in format "<prefix>_name". 
    # For example, "ad_sim1_lambdatest", "ad_sim2_lambdatest", "ad_sim3_lambdatest", "ad_sizetest", "ad_compare_all"
    # plot_all(prefix="prof")
    # Read AD test result
    # with open("resultdata/prof/prof_leatest_result.json", "r") as f:
    #     data = json.load(f)
    # for key in data:
    #     print(key)
    # Sim 1 lambda comparison
    # label = ["Random", r"Sim1 lambd=0.2", r"Sim1 lambd=0.6", r"Sim1 lambd=1"]
    # acc_lst = [result['acc'] for result in data if result['name'] in ["random", "similarity1_lambda02", "similarity1_lambda06", "similarity1_lambda1"]]
    # hr_lst = [result['hit_rate'] for result in data if result['name'] in ["random", "similarity1_lambda02", "similarity1_lambda06", "similarity1_lambda1"]]
    # plot_helper(acc_lst, hr_lst, label, "ad_sim1.png")
    # Sim 1 lambda 0.2 Size comparison
    # label = ["Random", r"Sim1 lambd=0.2 size=20", r"Sim1 lambd=0.2 size=50", r"Sim1 lambd=0.2 size=100"]
    # acc_lst = [result['acc'] for result in data if result['name'] in ["random", "similarity1_lambda02_size20", "similarity1_lambda02_size50", "similarity1_lambda02"]]
    # hr_lst = [result['hit_rate'] for result in data if result['name'] in ["random", "similarity1_lambda02_size20", "similarity1_lambda02_size50", "similarity1_lambda02"]]
    # plot_helper(acc_lst, hr_lst, label, "ad_sim1_lambda02_size.png")
    # Sim 1 lambda 0.2 Size 100 Compare all
    # label = ["Random", "Entropy", "Conflict","Suggested","Diversity","Informative"]
    # acc_lst = [result['acc'] for result in data if result['name'] in ["random", "entropy", "conflict", "suggested","diversity","informative"]]
    # hr_lst = [result['hit_rate'] for result in data if result['name'] in ["random", "entropy", "conflict", "suggested","diversity","informative"]]
    # # plot_helper(acc_lst, hr_lst, label, "ad_sim1_lambda02_size100_compareall.png")
    # # Accuracy
    # plot_helper(acc_lst, label, "ad_sim1_lambda02_size100_compareall_acc.png", "Accuracy")
    # # Hit rate
    # plot_helper_hit(hr_lst, label, "ad_sim1_lambda02_size100_compareall_hr.png", "Hit rate")

    ### Test plot
    # Occupation
    # labels = ["Random", "Entropy", "Diversity", "Informative", "Multi-criteria (Ours)"]
    # strategy = "sim3_lambda6_size100"
    # acc_lst = []
    # for label in labels:
    #     for result in data['comps']:
    #         if label.lower() in result['name']:
    #             print(result['name'])
    #             acc_lst.append(result['test_acc'])
    #             break
    #         elif result['name'] == strategy:
    #             print(result['name'])
    #             acc_lst.append(result['test_acc'])
    # acc_lst = [result['test_acc'] for result in data['comps'] if result['name'] in ["random", "entropy", "conflict", "sim2_lambda2_size20","diversity_1","informative_1"]]
    # print(acc_lst)
    # print(len(acc_lst))
    # hr_lst = [result['hit_rate'] for result in data['comps']  if result['name'] in ["random", "entropy", "conflict", "sim1_lambda2_size20","diversity_1","informative_1"]]
    # plot_helper(acc_lst, hr_lst, label, "ad_sim1_lambda02_size100_compareall.png")
    # Accuracy
    # plot_helper(acc_lst, labels, "prof_cl_acc.pdf", "Accuracy")
    # Hit rate
    # plot_helper_hit(hr_lst, label, "prof_cl_hr.pdf", "Hit rate")

    # Bird 168169170
    # with open("resultdata/bird/bird_result_0126_171.json", "r") as f:
    #     data = json.load(f)
    #
    # labels = ["Random", "Entropy", "Diversity", "Informative", "Multi-criteria (Ours)"]
    # strategy = "sim1_lambda6_size50"
    # acc_lst = []
    # hr_lst = []
    # for label in labels:
    #     for result in data['comps']:
    #         if label.lower() in result['name']:
    #             print(result['name'])
    #             acc_lst.append(result['test_acc'])
    #             hr_lst.append(result['hit_rates'])
    #             break
    #         elif result['name'] == strategy:
    #             print(result['name'])
    #             acc_lst.append(result['test_acc'])
    #             hr_lst.append(result['hit_rates'])
    #
    # plot_helper(acc_lst, labels, "bird_result_0126_171_cl_acc.pdf", "Accuracy")
    # plot_helper_hit(hr_lst, labels, "bird_result_0126_171_cl_hr.pdf", "Hit rate")

    # Medical
    # with open("resultdata/medical/medical_result_jan29.json", "r") as f:
    #     data = json.load(f)
    #
    # labels = ["Random", "Entropy", "Diversity", "Informative", "Multi-criteria (Ours)"]
    # strategy = "sim1_lambda2_size20"
    # acc_lst = []
    # hr_lst = []
    # for label in labels:
    #     for result in data['comps']:
    #         if label.lower() in result['name']:
    #             print(result['name'])
    #             acc_lst.append(result['test_acc'])
    #             hr_lst.append(result['hit_rates'])
    #             break
    #         elif result['name'] == strategy:
    #             print(result['name'])
    #             acc_lst.append(result['test_acc'])
    #             hr_lst.append(result['hit_rates'])
    #
    # # plot_helper(acc_lst, labels, "plots/medical/medical_3_20_0126_cl_acc.pdf", "Accuracy")
    # # plot_helper_hit(hr_lst, labels, "plots/medical/medical_3_20_0126_cl_hr.pdf", "Hit rate")
    # plot_helper(acc_lst, labels, "plots/medical/medical_result_jan29_cl_acc.pdf", "Accuracy")
    # plot_helper_hit(hr_lst, labels, "plots/medical/medical_result_jan29_cl_hr.pdf", "Hit rate")

    # Prof
    # with open("resultdata/prof/prof_result_0125.json", "r") as f:
    #     data = json.load(f)
    #
    # labels = ["Random", "Entropy", "Diversity", "Informative", "Multi-criteria (Ours)"]
    # strategy = "sim2_lambda1_size20"
    # acc_lst = []
    # hr_lst = []
    # for label in labels:
    #     for result in data['comps']:
    #         if label.lower() in result['name']:
    #             print(result['name'])
    #             acc_lst.append(result['test_acc'])
    #             hr_lst.append(result['hit_rates'])
    #             break
    #         elif result['name'] == strategy:
    #             print(result['name'])
    #             acc_lst.append(result['test_acc'])
    #             hr_lst.append(result['hit_rates'])
    #
    # plot_helper(acc_lst, labels, "plots/prof/prof_0125_cl_acc.pdf", "Accuracy")
    # plot_helper_hit(hr_lst, labels, "plots/prof/prof_0125_cl_hr.pdf", "Hit rate")

    # AD 5 20
    # with open("resultdata/ad/adinitial_result_5_5_19.json", "r") as f:
    #     data = json.load(f)
    #
    # labels = ["Random", "Entropy", "Diversity", "Informative", "Multi-criteria (Ours)"]
    # strategy = "sim2_lambda2_size20"
    # acc_lst = []
    # hr_lst = []
    # for label in labels:
    #     for result in data['comps']:
    #         if label.lower() in result['name']:
    #             print(result['name'])
    #             acc_lst.append(result['test_acc'])
    #             hr_lst.append(result['hit_rates'])
    #             break
    #         elif result['name'] == strategy:
    #             print(result['name'])
    #             acc_lst.append(result['test_acc'])
    #             hr_lst.append(result['hit_rates'])
    #
    # plot_helper(acc_lst, labels, "plots/ad/ad_5_5_19_cl_acc.pdf", "Accuracy")
    # plot_helper_hit(hr_lst, labels, "plots/ad/ad_5_5_19_cl_hr.pdf", "Hit rate")

    # AD 3 33
    with open("resultdata/ad/ad_result_3_30_jan26.json", "r") as f:
        data = json.load(f)

    labels = ["Random", "Diversity", "Informativeness", "Multi-criteria"]
    strategy = "sim2_lambda1_size20"
    acc_lst = []
    hr_lst = []
    for label in labels:
        for result in data['comps']:
            if label.lower() in result['name']:
                print(result['name'])
                acc_lst.append(result['test_acc'])
                hr_lst.append([1 - a for a in result['hit_rates']])
                break
            elif label == "Informativeness" and "informative" in result['name']:
                print(result['name'])
                acc_lst.append(result['test_acc'])
                hr_lst.append([1 - a for a in result['hit_rates']])
                break
            elif result['name'] == strategy:
                print(result['name'])
                acc_lst.append(result['test_acc'])
                hr_lst.append([1 - a for a in result['hit_rates']])

    print(len(acc_lst[0]))
    print(len(hr_lst[0]))
    # Remove the last item in each list in acc_lst
    for i in range(len(acc_lst)):
        acc_lst[i] = acc_lst[i][:-1]
    print(len(acc_lst[0]))
    print(len(hr_lst[0]))
    plot_helper(acc_lst, labels, "plots/ad/ad_3_30_0126_cl_acc.pdf", "Accuracy")
    plot_helper_hit(hr_lst, labels, "plots/ad/ad_3_30_0126_cl_hr.pdf", "Hit rate")
    #


