import matplotlib.pyplot as plt

# Your data
labels = ['SELECT', 'UPDATE', 'DELETE', 'CREATE VIEW']
values = [50, 25, 15, 10]

# Muted colors
colors = ['#7A9CC6', '#D9A25C', '#8FAE8B', '#C97B7B']

fig, ax = plt.subplots(figsize=(8, 8))
wedges, texts, autotexts = ax.pie(
    values,
    labels=labels,
    autopct='%1.1f%%',
    startangle=90,
    colors=colors,
    wedgeprops={'edgecolor': 'white', 'linewidth': 1},
    textprops={'fontsize': 16}       # font size for labels
)

# Make the percentage numbers bigger/bolder too
for autotext in autotexts:
    autotext.set_fontsize(16)
    autotext.set_color('white')
    autotext.set_fontweight('bold')

ax.axis('equal')

plt.tight_layout()
plt.savefig('pie_chart.png', dpi=200)
plt.show()