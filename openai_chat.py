import openai

openai.api_key = "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"
message_history = []


def chat(inp, role="user"):
    message_history.append({"role": role, "content": f"{inp}"})
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=message_history
    )
    reply_content = completion.choices[0].message.content
    message_history.append({"role": "assistant", "content": f"{reply_content}"})
    return reply_content


for i in range(10):
    user_input = input("> ")
    print("User's input was: ", user_input)
    print(chat(user_input))
    print()
