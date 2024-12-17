import matplotlib.pyplot as plt
from re_loss import get_loss


plt.rcParams.update({'font.size': 18})

def draw_plot(loss, eval_loss, title, step=1):
    epoch = range(1, len(loss) + 1, step)

    plt.title(title, fontsize="x-large")

    plt.ylabel("Loss", fontsize="large")
    plt.xlabel("Epoch", fontsize="large")
    plt.plot(epoch, loss[::step], color='red', marker='o', markersize=5, label="train_loss")
    plt.plot(epoch, eval_loss[::step], color='green', marker='o', markersize=5, label="val_loss")

    plt.legend(loc='upper right')

    stepx = 1/(len(loss)*len(loss))
    plt.xlim(1-stepx, len(loss)+stepx)

    step_y = (max(loss+eval_loss) - min(loss+eval_loss))/len(loss)

    plt.ylim(min(loss+eval_loss) - step_y, max(loss+eval_loss) + step_y)
    plt.margins(1)

    plt.xticks(epoch)

    index_smallest = eval_loss.index(min(eval_loss)) + 1

    substep_y = 0

    plt.plot(index_smallest, min(eval_loss), "black", marker="o", markersize=6)
    # plt.text(index_smallest, min(eval_loss) + substep_y, min(eval_loss), fontsize="large")

    print(min(eval_loss))
    plt.plot(index_smallest, loss[index_smallest - 1], "black", marker="o", markersize=6)
    # plt.text(index_smallest, loss[index_smallest - 1] + substep_y + step_y, loss[index_smallest - 1], fontsize="large")

    print(loss[index_smallest - 1])

    plt.show()

train_rut5_small, valid_rut5_small = get_loss("data/fredt5.txt")
draw_plot(train_rut5_small, valid_rut5_small, "FRED-T5-large")
