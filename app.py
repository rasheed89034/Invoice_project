# import streamlit as st
# import base64
# import hashlib
# from audio_recorder_streamlit import audio_recorder

# from audio_handler import transcribe_audio_bytes
# from ai_extractor import extract_invoice_data
# from pdf_generator import generate_invoice_pdf

# # --- Helper: None-safe conversions ---
# def safe_float(val, default=0.0):
#     try:
#         return float(val) if val is not None else default
#     except (ValueError, TypeError):
#         return default

# def safe_int(val, default=0):
#     try:
#         return int(val) if val is not None else default
#     except (ValueError, TypeError):
#         return default

# def safe_str(val, default=""):
#     return str(val) if val is not None else default

# # --- UI Configuration ---
# st.set_page_config(page_title="AI Solar Invoice Generator", layout="centered")
# st.title("🎙️ AI Voice-to-Invoice Generator")
# st.write("Click the mic → speak your details → click again → form fills automatically!")

# # --- Session State ---
# if "invoice_data" not in st.session_state:
#     st.session_state.invoice_data = {
#         "client_name": "", "cnic_number": "", "address": "",
#         "total_panels": 0, "per_panel_price": 0.0,
#         "total_amount": 0.0, "discount": 0.0,
#         "receive_payment": 0.0, "remaining_amount": 0.0
#     }
# if "last_audio_hash" not in st.session_state:
#     st.session_state.last_audio_hash = None
# if "transcript" not in st.session_state:
#     st.session_state.transcript = ""

# # --- Step 1: Record Audio ---
# st.header("🎙️ Step 1: Record Your Voice")
# st.info("Click the mic icon → speak all details (use 'next' between fields) → click mic again to stop.")

# audio_bytes = audio_recorder(
#     text="",
#     recording_color="#e74c3c",
#     neutral_color="#2c3e50",
#     icon_name="microphone",
#     icon_size="3x",
#     pause_threshold=3.0,
#     sample_rate=16000,
# )

# # --- AUTO PROCESSING ---
# if audio_bytes:
#     audio_hash = hashlib.md5(audio_bytes).hexdigest()

#     if audio_hash != st.session_state.last_audio_hash and len(audio_bytes) > 2000:
#         st.session_state.last_audio_hash = audio_hash

#         st.audio(audio_bytes, format="audio/wav")

#         # Step A: Whisper → Transcript
#         with st.spinner("🎧 Transcribing audio..."):
#             transcript = transcribe_audio_bytes(audio_bytes)

#         if "Error" in transcript or "System Error" in transcript:
#             st.error(f"❌ Transcription failed: {transcript}")
#         else:
#             st.session_state.transcript = transcript
#             st.success(f"✅ Transcript: **{transcript}**")

#             # Step B: Gemini → Form Data
#             with st.spinner("🤖 Extracting data and filling form..."):
#                 data = extract_invoice_data(transcript)

#             if "error" in data:
#                 st.error(f"❌ AI Extraction Error: {data['error']}")
#             else:
#                 st.session_state.invoice_data = {
#                     "client_name":     safe_str(data.get("client_name")),
#                     "cnic_number":     safe_str(data.get("cnic_number")),
#                     "address":         safe_str(data.get("address")),
#                     "total_panels":    safe_int(data.get("total_panels")),
#                     "per_panel_price": safe_float(data.get("per_panel_price")),
#                     "total_amount":    safe_float(data.get("total_amount")),
#                     "discount":        safe_float(data.get("discount")),
#                     "receive_payment": safe_float(data.get("receive_payment")),
#                     "remaining_amount":safe_float(data.get("remaining_amount")),
#                 }
#                 st.success("✅ Form filled successfully!")

# if st.session_state.transcript:
#     st.caption(f"🗣️ Last transcript: {st.session_state.transcript}")

# # --- Step 2: Invoice Form ---
# st.divider()
# st.header("📋 Solar Invoice Form")
# st.caption("Auto-filled from voice — you can also edit manually.")

# c1, c2 = st.columns(2)

# with c1:
#     client_name = st.text_input("👤 Client Name",
#         value=safe_str(st.session_state.invoice_data.get("client_name")))
#     cnic_number = st.text_input("🪪 CNIC Number",
#         value=safe_str(st.session_state.invoice_data.get("cnic_number")))
#     total_panels = st.number_input("🔆 Total Panels", min_value=0,
#         value=safe_int(st.session_state.invoice_data.get("total_panels")))
#     discount = st.number_input("🏷️ Discount (Rs.)", min_value=0.0,
#         value=safe_float(st.session_state.invoice_data.get("discount")))

# with c2:
#     address = st.text_input("🏠 Address",
#         value=safe_str(st.session_state.invoice_data.get("address")))
#     per_panel_price = st.number_input("💲 Per Panel Price (Rs.)", min_value=0.0,
#         value=safe_float(st.session_state.invoice_data.get("per_panel_price")))
#     receive_payment = st.number_input("💵 Received Payment (Rs.)", min_value=0.0,
#         value=safe_float(st.session_state.invoice_data.get("receive_payment")))

# # Auto calculations
# total_amount = total_panels * per_panel_price
# remaining_amount = total_amount - discount - receive_payment
# st.info(f"💰 **Gross Amount:** Rs. {total_amount:,.0f}  |  ⏳ **Remaining Balance:** Rs. {remaining_amount:,.0f}")

# updated_data = {
#     "client_name": client_name, "cnic_number": cnic_number,
#     "address": address, "total_panels": total_panels,
#     "per_panel_price": per_panel_price, "total_amount": total_amount,
#     "discount": discount, "receive_payment": receive_payment,
#     "remaining_amount": remaining_amount
# }

# # --- Step 3: PDF ---
# st.divider()
# st.header("📄 Generate Invoice PDF")

# if st.button("🖨️ Generate PDF", type="primary", use_container_width=True):
#     if not client_name:
#         st.warning("⚠️ Please fill the form first via voice or manually.")
#     else:
#         with st.spinner("Generating PDF..."):
#             pdf_file = generate_invoice_pdf(updated_data)

#         if "Error" in pdf_file:
#             st.error(pdf_file)
#         else:
#             st.success("✅ PDF generated successfully!")
#             with open(pdf_file, "rb") as f:
#                 pdf_bytes = f.read()
#             b64 = base64.b64encode(pdf_bytes).decode()
#             st.markdown(
#                 f'<iframe src="data:application/pdf;base64,{b64}" width="100%" height="600"></iframe>',
#                 unsafe_allow_html=True
#             )
#             st.download_button("📥 Download PDF", pdf_bytes, "Solar_Invoice.pdf", "application/pdf")


import streamlit as st
import hashlib
from audio_recorder_streamlit import audio_recorder

from audio_handler import transcribe_audio_bytes
from ai_extractor import extract_invoice_data
from pdf_generator import generate_invoice_pdf

# --- Helper: None-safe conversions ---
def safe_float(val, default=0.0):
    try:
        return float(val) if val is not None else default
    except (ValueError, TypeError):
        return default

def safe_int(val, default=0):
    try:
        return int(val) if val is not None else default
    except (ValueError, TypeError):
        return default

def safe_str(val, default=""):
    return str(val) if val is not None else default

# --- UI Configuration ---
st.set_page_config(page_title="AI Solar Invoice Generator", layout="centered")
st.title("🎙️ AI Voice-to-Invoice Generator")
st.write("Click the mic → speak your details → click again → form fills automatically!")

# --- Session State ---
if "invoice_data" not in st.session_state:
    st.session_state.invoice_data = {
        "client_name": "", "cnic_number": "", "address": "",
        "total_panels": 0, "per_panel_price": 0.0,
        "total_amount": 0.0, "discount": 0.0,
        "receive_payment": 0.0, "remaining_amount": 0.0
    }
if "last_audio_hash" not in st.session_state:
    st.session_state.last_audio_hash = None
if "transcript" not in st.session_state:
    st.session_state.transcript = ""

# --- Step 1: Record Audio ---
st.header("🎙️ Step 1: Record Your Voice")
st.info("Click the mic icon → speak all details (use 'next' between fields) → click mic again to stop.")

audio_bytes = audio_recorder(
    text="",
    recording_color="#e74c3c",
    neutral_color="#2c3e50",
    icon_name="microphone",
    icon_size="3x",
    pause_threshold=3.0,
    sample_rate=16000,
)

# --- AUTO PROCESSING ---
if audio_bytes:
    audio_hash = hashlib.md5(audio_bytes).hexdigest()

    if audio_hash != st.session_state.last_audio_hash and len(audio_bytes) > 2000:
        st.session_state.last_audio_hash = audio_hash

        st.audio(audio_bytes, format="audio/wav")

        # Step A: Whisper → Transcript
        with st.spinner("🎧 Transcribing audio..."):
            transcript = transcribe_audio_bytes(audio_bytes)

        if "Error" in transcript or "System Error" in transcript:
            st.error(f"❌ Transcription failed: {transcript}")
        else:
            st.session_state.transcript = transcript
            st.success(f"✅ Transcript: **{transcript}**")

            # Step B: Gemini → Form Data
            with st.spinner("🤖 Extracting data and filling form..."):
                data = extract_invoice_data(transcript)

            if "error" in data:
                st.error(f"❌ AI Extraction Error: {data['error']}")
            else:
                st.session_state.invoice_data = {
                    "client_name":     safe_str(data.get("client_name")),
                    "cnic_number":     safe_str(data.get("cnic_number")),
                    "address":         safe_str(data.get("address")),
                    "total_panels":    safe_int(data.get("total_panels")),
                    "per_panel_price": safe_float(data.get("per_panel_price")),
                    "total_amount":    safe_float(data.get("total_amount")),
                    "discount":        safe_float(data.get("discount")),
                    "receive_payment": safe_float(data.get("receive_payment")),
                    "remaining_amount":safe_float(data.get("remaining_amount")),
                }
                st.success("✅ Form filled successfully!")

if st.session_state.transcript:
    st.caption(f"🗣️ Last transcript: {st.session_state.transcript}")

# --- Step 2: Invoice Form ---
st.divider()
st.header("📋 Solar Invoice Form")
st.caption("Auto-filled from voice — you can also edit manually.")

c1, c2 = st.columns(2)

with c1:
    client_name = st.text_input("👤 Client Name",
        value=safe_str(st.session_state.invoice_data.get("client_name")))
    cnic_number = st.text_input("🪪 CNIC Number",
        value=safe_str(st.session_state.invoice_data.get("cnic_number")))
    total_panels = st.number_input("🔆 Total Panels", min_value=0,
        value=safe_int(st.session_state.invoice_data.get("total_panels")))
    discount = st.number_input("🏷️ Discount (Rs.)", min_value=0.0,
        value=safe_float(st.session_state.invoice_data.get("discount")))

with c2:
    address = st.text_input("🏠 Address",
        value=safe_str(st.session_state.invoice_data.get("address")))
    per_panel_price = st.number_input("💲 Per Panel Price (Rs.)", min_value=0.0,
        value=safe_float(st.session_state.invoice_data.get("per_panel_price")))
    receive_payment = st.number_input("💵 Received Payment (Rs.)", min_value=0.0,
        value=safe_float(st.session_state.invoice_data.get("receive_payment")))

# Auto calculations
total_amount = total_panels * per_panel_price
remaining_amount = total_amount - discount - receive_payment
st.info(f"💰 **Gross Amount:** Rs. {total_amount:,.0f}  |  ⏳ **Remaining Balance:** Rs. {remaining_amount:,.0f}")

updated_data = {
    "client_name": client_name, "cnic_number": cnic_number,
    "address": address, "total_panels": total_panels,
    "per_panel_price": per_panel_price, "total_amount": total_amount,
    "discount": discount, "receive_payment": receive_payment,
    "remaining_amount": remaining_amount
}

# --- Step 3: PDF ---
st.divider()
st.header("📄 Generate Invoice PDF")

if st.button("🖨️ Generate PDF", type="primary", use_container_width=True):
    if not client_name:
        st.warning("⚠️ Please fill the form first via voice or manually.")
    else:
        with st.spinner("Generating PDF..."):
            pdf_file = generate_invoice_pdf(updated_data)

        if "Error" in pdf_file:
            st.error(pdf_file)
        else:
            st.success("✅ PDF generated successfully!")
            with open(pdf_file, "rb") as f:
                pdf_bytes = f.read()
            st.download_button(
                label="📥 Download PDF",
                data=pdf_bytes,
                file_name="Solar_Invoice.pdf",
                mime="application/pdf",
                use_container_width=True
            )

