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
            plt.xticks(np.arange(1, 22, 2), fontsize=13)
            plt.xlabel(f"Query (12 instances per round)", fontsize=18)
            plt.ylim(0.3,0.85)
            plt.yticks(np.arange(0.3,0.85, 0.05), fontsize=13)
            plt.ylabel(name, fontsize=18)
            for idx, item in enumerate(data_lst):
                plt.plot(np.arange(1,len(item)+1, dtype=int), item, label=f"{label_lst[idx]}",marker ='.', markersize=10, linewidth=2)
            plt.legend(fontsize=14, frameon=True)
            plt.savefig("adacc.pdf", format="pdf")

def plot_helper_hit(data_lst, label_lst, file_name="result.png", name="Accuracy"):
    with plt.style.context('seaborn-whitegrid'):
            plt.figure(figsize=(10, 5))
            ax = plt.gca()
            ax.xaxis.set_major_locator(plt.MaxNLocator(integer=True)), 
            ax.xaxis.grid(False)
            plt.xticks(np.arange(1, 22, 2), fontsize=13)
            plt.xlabel(f"Query (12 instances per round)", fontsize=18)
            plt.ylim(0,1)
            plt.yticks(fontsize=13)
            plt.ylabel(name, fontsize=18)
            for idx, item in enumerate(data_lst):
                plt.plot(np.arange(1,len(item)+1, dtype=int), item, label=f"{label_lst[idx]}",marker ='.', markersize=10, linewidth=2)
            plt.legend(fontsize=14, frameon=True, loc='upper left')
            plt.savefig("adacc_hit.pdf", format="pdf")

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
    with open("resultdata/ad/compareall.json", "r") as f:
        data = json.load(f)
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
    label = ["Random", "Entropy", "Conflict","Suggested","Diversity","Informative"]
    acc_lst = [result['acc'] for result in data if result['name'] in ["random", "entropy", "conflict", "suggested","diversity","informative"]]
    hr_lst = [result['hit_rate'] for result in data if result['name'] in ["random", "entropy", "conflict", "suggested","diversity","informative"]]
    # plot_helper(acc_lst, hr_lst, label, "ad_sim1_lambda02_size100_compareall.png")
    # Accuracy
    plot_helper(acc_lst, label, "ad_sim1_lambda02_size100_compareall_acc.png", "Accuracy")
    # Hit rate
    plot_helper_hit(hr_lst, label, "ad_sim1_lambda02_size100_compareall_hr.png", "Hit rate")


