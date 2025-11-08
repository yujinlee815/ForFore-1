# import streamlit as st
# from openai import OpenAI

# # Show title and description.
# st.title("💬 Chatbot")
# st.write(
#     "This is a simple chatbot that uses OpenAI's GPT-3.5 model to generate responses. "
#     "To use this app, you need to provide an OpenAI API key, which you can get [here](https://platform.openai.com/account/api-keys). "
#     "You can also learn how to build this app step by step by [following our tutorial](https://docs.streamlit.io/develop/tutorials/llms/build-conversational-apps)."
# )

# # Ask user for their OpenAI API key via `st.text_input`.
# # Alternatively, you can store the API key in `./.streamlit/secrets.toml` and access it
# # via `st.secrets`, see https://docs.streamlit.io/develop/concepts/connections/secrets-management
# openai_api_key = st.text_input("OpenAI API Key", type="password")
# if not openai_api_key:
#     st.info("Please add your OpenAI API key to continue.", icon="🗝️")
# else:

#     # Create an OpenAI client.
#     client = OpenAI(api_key=openai_api_key)

#     # Create a session state variable to store the chat messages. This ensures that the
#     # messages persist across reruns.
#     if "messages" not in st.session_state:
#         st.session_state.messages = []

#     # Display the existing chat messages via `st.chat_message`.
#     for message in st.session_state.messages:
#         with st.chat_message(message["role"]):
#             st.markdown(message["content"])

#     # Create a chat input field to allow the user to enter a message. This will display
#     # automatically at the bottom of the page.
#     if prompt := st.chat_input("What is up?"):

#         # Store and display the current prompt.
#         st.session_state.messages.append({"role": "user", "content": prompt})
#         with st.chat_message("user"):
#             st.markdown(prompt)

#         # Generate a response using the OpenAI API.
#         stream = client.chat.completions.create(
#             model="gpt-3.5-turbo",
#             messages=[
#                 {"role": m["role"], "content": m["content"]}
#                 for m in st.session_state.messages
#             ],
#             stream=True,
#         )

#         # Stream the response to the chat using `st.write_stream`, then store it in 
#         # session state.
#         with st.chat_message("assistant"):
#             response = st.write_stream(stream)
#         st.session_state.messages.append({"role": "assistant", "content": response})

import streamlit as st
from PIL import Image
import torch
from transformers import AutoProcessor, AutoModelForVision2Seq

# --------------------------
# Basic Configuration
# --------------------------
st.set_page_config(page_title="ForFore Chatbot", page_icon="💬", layout="centered")

# 4-bit is lighter. If you have low GPU VRAM, uncomment the 4-bit version below.
DEFAULT_MODEL_ID = "unsloth/Llama-3.2-11B-Vision-Instruct"
# DEFAULT_MODEL_ID = "unsloth/Llama-3.2-11B-Vision-Instruct-bnb-4bit"  # 4-bit variant

@st.cache_resource(show_spinner=True)
def load_model(model_id: str):
    """Load model and processor once and cache."""
    device = "cuda" if torch.cuda.is_available() else "cpu"
    dtype = torch.float16 if device == "cuda" else torch.float32

    processor = AutoProcessor.from_pretrained(model_id, trust_remote_code=True)
    model = AutoModelForVision2Seq.from_pretrained(
        model_id,
        torch_dtype=dtype,
        device_map="auto",
        trust_remote_code=True,
    )
    return processor, model

def generate_reply(user_text: str, image_file, processor, model, max_new_tokens: int = 256):
    """
    Llama-3.2-Vision requires a chat template.
    When an image is present, create a prompt with {"type": "image"} token,
    then pass it as processor(text=prompt, images=[...]).
    """
    if image_file is not None:
        image = Image.open(image_file).convert("RGB")

        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "image"},                       # ← Image token
                    {"type": "text", "text": user_text},     # ← User question
                ],
            }
        ]
        prompt = processor.apply_chat_template(
            messages, add_generation_prompt=True
        )
        inputs = processor(
            text=prompt,
            images=[image],      # Pass as list
            return_tensors="pt",
            padding=True
        ).to(model.device)

    else:
        # For text-only input, also use chat template
        messages = [
            {"role": "user", "content": [{"type": "text", "text": user_text}]}
        ]
        prompt = processor.apply_chat_template(
            messages, add_generation_prompt=True
        )
        inputs = processor(
            text=prompt,
            return_tensors="pt",
            padding=True
        ).to(model.device)

    with torch.no_grad():
        out_ids = model.generate(**inputs, max_new_tokens=max_new_tokens)

    return processor.batch_decode(out_ids, skip_special_tokens=True)[0].strip()


# --------------------------
# Sidebar (Settings)
# --------------------------
with st.sidebar:
    st.markdown("### ⚙️ Settings")
    model_id = st.text_input("Hugging Face Model ID", value=DEFAULT_MODEL_ID, help="e.g., unsloth/Llama-3.2-11B-Vision-Instruct")
    max_tokens = st.slider("Max New Tokens", min_value=64, max_value=1024, value=256, step=64)
    st.caption("ForFore AI Assistant")

st.title("🤖 ForFore Chatbot 🤖")
st.write("ForFore is an intelligent administrative and life assistant for foreign residents in Korea. Upload images of visas, contracts, or documents to receive easy-to-understand explanations in your native language.")

# New feature announcement
st.info("💡 **New Feature!** Check out the **Jobs** page in the left sidebar! Find employment opportunities tailored for foreign residents.")

# Load model
processor, model = load_model(model_id)

# Chat history state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Render previous conversations
for role, content in st.session_state.messages:
    with st.chat_message(role):
        st.markdown(content)

# Optional image upload
uploaded_image = st.file_uploader("Upload Image (Optional)", type=["png", "jpg", "jpeg"])

# Input field
if user_input := st.chat_input("Type your message here..."):
    # Display and save user message
    st.session_state.messages.append(("user", user_input))
    with st.chat_message("user"):
        st.markdown(user_input)

    # Model response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                reply = generate_reply(user_input, uploaded_image, processor, model, max_new_tokens=max_tokens)
            except Exception as e:
                reply = f"An error occurred: {e}"
            st.markdown(reply)

    st.session_state.messages.append(("assistant", reply))
