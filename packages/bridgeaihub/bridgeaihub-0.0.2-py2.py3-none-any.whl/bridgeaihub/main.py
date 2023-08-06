import streamlit as st
from transformers import pipeline, GPT2Tokenizer




MODEL = 'gpt2'
DEFAULT_NUM_CHARS = 200


# Load the model
def get_model():
    with st.spinner('Loading the Model...'):
        model = pipeline('text-generation', model=MODEL)

    return model

# Tokenize the text
def tokenize_text(input: str):
    tokenizer = GPT2Tokenizer.from_pretrained(MODEL)
    encoded_input = tokenizer(input, return_tensors='tf')
    
    return encoded_input

# Generate output text
def generate_text(model, input: str, n_char: int):
    
    # set_seed(42)  # for reproducibility
    result = model(input, max_length=n_char)
    gen_text = result[0]['generated_text']
    
    return gen_text

# Set page title and configurations
def set_title(title: str):
    st.set_page_config(page_title=title)
    st.title(title)
    
# Render input section
def get_inputs():
    st.write('##')
    input_text = st.text_input('Input Text:',)
    validate_input_text = st.empty()
    
    # Finding out minimum number of characters needed
    encoded_input = tokenize_text(input_text)
    cols = encoded_input['input_ids'].shape[1]        # Number of columns of tokenized tensor
    
    col, buff = st.columns([1,2])
    with col:
        n_char = st.number_input('Number of characters needed:', min_value=cols, step=1, value=DEFAULT_NUM_CHARS,
                                 help='Input must be greater than ' + str(cols))
    validate_n_char = st.empty()
    
    # Hide -/+ buttons in number input
    st.markdown("""
                <style>
                    button.step-up {display: none;}
                    button.step-down {display: none;}
                    div[data-baseweb] {border-radius: 4px;}
                </style>""",
                unsafe_allow_html=True)
    
    return input_text, n_char, cols, validate_input_text, validate_n_char

# Create output section
def render_output(model, input_text, validate_input_text, validate_n_char, n_char, cols):
    output = st.empty()
    
    if st.button('Generate Text', ):
        if input_text == '' or input_text is None:
            validate_input_text.warning("I can't generate output without any input text !!!")
            
        elif n_char is None:
            validate_n_char.warning('Please provide number of characters needed!!!')
            
        elif n_char <= cols:
            validate_n_char.warning(f'Number of characters must be greater than {cols}!!!')
            
        else:
            try:
                output.text('Generating Text...Please wait...')
                gen_text = generate_text(model, input_text, n_char)
                output.text_area('Output', gen_text, height=200)
                
            except Exception as e:
                st.write('An Error has occurred!!!')
                st.error(e)


# Create Streamlit application
def load_template():
    
    # Page configurations
    set_title("Bridge GPT")
    
    # Collecting input text and number of characters
    input_text, n_char, cols, validate_input_text, validate_n_char = get_inputs()
    
    gpt2 = get_model()
    
    render_output(gpt2, input_text, validate_input_text, validate_n_char, n_char, cols)
            
        
    
    
    
if __name__ == '__main__':
    load_template()