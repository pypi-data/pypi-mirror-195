import altair as alt
import streamsync as myfavframework
import pandas as pd
from handlers import increment

import matplotlib.pyplot as plt

fig, ax = plt.subplots()

fruits = ['apple', 'blueberry', 'cherry', 'orange']
counts = [40, 100, 30, 55]
bar_labels = ['red', 'blue', '_red', 'orange']
bar_colors = ['tab:red', 'tab:blue', 'tab:red', 'tab:orange']

ax.bar(fruits, counts, label=bar_labels, color=bar_colors)

ax.set_ylabel('fruit supply')
ax.set_title('Fruit supply by kind and color')
ax.legend(title='Fruit color')

data = pd.DataFrame({'a': list('CCCDDDEEE'),
                     'b': [10, 7, 4, 1, 2, 6, 8, 4, 1]})
chart = alt.Chart(data).mark_bar().encode(
    x='a',
    y='average(b)'
)

print("Hello world! You'll see this message in the log")
print("If you edit the file somewhere else, for example, in VS Code, the code will reload automatically. Including dependencies!")

# def increment(state):
#     state["counter"] += 1
#     print("you got to increment")


colored = []
for i in range(20):
    colored.append({"hue": i*10, "name": f"Card {i}"})

myfavframework.init_state({
    "message": "A decent app for testing Streamsync",
    "counter": 12,
    "selected_option": "",
    "data": data,
    "chart": chart,
    "fig": fig,
    "options": {
        "d": "Dududu",
        "e": "Eueueu",
        "f": "Fafafufu"
    },
    "image_column_visible": True
})


def toggle_image_column(state):
    state["image_column_visible"] = not state["image_column_visible"]

def very_long_name_toggle_image_column(state):
    state["image_column_visible"] = not state["image_column_visible"]


def go_to_primary(state):
    state.change_page("primary")


def go_to_secondary(state):
    state.change_page("secondary")


def print_option(state, payload):
    print("Printing payload")
    print(payload)
    state["selected_option"] = payload


def print_context(state, context):
    print(context)
    print(context["cardId"])

def handle_click():
	print("hi")
