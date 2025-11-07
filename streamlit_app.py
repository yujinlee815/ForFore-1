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
# 기본 설정
# --------------------------
st.set_page_config(page_title="Llama 3.2 Vision Chatbot", page_icon="💬", layout="centered")

# 4-bit이 더 가벼움. GPU VRAM 적으면 아래 4bit 주석을 풀고 쓰세요.
DEFAULT_MODEL_ID = "unsloth/Llama-3.2-11B-Vision-Instruct"
# DEFAULT_MODEL_ID = "unsloth/Llama-3.2-11B-Vision-Instruct-bnb-4bit"  # 4-bit 변형(이름은 환경에 따라 약간 다를 수 있음)

@st.cache_resource(show_spinner=True)
def load_model(model_id: str):
    """모델/프로세서를 1회만 로드해서 캐시."""
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
    Llama-3.2-Vision은 chat template이 필요함.
    이미지가 있을 땐 {"type": "image"} 토큰을 포함한 메시지로 prompt를 만든 뒤,
    processor(text=prompt, images=[...]) 형태로 전달해야 함.
    """
    if image_file is not None:
        image = Image.open(image_file).convert("RGB")

        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "image"},                       # ← 이미지 토큰
                    {"type": "text", "text": user_text},     # ← 사용자 질문
                ],
            }
        ]
        prompt = processor.apply_chat_template(
            messages, add_generation_prompt=True
        )
        inputs = processor(
            text=prompt,
            images=[image],      # 리스트로 전달
            return_tensors="pt",
            padding=True
        ).to(model.device)

    else:
        # 텍스트만 있을 때도 chat template을 사용
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
# 사이드바 (설정)
# --------------------------
with st.sidebar:
    st.markdown("### ⚙️ Settings")
    model_id = st.text_input("Hugging Face 모델 ID", value=DEFAULT_MODEL_ID, help="예) unsloth/Llama-3.2-11B-Vision-Instruct")
    max_tokens = st.slider("max_new_tokens", min_value=64, max_value=1024, value=256, step=64)
    st.caption("소박이")

st.title("🤖 ForFore Chatbot 🤖")
st.write("ForFore은 한국에 거주하는 외국인 주민을 위한 지능형 행정·생활 도우미입니다. 비자, 계약서, 생활문서 등 이미지를 올리면 내용을 분석해 사용자의 모국어로 이해하기 쉬운 설명과 안내를 제공합니다.")

# 모델 로드
processor, model = load_model(model_id)

# 채팅 기록 상태
if "messages" not in st.session_state:
    st.session_state.messages = []

# 이전 대화 렌더링
for role, content in st.session_state.messages:
    with st.chat_message(role):
        st.markdown(content)

# 선택 이미지 업로드
uploaded_image = st.file_uploader("이미지(선택)", type=["png", "jpg", "jpeg"])

# 입력창
if user_input := st.chat_input("메시지를 입력하세요"):
    # 사용자 메시지 출력/저장
    st.session_state.messages.append(("user", user_input))
    with st.chat_message("user"):
        st.markdown(user_input)

    # 모델 응답
    with st.chat_message("assistant"):
        with st.spinner("생각 중..."):
            try:
                reply = generate_reply(user_input, uploaded_image, processor, model, max_new_tokens=max_tokens)
            except Exception as e:
                reply = f"오류가 발생했어요: {e}"
            st.markdown(reply)

    st.session_state.messages.append(("assistant", reply))
