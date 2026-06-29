# import streamlit as st
# import os
# from audio_recorder_streamlit import audio_recorder

# # Importing our custom modules
# from audio_handler import transcribe_audio_bytes
# from ai_extractor import extract_invoice_data
# from pdf_generator import generate_invoice_pdf

# # --- UI Configuration ---
# st.set_page_config(page_title="AI Solar Invoice Generator", layout="centered")
# st.title("🎙️ AI Voice-to-Invoice Generator")
# st.write("Speak your solar panel invoice details, and the AI will extract the data to generate a professional PDF.")

# # --- Session State Management ---
# # We use session state to keep data on the screen after button clicks
# if "transcript" not in st.session_state:
#     st.session_state.transcript = None
# if "invoice_data" not in st.session_state:
#     st.session_state.invoice_data = None

# # --- Step 1: Audio Recording ---
# st.header("Step 1: Record Invoice Details")
# st.info("Click the mic icon, speak your details using 'next' as a separator, and click the mic again to stop.")

# # The audio widget
# audio_bytes = audio_recorder(text="Click to Record", pause_threshold=2.0)

# if audio_bytes:
#     st.audio(audio_bytes, format="audio/wav")
    
#     if st.button("Process Audio & Extract Data", type="primary"):
#         # Pipeline Part 1: Audio to Text (Whisper)
#         with st.spinner("Transcribing audio using Whisper AI..."):
#             transcript = transcribe_audio_bytes(audio_bytes)
#             st.session_state.transcript = transcript
            
#         st.success("Transcription Complete!")
#         st.write("**Extracted Text:**", transcript)
        
#         # Pipeline Part 2: Text to JSON (Gemini 2.5 Flash)
#         with st.spinner("Extracting structured data using Gemini AI..."):
#             extracted_data = extract_invoice_data(transcript)
            
#             if "error" in extracted_data:
#                 st.error(extracted_data["error"])
#             else:
#                 st.session_state.invoice_data = extracted_data
#                 st.success("Data Extraction Complete!")

# # --- Step 2: Review and PDF Generation ---
# if st.session_state.invoice_data:
#     st.divider()
#     st.header("Step 2: Review Data & Generate PDF")
    
#     # Display the structured data
#     st.json(st.session_state.invoice_data)
    
#     # Pipeline Part 3: JSON to PDF
#     if st.button("Generate Invoice PDF"):
#         with st.spinner("Generating professional PDF..."):
#             pdf_filename = generate_invoice_pdf(st.session_state.invoice_data)
            
#             if "Error" in pdf_filename:
#                 st.error(pdf_filename)
#             else:
#                 st.success("PDF Generated Successfully!")
                
#                 # Provide a download button for the user
#                 with open(pdf_filename, "rb") as file:
#                     st.download_button(
#                         label="📥 Download Invoice PDF",
#                         data=file,
#                         file_name="Solar_Invoice.pdf",
#                         mime="application/pdf"
#                     )


# import streamlit as st
# import os
# import base64
# from audio_recorder_streamlit import audio_recorder
# from streamlit_mic_recorder import mic_recorder

# # Importing custom modules
# from audio_handler import transcribe_audio_bytes
# from ai_extractor import extract_invoice_data
# from pdf_generator import generate_invoice_pdf

# # --- UI Configuration ---
# st.set_page_config(page_title="AI Solar Invoice Generator", layout="centered")
# st.title("🎙️ AI Voice-to-Invoice Generator")
# st.write("Speak your solar panel invoice details or upload a file.")

# # --- Session State Management ---
# if "invoice_data" not in st.session_state:
#     st.session_state.invoice_data = {
#         "client_name": "", "cnic_number": "", "address": "",
#         "total_panels": 0, "per_panel_price": 0.0,
#         "total_amount": 0.0, "discount": 0.0,
#         "receive_payment": 0.0, "remaining_amount": 0.0
#     }

# # --- Step 1: Input Audio (Mic or Upload) ---
# st.header("Step 1: Input Invoice Details")
# tab1, tab2 = st.tabs(["🎙️ Record Audio", "📁 Upload File"])

# audio_bytes = None

# with tab1:
#     st.info("Click the mic to record. If 'Error' appears, use Upload tab.")
#     rec = audio_recorder(text="Click to Record", key="stable_recorder")
#     if rec:
#         audio_bytes = rec
#         st.audio(audio_bytes, format="audio/wav")

# with tab2:
#     uploaded_file = st.file_uploader("Upload audio file", type=['wav', 'mp3'])
#     if uploaded_file:
#         audio_bytes = uploaded_file.read()

# # --- Processing Pipeline ---
# if audio_bytes:
#     if st.button("Process Audio & Extract Data", type="primary"):
#         if len(audio_bytes) < 5000:
#             st.warning("Recording too short. Please record 3-4 seconds.")
#         else:
#             with st.spinner("Processing..."):
#                 transcript = transcribe_audio_bytes(audio_bytes)
#                 if "System Error" in transcript:
#                     st.error(transcript)
#                 else:
#                     st.success("Transcription Complete!")
#                     data = extract_invoice_data(transcript)
#                     if "error" in data:
#                         st.error(data["error"])
#                     else:
#                         st.session_state.invoice_data = data
#                         st.rerun()

# # --- Step 2: Live Form UI ---
# st.divider()
# st.header("📋 Solar Invoice Form")
# c1, c2 = st.columns(2)

# with c1:
#     client_name = st.text_input("Client Name", value=st.session_state.invoice_data.get("client_name", ""))
#     cnic_number = st.text_input("CNIC Number", value=st.session_state.invoice_data.get("cnic_number", ""))
#     total_panels = st.number_input("Total Panels", value=int(st.session_state.invoice_data.get("total_panels", 0)))
#     discount = st.number_input("Discount Applied (Rs.)", value=float(st.session_state.invoice_data.get("discount", 0.0)))

# with c2:
#     address = st.text_input("Address", value=st.session_state.invoice_data.get("address", ""))
#     per_panel_price = st.number_input("Per Panel Price (Rs.)", value=float(st.session_state.invoice_data.get("per_panel_price", 0.0)))
#     receive_payment = st.number_input("Received Payment (Rs.)", value=float(st.session_state.invoice_data.get("receive_payment", 0.0)))

# # Calculations
# total_amount = total_panels * per_panel_price
# remaining_amount = total_amount - discount - receive_payment
# st.write(f"**Gross Amount:** Rs. {total_amount:,.2f} | **Remaining Balance:** Rs. {remaining_amount:,.2f}")

# updated_data = {
#     "client_name": client_name, "cnic_number": cnic_number, "address": address,
#     "total_panels": total_panels, "per_panel_price": per_panel_price,
#     "total_amount": total_amount, "discount": discount,
#     "receive_payment": receive_payment, "remaining_amount": remaining_amount
# }

# # --- Step 3: PDF Generation ---
# st.divider()
# if st.button("Generate Invoice PDF", type="secondary"):
#     pdf_file = generate_invoice_pdf(updated_data)
#     if "Error" in pdf_file:
#         st.error(pdf_file)
#     else:
#         st.success("PDF Generated!")
#         with open(pdf_file, "rb") as f:
#             b64 = base64.b64encode(f.read()).decode('utf-8')
#             st.markdown(f'<iframe src="data:application/pdf;base64,{b64}" width="100%" height="600"></iframe>', unsafe_allow_html=True)
#             st.download_button("📥 Download PDF", f, "Solar_Invoice.pdf", "application/pdf")



# import streamlit as st
# import os
# import base64
# from streamlit_mic_recorder import mic_recorder

# # Importing custom modules
# from audio_handler import transcribe_audio_bytes
# from ai_extractor import extract_invoice_data
# from pdf_generator import generate_invoice_pdf

# # --- UI Configuration ---
# st.set_page_config(page_title="AI Solar Invoice Generator", layout="centered")
# st.title("🎙️ AI Voice-to-Invoice Generator")

# # --- Session State Initialization ---
# if "invoice_data" not in st.session_state:
#     st.session_state.invoice_data = {
#         "client_name": "", "cnic_number": "", "address": "",
#         "total_panels": 0, "per_panel_price": 0.0,
#         "total_amount": 0.0, "discount": 0.0,
#         "receive_payment": 0.0, "remaining_amount": 0.0
#     }

# # --- Step 1: Input Audio (Mic or Upload) ---
# st.header("Step 1: Get Invoice Details")
# tab1, tab2 = st.tabs(["🎙️ Record Audio", "📁 Upload File"])

# audio_bytes = None

# with tab1:
#     st.info("Click 'Click to Record', speak, then click 'Stop Recording'.")
#     # Naya stable mic recorder
#     audio_data = mic_recorder(start_prompt="Click to Record", stop_prompt="Stop Recording", key='mic_recorder')
#     if audio_data:
#         audio_bytes = audio_data['bytes']
#         st.audio(audio_bytes, format="audio/wav")

# with tab2:
#     uploaded_file = st.file_uploader("Upload audio file", type=['wav', 'mp3'])
#     if uploaded_file:
#         audio_bytes = uploaded_file.read()

# # --- Pipeline ---
# if audio_bytes:
#     if st.button("Process Audio & Extract Data", type="primary"):
#         if len(audio_bytes) < 5000:
#             st.warning("Recording too short. Please try again.")
#         else:
#             with st.spinner("Processing..."):
#                 transcript = transcribe_audio_bytes(audio_bytes)
#                 if "System Error" in transcript:
#                     st.error(transcript)
#                 else:
#                     st.success("Transcription Complete!")
#                     data = extract_invoice_data(transcript)
#                     if "error" in data:
#                         st.error(data["error"])
#                     else:
#                         st.session_state.invoice_data = data
#                         st.rerun()

# # --- Step 2: Live Form ---
# st.divider()
# st.header("📋 Solar Invoice Form")
# c1, c2 = st.columns(2)

# with c1:
#     client_name = st.text_input("Client Name", value=st.session_state.invoice_data.get("client_name", ""))
#     cnic_number = st.text_input("CNIC Number", value=st.session_state.invoice_data.get("cnic_number", ""))
#     total_panels = st.number_input("Total Panels", value=int(st.session_state.invoice_data.get("total_panels", 0)))
#     discount = st.number_input("Discount Applied (Rs.)", value=float(st.session_state.invoice_data.get("discount", 0.0)))

# with c2:
#     address = st.text_input("Address", value=st.session_state.invoice_data.get("address", ""))
#     per_panel_price = st.number_input("Per Panel Price (Rs.)", value=float(st.session_state.invoice_data.get("per_panel_price", 0.0)))
#     receive_payment = st.number_input("Received Payment (Rs.)", value=float(st.session_state.invoice_data.get("receive_payment", 0.0)))

# # Calculations
# total_amount = total_panels * per_panel_price
# remaining_amount = total_amount - discount - receive_payment
# st.write(f"**Gross Amount:** Rs. {total_amount:,.2f} | **Remaining Balance:** Rs. {remaining_amount:,.2f}")

# updated_data = {
#     "client_name": client_name, "cnic_number": cnic_number, "address": address,
#     "total_panels": total_panels, "per_panel_price": per_panel_price,
#     "total_amount": total_amount, "discount": discount,
#     "receive_payment": receive_payment, "remaining_amount": remaining_amount
# }

# # --- Step 3: PDF Generation ---
# st.divider()
# if st.button("Generate Invoice PDF", type="secondary"):
#     pdf_file = generate_invoice_pdf(updated_data)
#     if "Error" in pdf_file:
#         st.error(pdf_file)
#     else:
#         st.success("PDF Generated!")
#         with open(pdf_file, "rb") as f:
#             b64 = base64.b64encode(f.read()).decode('utf-8')
#             st.markdown(f'<iframe src="data:application/pdf;base64,{b64}" width="100%" height="600"></iframe>', unsafe_allow_html=True)
#             st.download_button("📥 Download PDF", f, "Solar_Invoice.pdf", "application/pdf")

# import streamlit as st
# import os
# import base64
# from streamlit_mic_recorder import mic_recorder

# # Importing custom modules
# from audio_handler import transcribe_audio_bytes
# from ai_extractor import extract_invoice_data
# from pdf_generator import generate_invoice_pdf

# # --- UI Configuration ---
# st.set_page_config(page_title="AI Solar Invoice Generator", layout="centered")
# st.title("🎙️ AI Voice-to-Invoice Generator")

# # --- Session State Initialization ---
# if "invoice_data" not in st.session_state:
#     st.session_state.invoice_data = {
#         "client_name": "", "cnic_number": "", "address": "",
#         "total_panels": 0, "per_panel_price": 0.0,
#         "total_amount": 0.0, "discount": 0.0,
#         "receive_payment": 0.0, "remaining_amount": 0.0
#     }

# # --- Step 1: Input Audio ---
# st.header("Step 1: Get Invoice Details")
# tab1, tab2 = st.tabs(["🎙️ Record Audio", "📁 Upload File"])

# audio_bytes = None

# with tab1:
#     st.info("Click 'Click to Record', speak, then click 'Stop Recording'.")
#     audio_data = mic_recorder(start_prompt="Click to Record", stop_prompt="Stop Recording", key='mic_recorder')
    
#     if audio_data and 'bytes' in audio_data:
#         audio_bytes = audio_data['bytes']
#         st.write(f"✅ Audio received! ({len(audio_bytes)} bytes)")
#         st.audio(audio_bytes, format="audio/wav")

# with tab2:
#     uploaded_file = st.file_uploader("Upload audio file", type=['wav', 'mp3'])
#     if uploaded_file:
#         audio_bytes = uploaded_file.read()

# # --- Pipeline ---
# if audio_bytes:
#     if st.button("Process Audio & Extract Data", type="primary"):
#         with st.spinner("Processing..."):
#             transcript = transcribe_audio_bytes(audio_bytes)
            
#             if "System Error" in transcript:
#                 st.error(transcript)
#             else:
#                 st.success(f"Transcript: {transcript}")
#                 data = extract_invoice_data(transcript)
                
#                 if "error" in data:
#                     st.error(data["error"])
#                 else:
#                     st.session_state.invoice_data = data
#                     st.rerun()

# # --- Step 2: Live Form ---
# st.divider()
# st.header("📋 Solar Invoice Form")
# c1, c2 = st.columns(2)

# with c1:
#     client_name = st.text_input("Client Name", value=st.session_state.invoice_data.get("client_name", ""))
#     cnic_number = st.text_input("CNIC Number", value=st.session_state.invoice_data.get("cnic_number", ""))
#     total_panels = st.number_input("Total Panels", value=int(st.session_state.invoice_data.get("total_panels", 0)))
#     discount = st.number_input("Discount Applied (Rs.)", value=float(st.session_state.invoice_data.get("discount", 0.0)))

# with c2:
#     address = st.text_input("Address", value=st.session_state.invoice_data.get("address", ""))
#     per_panel_price = st.number_input("Per Panel Price (Rs.)", value=float(st.session_state.invoice_data.get("per_panel_price", 0.0)))
#     receive_payment = st.number_input("Received Payment (Rs.)", value=float(st.session_state.invoice_data.get("receive_payment", 0.0)))

# # Live Calculations
# total_amount = total_panels * per_panel_price
# remaining_amount = total_amount - discount - receive_payment
# st.write(f"**Gross Amount:** Rs. {total_amount:,.2f} | **Remaining Balance:** Rs. {remaining_amount:,.2f}")

# updated_data = {
#     "client_name": client_name, "cnic_number": cnic_number, "address": address,
#     "total_panels": total_panels, "per_panel_price": per_panel_price,
#     "total_amount": total_amount, "discount": discount,
#     "receive_payment": receive_payment, "remaining_amount": remaining_amount
# }

# # --- Step 3: PDF Generation ---
# st.divider()
# if st.button("Generate Invoice PDF", type="secondary"):
#     pdf_file = generate_invoice_pdf(updated_data)
#     if "Error" in pdf_file:
#         st.error(pdf_file)
#     else:
#         st.success("PDF Generated!")
#         with open(pdf_file, "rb") as f:
#             b64 = base64.b64encode(f.read()).decode('utf-8')
#             st.markdown(f'<iframe src="data:application/pdf;base64,{b64}" width="100%" height="600"></iframe>', unsafe_allow_html=True)
#             st.download_button("📥 Download PDF", f, "Solar_Invoice.pdf", "application/pdf")


# import streamlit as st
# import base64
# from audio_recorder_streamlit import audio_recorder

# from audio_handler import transcribe_audio_bytes
# from ai_extractor import extract_invoice_data
# from pdf_generator import generate_invoice_pdf

# # --- UI Configuration ---
# st.set_page_config(page_title="AI Solar Invoice Generator", layout="centered")
# st.title("🎙️ AI Voice-to-Invoice Generator")
# st.write("Mic icon dabao → bolo → dobara dabao → form khud fill ho jayega!")

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
# st.header("🎙️ Step 1: Voice Record Karo")
# st.info("👇 Mic icon dabao → poora data bolo (next se fields alag karo) → dobara mic icon dabao")

# # audio_recorder: stop karte hi bytes return karta hai automatically
# audio_bytes = audio_recorder(
#     text="",
#     recording_color="#e74c3c",
#     neutral_color="#2c3e50",
#     icon_name="microphone",
#     icon_size="3x",
#     pause_threshold=3.0,   # 3 second silence pe auto stop
#     sample_rate=16000,
# )

# # --- AUTO PROCESSING: mic stop hote hi trigger ---
# if audio_bytes:
#     # Hash se check karo ke ye naya audio hai ya same
#     import hashlib
#     audio_hash = hashlib.md5(audio_bytes).hexdigest()
    
#     if audio_hash != st.session_state.last_audio_hash and len(audio_bytes) > 2000:
#         st.session_state.last_audio_hash = audio_hash
        
#         st.audio(audio_bytes, format="audio/wav")
        
#         # Step A: Whisper → Transcript
#         with st.spinner("🎧 Whisper AI sun raha hai..."):
#             transcript = transcribe_audio_bytes(audio_bytes)
        
#         if "Error" in transcript or "System Error" in transcript:
#             st.error(f"❌ Transcription fail hui: {transcript}")
#         else:
#             st.session_state.transcript = transcript
#             st.success(f"✅ Transcription: **{transcript}**")
            
#             # Step B: Gemini → Form Data
#             with st.spinner("🤖 AI form fill kar raha hai..."):
#                 data = extract_invoice_data(transcript)
            
#             if "error" in data:
#                 st.error(f"❌ AI Error: {data['error']}")
#             else:
#                 st.session_state.invoice_data = data
#                 st.balloons()
#                 st.success("✅ Form fill ho gaya!")

# # Last transcript dikhao
# if st.session_state.transcript:
#     st.caption(f"🗣️ Last transcript: {st.session_state.transcript}")

# # --- Step 2: Invoice Form ---
# st.divider()
# st.header("📋 Solar Invoice Form")
# st.caption("Voice se fill hoga — manually bhi edit kar sakte ho")

# c1, c2 = st.columns(2)

# with c1:
#     client_name = st.text_input("👤 Client Name",
#         value=st.session_state.invoice_data.get("client_name", ""))
#     cnic_number = st.text_input("🪪 CNIC Number",
#         value=st.session_state.invoice_data.get("cnic_number", ""))
#     total_panels = st.number_input("🔆 Total Panels", min_value=0,
#         value=int(st.session_state.invoice_data.get("total_panels", 0)))
#     discount = st.number_input("🏷️ Discount (Rs.)", min_value=0.0,
#         value=float(st.session_state.invoice_data.get("discount", 0.0)))

# with c2:
#     address = st.text_input("🏠 Address",
#         value=st.session_state.invoice_data.get("address", ""))
#     per_panel_price = st.number_input("💲 Per Panel Price (Rs.)", min_value=0.0,
#         value=float(st.session_state.invoice_data.get("per_panel_price", 0.0)))
#     receive_payment = st.number_input("💵 Received Payment (Rs.)", min_value=0.0,
#         value=float(st.session_state.invoice_data.get("receive_payment", 0.0)))

# # Auto calculations
# total_amount = total_panels * per_panel_price
# remaining_amount = total_amount - discount - receive_payment
# st.info(f"💰 **Gross Amount:** Rs. {total_amount:,.0f}  |  ⏳ **Remaining:** Rs. {remaining_amount:,.0f}")

# updated_data = {
#     "client_name": client_name, "cnic_number": cnic_number,
#     "address": address, "total_panels": total_panels,
#     "per_panel_price": per_panel_price, "total_amount": total_amount,
#     "discount": discount, "receive_payment": receive_payment,
#     "remaining_amount": remaining_amount
# }

# # --- Step 3: PDF ---
# st.divider()
# st.header("📄 Invoice PDF Generate Karo")

# if st.button("🖨️ Generate PDF", type="primary", use_container_width=True):
#     if not client_name:
#         st.warning("⚠️ Pehle voice se ya manually form fill karo.")
#     else:
#         with st.spinner("PDF ban rahi hai..."):
#             pdf_file = generate_invoice_pdf(updated_data)

#         if "Error" in pdf_file:
#             st.error(pdf_file)
#         else:
#             st.success("✅ PDF ready!")
#             with open(pdf_file, "rb") as f:
#                 pdf_bytes = f.read()
#             b64 = base64.b64encode(pdf_bytes).decode()
#             st.markdown(
#                 f'<iframe src="data:application/pdf;base64,{b64}" width="100%" height="600"></iframe>',
#                 unsafe_allow_html=True
#             )
#             st.download_button("📥 Download PDF", pdf_bytes, "Solar_Invoice.pdf", "application/pdf")

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
# st.write("Mic icon dabao → bolo → dobara dabao → form khud fill ho jayega!")

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
# st.header("🎙️ Step 1: Voice Record Karo")
# st.info("👇 Mic icon dabao → poora data bolo (next se fields alag karo) → dobara mic icon dabao")

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
#         with st.spinner("🎧 Whisper AI sun raha hai..."):
#             transcript = transcribe_audio_bytes(audio_bytes)

#         if "Error" in transcript or "System Error" in transcript:
#             st.error(f"❌ Transcription fail: {transcript}")
#         else:
#             st.session_state.transcript = transcript
#             st.success(f"✅ Transcription: **{transcript}**")

#             # Step B: Gemini → Form Data
#             with st.spinner("🤖 AI form fill kar raha hai..."):
#                 data = extract_invoice_data(transcript)

#             if "error" in data:
#                 st.error(f"❌ AI Error: {data['error']}")
#             else:
#                 # None values ko safe defaults se replace karo
#                 st.session_state.invoice_data = {
#                     "client_name":    safe_str(data.get("client_name")),
#                     "cnic_number":    safe_str(data.get("cnic_number")),
#                     "address":        safe_str(data.get("address")),
#                     "total_panels":   safe_int(data.get("total_panels")),
#                     "per_panel_price":safe_float(data.get("per_panel_price")),
#                     "total_amount":   safe_float(data.get("total_amount")),
#                     "discount":       safe_float(data.get("discount")),        # ye None aa raha tha
#                     "receive_payment":safe_float(data.get("receive_payment")),
#                     "remaining_amount":safe_float(data.get("remaining_amount")),
#                 }
#                 st.balloons()
#                 st.success("✅ Form fill ho gaya!")

# if st.session_state.transcript:
#     st.caption(f"🗣️ Last transcript: {st.session_state.transcript}")

# # --- Step 2: Invoice Form ---
# st.divider()
# st.header("📋 Solar Invoice Form")
# st.caption("Voice se fill hoga — manually bhi edit kar sakte ho")

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
# st.info(f"💰 **Gross Amount:** Rs. {total_amount:,.0f}  |  ⏳ **Remaining:** Rs. {remaining_amount:,.0f}")

# updated_data = {
#     "client_name": client_name, "cnic_number": cnic_number,
#     "address": address, "total_panels": total_panels,
#     "per_panel_price": per_panel_price, "total_amount": total_amount,
#     "discount": discount, "receive_payment": receive_payment,
#     "remaining_amount": remaining_amount
# }

# # --- Step 3: PDF ---
# st.divider()
# st.header("📄 Invoice PDF Generate Karo")

# if st.button("🖨️ Generate PDF", type="primary", use_container_width=True):
#     if not client_name:
#         st.warning("⚠️ ")
#     else:
#         with st.spinner("PDF ban rahi hai..."):
#             pdf_file = generate_invoice_pdf(updated_data)

#         if "Error" in pdf_file:
#             st.error(pdf_file)
#         else:
#             st.success("✅ PDF ready!")
#             with open(pdf_file, "rb") as f:
#                 pdf_bytes = f.read()
#             b64 = base64.b64encode(pdf_bytes).decode()
#             st.markdown(
#                 f'<iframe src="data:application/pdf;base64,{b64}" width="100%" height="600"></iframe>',
#                 unsafe_allow_html=True
#             )
#             st.download_button("📥 Download PDF", pdf_bytes, "Solar_Invoice.pdf", "application/pdf")


import streamlit as st
import base64
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
            b64 = base64.b64encode(pdf_bytes).decode()
            st.markdown(
                f'<iframe src="data:application/pdf;base64,{b64}" width="100%" height="600"></iframe>',
                unsafe_allow_html=True
            )
            st.download_button("📥 Download PDF", pdf_bytes, "Solar_Invoice.pdf", "application/pdf")
