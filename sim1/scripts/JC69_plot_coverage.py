import os

from matplotlib import pyplot as plt
import numpy as np


def translate_stats_log(file_path):
    translate_map = {

        "D.treeLikelihood": "treeLikelihood"

    }
    if os.path.exists(file_path + ".orig"):
        return
    os.rename(file_path, file_path + ".orig")
    writer = open(file_path, 'w')
    with open(file_path + ".orig", 'r') as reader:
        header_line = reader.readline().strip()
        headers = header_line.split('\t')
        for i in range(len(headers)):
            if headers[i] in translate_map:
                headers[i] = translate_map[headers[i]]
        writer.write("\t".join(headers) + "\n")
        for data_line in reader:
            writer.write(data_line)
    writer.close()


def translate_all_stats_logs(filepath):
    for i in range(100):
        translate_stats_log(filepath % i)


def parse_true_csv(file_path):
    sep = "\t"
    with open(file_path, 'r') as reader:
        header_line = reader.readline().strip()
        data_line = reader.readline().strip()
        headers = header_line.split(sep)
        data = data_line.split(sep)
        zipped_data = zip(headers, data)
        result = {}
        # for header, data in zipped_data:
        #     result[header] = float(data)
        for header, data in zipped_data:
            try:
                result[header] = float(data)
            except ValueError:
                result[header] = data

        return result


def parse_stats_log(file_path):
    with open(file_path, 'r') as reader:
        result = {}
        header_line = reader.readline().strip()
        headers = header_line.split('\t')[1:]

        for data_line in reader:
            data_line = data_line.strip()
            items = data_line.split('\t')
            trace = items[0]
            if trace == "mode":
                continue

            items = items[1:]

            zipped_data = zip(headers, items)
            tmp = {}
            for header, data in zipped_data:
                tmp[header] = float(data)

            result[trace] = tmp

    return result


def plot_figs(stats_path, true_path, parameter_list):
    true = []
    mean = []
    hdp95lower = []
    hdp95upper = []
    ess = []
    # translate stats logs
    translate_all_stats_logs(stats_path)
    # convert parameters to math characters
    parameter_map = {
        "f0": "f0",
        "NInfinity": "NInfinity",
        "b": "b",
        "tree.height": "treeheight",
        "tree.treeLength": "treelength"



    }
    # figure settings
    font_size = 12
    width = 6.75 / 2
    plt.rcParams['font.family'] = 'Helvetica'
    plt.rc('font', size=font_size)
    plt.rc('axes', titlesize=font_size)
    plt.rcParams['figure.figsize'] = (width, width)
    plt.rcParams['figure.dpi'] = 300
    # process files
    for fileid in range(100):
        stats_file = stats_path % fileid
        true_file = true_path % fileid
        stats_data = parse_stats_log(stats_file)
        true_data = parse_true_csv(true_file)
        mean.append(stats_data['mean'])
        hdp95lower.append(stats_data['HPD95.lower'])
        hdp95upper.append(stats_data['HPD95.upper'])
        ess.append(stats_data['ESS'])
        true.append(true_data)
    # plot parameters
    for parameter in parameter_list:
        # get values
        # true_values = [x[parameter] for x in true]
        # mean_values = [x[parameter] for x in mean]
        mapped_parameter = parameter_map[parameter]
        true_values = [x[mapped_parameter] for x in true]
        mean_values = [x[parameter] for x in mean]
        lowers = [x[parameter] for x in hdp95lower]
        uppers = [x[parameter] for x in hdp95upper]



        # map colors
        color_list = {True: 'c', False: 'r'}
        colors_boolean = [lowers[i] <= true_values[i] <= uppers[i] for i in range(len(true_values))]
        color_values = [color_list[x] for x in colors_boolean]
        # begin plotting
        plt.clf()
        line_width = 3
        alpha = 0.2
        ax = plt.subplot(111)
        plt.plot(true_values, mean_values, 'k.', ms=2, zorder=2)
        plt.vlines(true_values, ymin=lowers, ymax=uppers, colors=color_values, alpha=alpha, lw=line_width, zorder=1)
        if parameter == "treeheight":
            plt.ylim([0, 1.05])
            plt.xlim([0, 1.05])
            plt.xticks(np.arange(0, 3.1, 1.0))
            plt.yticks(np.arange(0, 3.1, 1.0))
            plt.plot([0, 3], [0, 3], 'k-', lw=0.5, label="x = y", zorder=10)
        elif parameter == "treelength":
            plt.ylim([0, 10.5])
            plt.xlim([0, 10.5])
            plt.xticks(range(0, 11, 2))
            plt.yticks(range(0, 11, 2))
            plt.plot([0, 10], [0, 10], 'k-', lw=0.5, label="x = y", zorder=10)
        else:
            y1 = min(lowers)
            y2 = max(uppers)
            x1 = min(true_values)
            x2 = max(true_values)
            plt.plot([x1, x2], [x1, x2], 'k-', lw=0.5, label="x = y", zorder=10)


        plt.xlabel("True " + parameter_map[parameter])
        plt.ylabel("Estimated " + parameter_map[parameter])
        if parameter.startswith("tree"):
            plt.title(parameter_map[parameter].capitalize())
        else:
            plt.title(parameter_map[parameter])
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        plt.tight_layout()

        within_hpd_count = sum(
            lower <= true_val <= upper for true_val, lower, upper in zip(true_values, lowers, uppers)
        )
        total_count = len(true_values)  # 总计算次数
        coverage_percent = within_hpd_count / total_count * 100  # 计算覆盖率


        plt.text(
            0.05, 0.95,
            f'covg. = {coverage_percent:.0f} %',
            transform=plt.gca().transAxes,
            fontsize=10,
            verticalalignment='top',
            horizontalalignment='left',
            bbox=dict(facecolor='white', alpha=0.5)
        )

        output_path = "/Users/xuyuan/workspace/py/pythonProject1/sim1/figures/" + parameter.lower().replace(".", "_") + ".pdf"
        plt.savefig(output_path)
        print("figure saved: %s" % os.path.abspath(output_path))



# gt16 simulation 3
parameters = ["f0", "NInfinity", "b", "tree.height", "tree.treeLength"]
# stats_format = "../stats/gt16_coal_n16_L200_%d_stats.log"
stats_format = "/Users/xuyuan/workspace/py/pythonProject1/sim1/stats/gompCoal-%d_stats.log"
# true_format = "../data/gt16CoalErrModel_%d_true.log"
true_format = "/Users/xuyuan/workspace/py/pythonProject1/sim1/data/gompCoal-%d.log"
plot_figs(stats_format, true_format, parameters)

