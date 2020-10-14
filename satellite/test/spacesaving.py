import matplotlib.pyplot as plt

plt.clf()
figure = plt.gcf()  # get current figure
figure.set_size_inches(18, 10)


def plot_settings():
    plt.legend()
    plt.xticks(fontsize=18)
    plt.yticks(fontsize=18)
    plt.title(f"Space Saving vs Block (buffer) size", fontsize = 24)
    plt.ylabel("Space Saving (%)", fontsize = 22)
    plt.xlabel("Block size", fontsize = 22)

plot_settings()
plt.savefig('spacesavingtemplate.png', dpi = 200)