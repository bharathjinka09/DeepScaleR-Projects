import gradio as gr
import ollama

# Function to interact with the Deepscaler chatbot
def format_previous_responses(responses):
	if not responses:
		return "_No previous responses yet._"
	return "\n\n".join(f"{index}. {response}" for index, response in enumerate(responses, start=1))

def chat_with_bot(user_message, previous_responses):
	if not user_message.strip():
		yield "", "", previous_responses, format_previous_responses(previous_responses)
		return

	yield "", f"**You asked:** {user_message}\n\n**Response:** _Generating..._", previous_responses, format_previous_responses(previous_responses)
	response = ollama.chat(
		model='deepscaler-chat',
		messages=[{"role": "user", "content": user_message}],
		stream=True,
	)
	content = ""
	for chunk in response:
		content += chunk.message.content
		yield "", f"**You asked:** {user_message}\n\n**Response:**\n\n{content}", previous_responses, format_previous_responses(previous_responses)

	if content:
		previous_responses = [*previous_responses, content]
		yield "", f"**You asked:** {user_message}\n\n**Response:**\n\n{content}", previous_responses, format_previous_responses(previous_responses)

with gr.Blocks(title="AI-Chatbot using DeepScaler") as chatbot_ui:
	gr.Markdown("# AI-Chatbot using DeepScaler")
	message = gr.Textbox(label="Chat Message")
	send = gr.Button("Send")
	response = gr.Markdown(label="Bot Response")
	gr.Markdown("### Previous responses")
	previous_responses = gr.State([])
	previous_response_list = gr.Markdown("_No previous responses yet._")
	message.submit(chat_with_bot, inputs=[message, previous_responses], outputs=[message, response, previous_responses, previous_response_list])
	send.click(chat_with_bot, inputs=[message, previous_responses], outputs=[message, response, previous_responses, previous_response_list])

if __name__ == "__main__":
	chatbot_ui.launch(pwa=True, share=True)
