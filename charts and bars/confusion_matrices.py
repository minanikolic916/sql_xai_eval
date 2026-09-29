import numpy as np
import matplotlib.pyplot as plt

labels = ["correct", "incorrect_syntax", "incorrect_semantic"]
cm = [
    [16, 4, 0],
    [1, 33, 6],
    [4, 3, 33]
]

fig, ax = plt.subplots()
ax.imshow(cm, cmap="Blues")

ax.set_xticks(range(len(labels)))
ax.set_yticks(range(len(labels)))
#ax.set_xticklabels(labels)
ax.set_xticklabels(labels, fontsize=9)
ax.set_yticklabels(labels, fontsize=9)

ax.xaxis.set_ticks_position("top")
ax.xaxis.set_label_position("top")
ax.set_xlabel("Large language model (DeepSeek-coder-v2-16b)", labelpad=15)
ax.set_ylabel("Human")

threshold = np.max(cm) / 2  

for i in range(len(labels)):
    for j in range(len(labels)):
        color = "white" if cm[i][j] > threshold else "black"
        ax.text(j, i, cm[i][j], ha="center", va="center", color=color)

plt.colorbar(ax.images[0])

plt.savefig("confusion_matrix.png", dpi=300, bbox_inches="tight")
#plt.show()