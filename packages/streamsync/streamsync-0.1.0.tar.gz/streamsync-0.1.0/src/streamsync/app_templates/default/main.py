import streamsync as ss

print("Hello world! You'll see this message in the log")
print("If you edit the file somewhere else, for example, in VS Code, the code will reload automatically. Including dependencies!")


def increment(state):
    state["counter"] += 1
    print("you got to increment")


ss.init_state({
    "message": "Hello",
    "counter": 12,
})
